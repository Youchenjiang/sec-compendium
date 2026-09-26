#!/usr/bin/env bash
# Minimal, reversible Linux containment helper.
# Default mode is status-only. Apply/rollback require explicit scope variables.
set -euo pipefail

MODE=${1:-status}
STATE_DIR=${STATE_DIR:-/var/tmp/hitcon-containment}
C2_IP=${C2_IP:-}
PROCESS_PATTERN=${PROCESS_PATTERN:-}
TARGET_PORT=${TARGET_PORT:-}
PERSISTENCE_FILE=${PERSISTENCE_FILE:-}
RESTART_CMD=${RESTART_CMD:-}
FORCE_KILL9=${FORCE_KILL9:-0}

timestamp() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
log() { printf '%s\t%s\n' "$(timestamp)" "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

usage() {
  cat <<'EOF'
usage: emergency_contain.sh [status|apply|rollback]

Explicit environment scope:
  C2_IP=<single IPv4/IPv6 address>
  PROCESS_PATTERN=<exact-enough pgrep -f pattern>
  TARGET_PORT=<listener port to verify after TERM>
  PERSISTENCE_FILE=<single cron/unit/drop-in file to quarantine>
  STATE_DIR=<rollback state directory>
  RESTART_CMD=<optional explicit rollback restart command>
  FORCE_KILL9=1  # optional; only after TERM timeout

The script never disables an interface, changes default routes, or flushes a
firewall. It adds/removes one exact OUTPUT rule and moves/restores one exact
persistence file.
EOF
}

validate_scope() {
  [[ -n $C2_IP && -n $PROCESS_PATTERN && -n $TARGET_PORT && -n $PERSISTENCE_FILE ]] || {
    usage >&2
    return 2
  }
  [[ $TARGET_PORT =~ ^[0-9]+$ ]] && (( TARGET_PORT >= 1 && TARGET_PORT <= 65535 )) || {
    echo "invalid TARGET_PORT" >&2
    return 2
  }
  have iptables || { echo "iptables is required" >&2; return 2; }
  have ss || { echo "ss is required" >&2; return 2; }
}

matching_pids() {
  pgrep -f -- "$PROCESS_PATTERN" 2>/dev/null || true
}

port_listening() {
  ss -lntp 2>/dev/null | grep -Eq "[:.]${TARGET_PORT}[[:space:]]"
}

firewall_present() {
  iptables -C OUTPUT -d "$C2_IP" -j DROP >/dev/null 2>&1
}

status() {
  validate_scope
  log "status scope c2=$C2_IP pattern=$PROCESS_PATTERN port=$TARGET_PORT persistence=$PERSISTENCE_FILE"
  local pids
  pids=$(matching_pids | paste -sd, -)
  log "process_pids=${pids:-none}"
  if port_listening; then log "listener=$TARGET_PORT present"; else log "listener=$TARGET_PORT absent"; fi
  if firewall_present; then log "outbound_block=$C2_IP present"; else log "outbound_block=$C2_IP absent"; fi
  if [[ -e $PERSISTENCE_FILE ]]; then log "persistence=present"; else log "persistence=absent"; fi
}

apply() {
  validate_scope
  [[ $EUID -eq 0 ]] || { echo "apply requires root" >&2; return 2; }
  install -d -m 0700 "$STATE_DIR"
  log "apply begin"

  if firewall_present; then
    log "firewall unchanged: exact OUTPUT block already present"
  else
    iptables -I OUTPUT 1 -d "$C2_IP" -j DROP
    printf '1\n' > "$STATE_DIR/firewall_added"
    log "firewall added: OUTPUT -d $C2_IP -j DROP; rollback=delete exact rule"
  fi

  if [[ -e $PERSISTENCE_FILE ]]; then
    # A fresh apply after a prior rollback must capture the *current* file,
    # not reuse an older backup from a previous containment cycle.
    cp -a -- "$PERSISTENCE_FILE" "$STATE_DIR/persistence.original"
    rm -f -- "$PERSISTENCE_FILE"
    printf '%s\n' "$PERSISTENCE_FILE" > "$STATE_DIR/persistence.path"
    log "persistence quarantined: $PERSISTENCE_FILE; rollback=restore saved copy"
  else
    log "persistence unchanged: already absent"
  fi

  local pids pid
  pids=$(matching_pids)
  if [[ -z $pids ]]; then
    log "process unchanged: no matching PID"
  else
    for pid in $pids; do
      kill -TERM "$pid" 2>/dev/null || true
      log "TERM sent pid=$pid"
    done
    for _ in 1 2 3 4 5; do
      sleep 1
      [[ -z $(matching_pids) ]] && break
    done
    pids=$(matching_pids)
    if [[ -n $pids && $FORCE_KILL9 == 1 ]]; then
      for pid in $pids; do
        kill -KILL "$pid" 2>/dev/null || true
        log "KILL sent pid=$pid after TERM timeout"
      done
      sleep 1
    elif [[ -n $pids ]]; then
      log "warning process still alive after TERM; FORCE_KILL9=1 required for escalation"
      return 3
    fi
  fi

  if port_listening; then
    log "warning listener $TARGET_PORT is still present after process containment"
    return 4
  fi
  log "listener $TARGET_PORT absent after TERM"
  log "apply complete"
}

rollback() {
  validate_scope
  [[ $EUID -eq 0 ]] || { echo "rollback requires root" >&2; return 2; }
  log "rollback begin"

  if [[ -e $STATE_DIR/firewall_added ]]; then
    if firewall_present; then
      iptables -D OUTPUT -d "$C2_IP" -j DROP
      log "firewall rollback: exact OUTPUT block removed"
    else
      log "firewall rollback: rule already absent"
    fi
    rm -f "$STATE_DIR/firewall_added"
  else
    log "firewall rollback: no script-owned rule recorded"
  fi

  if [[ -e $STATE_DIR/persistence.original ]]; then
    if [[ ! -e $PERSISTENCE_FILE ]]; then
      cp -a -- "$STATE_DIR/persistence.original" "$PERSISTENCE_FILE"
      log "persistence rollback: restored $PERSISTENCE_FILE"
    else
      log "persistence rollback: target already exists; preserved existing file"
    fi
  else
    log "persistence rollback: no saved copy"
  fi

  if [[ -n $RESTART_CMD && -z $(matching_pids) ]]; then
    nohup bash -c "$RESTART_CMD" >/var/log/hitcon-containment-restart.log 2>&1 &
    sleep 1
    log "process rollback: explicit RESTART_CMD launched"
  else
    log "process rollback: no restart needed/requested"
  fi
  log "rollback complete"
}

case "$MODE" in
  status) status ;;
  apply) apply ;;
  rollback) rollback ;;
  -h|--help|help) usage ;;
  *) usage >&2; exit 2 ;;
esac
