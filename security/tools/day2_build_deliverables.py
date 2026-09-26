#!/usr/bin/env python3
r"""day2_build_deliverables.py - turn raw EZ-tool CSV output into Day 2 deliverables.

Input  (--toolout): the directory produced by vm_day2_analyze.ps1 on the guest,
                    containing prefetch.csv, amcache_UnassociatedFileEntries.csv,
                    usbstore.csv, userassist_raw.csv, consentstore_raw.csv.
Output (--out):      prefetch.csv, amcache.csv, shimcache.csv,
                    usbstore_devices.csv, userassist.csv, consentstore.csv

The transformations here are exactly the "artifact gotchas" the sprint is meant to
teach, applied mechanically so the deliverable never depends on hand-eyeballing:
  * USBSTOR instance IDs end with "&0" (an invalid-instance marker, not firmware).
  * UserAssist value names are ROT13; the run count + last-run live in a 72-byte blob.
  * ConsentStore timestamps are FILETIME in LastUsedTimeStart / LastUsedTimeStop, and
    the DURATION is Stop - Start (LastWrite is NOT the usage time).

Standard library only.
"""
import argparse
import csv
import os
from datetime import datetime, timezone, timedelta


def read_rows(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def rot13(s):
    out = []
    for c in s:
        if "a" <= c <= "z":
            out.append(chr(ord("a") + (ord(c) - ord("a") + 13) % 26))
        elif "A" <= c <= "Z":
            out.append(chr(ord("A") + (ord(c) - ord("A") + 13) % 26))
        else:
            out.append(c)
    return "".join(out)


def filetime_utc(v):
    """Windows FILETIME (100ns since 1601-01-01 UTC) -> ISO8601 UTC string."""
    try:
        n = int(v)
    except (TypeError, ValueError):
        return ""
    if n <= 0:
        return ""
    seconds, ticks = divmod(n, 10_000_000)
    dt = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(
        seconds=seconds, microseconds=ticks // 10
    )
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"


def build(toolout, out):
    os.makedirs(out, exist_ok=True)

    # --- 1. prefetch.csv (pass-through, already normalized by PECmd) -----------
    pf = read_rows(os.path.join(toolout, "prefetch.csv"))
    with open(os.path.join(out, "prefetch.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["SourceFilename", "ExecutableName", "RunCount", "LastRun",
                    "PreviousRun0", "PreviousRun1", "PreviousRun2", "PreviousRun3",
                    "Size", "Hash"])
        for r in pf:
            w.writerow([r.get("SourceFilename", ""), r.get("ExecutableName", ""),
                        r.get("RunCount", ""), r.get("LastRun", ""),
                        r.get("PreviousRun0", ""), r.get("PreviousRun1", ""),
                        r.get("PreviousRun2", ""), r.get("PreviousRun3", ""),
                        r.get("Size", ""), r.get("Hash", "")])

    # --- 2. amcache.csv (SHA-1 of file entries) --------------------------------
    am = read_rows(os.path.join(toolout, "amcache_UnassociatedFileEntries.csv"))
    with open(os.path.join(out, "amcache.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["SHA1", "FullPath", "Name", "Size", "LastWriteTimestampUTC",
                    "LinkDateUTC", "IsOsComponent", "ProductName"])
        for r in am:
            w.writerow([r.get("SHA1", ""), r.get("FullPath", ""), r.get("Name", ""),
                        r.get("Size", ""), r.get("FileKeyLastWriteTimestamp", ""),
                        r.get("LinkDate", ""), r.get("IsOsComponent", ""),
                        r.get("ProductName", "")])

    # --- 3. shimcache.csv (pass-through from AppCompatCacheParser) ------------
    sc = read_rows(os.path.join(toolout, "shimcache.csv"))
    with open(os.path.join(out, "shimcache.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ControlSet", "CacheEntryPosition", "Path", "LastModifiedTimeUTC",
                    "Executed", "Duplicate", "SourceFile"])
        for r in sc:
            w.writerow([r.get("ControlSet", ""), r.get("CacheEntryPosition", ""),
                        r.get("Path", ""), r.get("LastModifiedTimeUTC", ""),
                        r.get("Executed", ""), r.get("Duplicate", ""),
                        r.get("SourceFile", "")])

    # --- 4. usbstore_devices.csv (strip the &0 instance suffix) ----------------
    usb = read_rows(os.path.join(toolout, "usbstore.csv"))
    devices = {}
    for r in usb:
        kp = r.get("KeyPath", "")
        if not kp.startswith("ROOT\\CurrentControlSet\\Enum\\USBSTOR\\"):
            continue
        tail = kp[len("ROOT\\CurrentControlSet\\Enum\\USBSTOR\\"):]
        parts = tail.split("\\")
        if len(parts) < 2:
            continue
        dev_type, inst = parts[0], parts[1]
        d = devices.setdefault(inst, {"dev_type": dev_type, "values": {}})
        if r.get("ValueName"):
            d["values"][r["ValueName"]] = r.get("ValueData", "")
    with open(os.path.join(out, "usbstore_devices.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["InstanceId", "DeviceType", "SerialNumber", "FriendlyName",
                    "DeviceDesc", "Service", "FirstInstallDateUTC"])
        for inst, d in devices.items():
            serial = inst[:-2] if inst.endswith("&0") else inst
            vals = d["values"]
            w.writerow([inst, d["dev_type"], serial, vals.get("FriendlyName", ""),
                        vals.get("DeviceDesc", ""), vals.get("Service", ""),
                        filetime_utc(vals.get("FirstInstallDate"))])

    # --- 5. userassist.csv (ROT13 decode + parsed blob) ------------------------
    ua = read_rows(os.path.join(toolout, "userassist_raw.csv"))
    with open(os.path.join(out, "userassist.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["KeyPath", "ValueNameROT13", "DecodedPath", "RunCount",
                    "LastExecutedUTC", "LastWriteUTC"])
        seen = set()
        for r in ua:
            vn = r.get("ValueName", "")
            if not vn or vn == "(default)":
                continue
            decoded = rot13(vn)
            # RECmd's UserAssist plugin puts the decoded path in ValueData and
            # "Run count: N" in ValueData2 when it can parse the blob.
            path = r.get("ValueData", "") if r.get("ValueData", "").startswith("C:") else decoded
            # RECmd's UserAssist plugin splits the parsed blob across ValueData2/3:
            #   ValueData2 -> "Last executed: <stamp>"   ValueData3 -> "Run count: N"
            runcount = ""
            for extra in (r.get("ValueData2", ""), r.get("ValueData3", "")):
                if "Run count:" in extra:
                    runcount = extra.split("Run count:")[-1].strip()
            last = ""
            for extra in (r.get("ValueData2", ""), r.get("ValueData3", "")):
                if extra.startswith("Last executed:"):
                    last = extra.split("Last executed:", 1)[1].strip()
            sig = (vn, path, runcount, last)
            if sig in seen:
                continue
            seen.add(sig)
            w.writerow([r.get("KeyPath", ""), vn, path, runcount, last,
                        r.get("LastWriteTimestamp", "")])

    # --- 6. consentstore.csv (Start/Stop + duration) ---------------------------
    cs = read_rows(os.path.join(toolout, "consentstore_raw.csv"))
    apps = {}
    for r in cs:
        kp = r.get("KeyPath", "")
        marker = "ConsentStore\\"
        if marker not in kp:
            continue
        rest = kp.split(marker, 1)[1]
        seg = rest.split("\\")
        if len(seg) < 3:
            continue
        cap, inst = seg[0], seg[-1]
        if r.get("ValueName"):
            apps.setdefault((cap, inst), {})[r["ValueName"]] = r.get("ValueData", "")
    with open(os.path.join(out, "consentstore.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Capability", "Application", "Permission", "LastUsedTimeStartUTC",
                    "LastUsedTimeStopUTC", "DurationSeconds"])
        for (cap, inst), v in sorted(apps.items()):
            start, stop = v.get("LastUsedTimeStart"), v.get("LastUsedTimeStop")
            dur = ""
            if start and stop:
                try:
                    dur = (int(stop) - int(start)) / 10_000_000
                except ValueError:
                    dur = ""
            w.writerow([cap, inst, v.get("Value", ""), filetime_utc(start),
                        filetime_utc(stop), dur])

    print("deliverables written to", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--toolout", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    build(a.toolout, a.out)
