import sys
import json
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.paths import RESULTS_DIR


def main():
    path = RESULTS_DIR / 'global_4701_sast_findings.json'
    if not path.exists():
        print(f"[!] SAST findings file not found: {path}")
        print("[!] Run scripts/scan.py --scope global first to generate the dataset.")
        return 1

    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    print('Total Findings:', len(data))
    pkgs = {d['package'] for d in data}
    print('Total Distinct Packages with Findings:', len(pkgs))

    sev_counts = Counter(d['severity'] for d in data)
    cat_counts = Counter(d['category'] for d in data)
    rule_counts = Counter(f"{d['rule_id']}: {d['type']}" for d in data)
    pkg_counts = Counter(d['package'] for d in data)

    print('\n--- Severity Breakdown ---')
    for s, c in sev_counts.most_common():
        print(f'  {s:10}: {c:6d} ({c / len(data) * 100:.1f}%)')

    print('\n--- Category Breakdown ---')
    for cat, c in cat_counts.most_common():
        print(f'  {cat:24}: {c:6d} ({c / len(data) * 100:.1f}%)')

    print('\n--- Top 20 Vulnerable Packages ---')
    for p, c in pkg_counts.most_common(20):
        print(f'  {p:45}: {c:5d}')

    print('\n--- Top 15 Specific Rules Triggered ---')
    for r, c in rule_counts.most_common(15):
        print(f'  {r:45}: {c:5d}')
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
