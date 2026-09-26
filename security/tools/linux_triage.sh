#!/usr/bin/env bash
# Read-only Linux endpoint triage for DFIR / competition use.
# No package installation, service changes, mounts, kills, writes, or cleanup.
set -u

PID_FILTER=""
if [[ ${1:-} == "--pid" ]]; then
  PID_FILTER=${2:-}
  if [[ ! $PID_FILTER =~ ^[0-9]+$ ]]; then
    echo "usage: $0 [--pid <numeric-pid>]" >&2
    exit 2
  fi
elif [[ $# -gt 0 ]]; then
  echo "usage: $0 [--pid <numeric-pid>]" >&2
  exit 2
fi

section() {
  printf '\n===== %s =====\n' "$1"
}

have() {
  command -v "$1" >/dev/null 2>&1
}

section "Acquisition context"
printf 'utc_now='; date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || true
printf 'hostname='; hostname 2>/dev/null || true
printf 'kernel='; uname -a 2>/dev/null || true
printf 'timezone='; timedatectl show -p Timezone --value 2>/dev/null || printf 'unknown\n'
printf 'uid='; id 2>/dev/null || true
printf 'uptime='; uptime 2>/dev/null || true

section "Logged-on users"
who -a 2>/dev/null || true
last -n 20 -F 2>/dev/null || true

section "Process tree / lineage"
ps -eo pid=,ppid=,user=,lstart=,etime=,args= --forest 2>/dev/null || ps auxww 2>/dev/null || true

section "Processes reparented to PID 1"
ps -eo pid=,ppid=,user=,lstart=,args= 2>/dev/null | awk '$2 == 1 {print}' || true

section "Network sockets with process ownership"
if have ss; then
  ss -tunap 2>/dev/null || ss -tuna 2>/dev/null || true
else
  echo "ss: MISSING"
fi
if have lsof; then
  lsof -nP -i 2>/dev/null || true
else
  echo "lsof: MISSING"
fi

if [[ -n $PID_FILTER ]]; then
  section "Focused /proc/${PID_FILTER}"
  if [[ -d /proc/$PID_FILTER ]]; then
    grep -E '^(Name|State|Pid|PPid|Uid|Gid|Threads|Cap(Inh|Prm|Eff|Bnd|Amb)):' "/proc/$PID_FILTER/status" 2>/dev/null || true
    printf 'exe='; readlink -f "/proc/$PID_FILTER/exe" 2>/dev/null || true
    printf 'cwd='; readlink -f "/proc/$PID_FILTER/cwd" 2>/dev/null || true
    printf 'cmdline='; tr '\0' ' ' < "/proc/$PID_FILTER/cmdline" 2>/dev/null; printf '\n'
    if [[ -r /proc/$PID_FILTER/environ ]]; then
      printf 'environ_keys='; tr '\0' '\n' < "/proc/$PID_FILTER/environ" | sed 's/=.*//' | paste -sd, -; printf '\n'
    else
      echo "environ_keys=unreadable"
    fi
    ls -la "/proc/$PID_FILTER/fd" 2>/dev/null || true
    if have lsof; then
      lsof -nP -p "$PID_FILTER" 2>/dev/null || true
    fi
  else
    echo "PID $PID_FILTER is not present in /proc"
  fi
fi

section "/etc/ld.so.preload"
if [[ -e /etc/ld.so.preload ]]; then
  stat /etc/ld.so.preload 2>/dev/null || true
  cat /etc/ld.so.preload 2>/dev/null || echo "present but unreadable"
else
  echo "not present"
fi

section "Kernel modules / preload-adjacent configuration"
cat /proc/modules 2>/dev/null || true
if [[ -f /etc/modules ]]; then
  echo "--- /etc/modules ---"
  cat /etc/modules 2>/dev/null || true
fi
if [[ -d /etc/modprobe.d ]]; then
  find /etc/modprobe.d -maxdepth 1 -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TSZ %p\n' 2>/dev/null | sort || true
fi

section "Cron persistence"
if [[ -f /etc/crontab ]]; then
  echo "--- /etc/crontab ---"
  cat /etc/crontab 2>/dev/null || true
fi
for dir in /etc/cron.d /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly; do
  if [[ -d $dir ]]; then
    echo "--- $dir ---"
    find "$dir" -maxdepth 1 -type f -printf '%M %u:%g %TY-%Tm-%TdT%TH:%TM:%TSZ %p\n' 2>/dev/null | sort || true
  fi
done
if have crontab; then
  echo "--- current-user crontab ---"
  crontab -l 2>/dev/null || echo "none/read denied"
fi

section "systemd persistence / running services"
if have systemctl; then
  systemctl list-unit-files --type=service --state=enabled --no-pager 2>/dev/null || true
  echo "--- running services ---"
  systemctl list-units --type=service --state=running --no-pager --no-legend 2>/dev/null || true
  echo "--- local unit files ---"
  find /etc/systemd/system -type f -o -type l 2>/dev/null | sort || true
else
  echo "systemctl: MISSING"
fi

section "SUID files on root filesystem"
find / -xdev -type f -perm -4000 -printf '%M %u:%g %TY-%Tm-%TdT%TH:%TM:%TSZ %p\n' 2>/dev/null | sort || true

section "Auditd availability / recent coverage"
for tool in ausearch aureport auditctl; do
  if have "$tool"; then
    printf '%s=' "$tool"; command -v "$tool"
  else
    echo "$tool=MISSING"
  fi
done
if have auditctl; then
  auditctl -s 2>/dev/null || true
  auditctl -l 2>/dev/null || true
fi
if have ausearch; then
  # Read-only recent sample. Full forensic reconstruction should still preserve
  # the raw log and group records by the complete epoch:serial audit id.
  ausearch -ts today -m SYSCALL,EXECVE,USER_CMD -i 2>/dev/null | tail -n 200 || true
elif [[ -r /var/log/audit/audit.log ]]; then
  echo "ausearch unavailable; raw /var/log/audit/audit.log is readable"
  wc -l /var/log/audit/audit.log 2>/dev/null || true
  tail -n 50 /var/log/audit/audit.log 2>/dev/null || true
else
  echo "ausearch unavailable and raw audit.log is not readable/present"
fi

section "High-value filesystem timestamps"
for path in /etc/ld.so.preload /etc/crontab /etc/rc.local /etc/passwd /etc/shadow /etc/sudoers; do
  [[ -e $path ]] && stat -c '%n | mode=%A | owner=%U:%G | size=%s | mtime=%y | ctime=%z' "$path" 2>/dev/null
done

section "Triage complete"
echo "All commands above are read-only. Preserve raw source artifacts separately before interpretation."
