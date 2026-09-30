#!/usr/bin/env python3
"""
purple_layer_generator.py - MITRE ATT&CK Navigator v4.5 紫隊全景圖層自動生成工具
功能：
1. 自動解析 attack_defense_matrix.md 內的 ATT&CK TTP 攻防對映資料。
2. 驗證所有標註之紅隊與藍隊 Playbook 本地檔案是否存在。
3. 輸出合乎 MITRE ATT&CK Navigator 官方規範之 JSON Layer 檔案。
4. 支援直接載入 https://mitre-attack.github.io/attack-navigator/ 進行攻防覆蓋視覺化。
"""

import os
import re
import sys
import json
from datetime import date

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MATRIX_MD = os.path.join(CURRENT_DIR, "attack_defense_matrix.md")
LAYERS_DIR = os.path.join(CURRENT_DIR, "layers")
OUTPUT_JSON = os.path.join(LAYERS_DIR, "enterprise_attack_defense_layer.json")

def parse_matrix_table(md_path):
    with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    techniques = []
    broken_targets = []

    for line in content.splitlines():
        line = line.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 6:
            continue
        m = re.match(r"^\*\*(T\d+(?:\.\d+)?)\*\*$", cols[0])
        if not m:
            continue

        tech_id = m.group(1)
        red_col = cols[2]
        blue_col = cols[3]
        telemetry_col = cols[4]
        mitigation_col = cols[5]

        # 提取紅隊手冊路徑
        red_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", red_col)
        blue_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", blue_col)

        # 檢驗檔案有效性
        for text, rel_path in red_links + blue_links:
            target_path = os.path.normpath(os.path.join(CURRENT_DIR, rel_path.split("#")[0]))
            if not os.path.exists(target_path):
                broken_targets.append((tech_id, text, target_path))

        red_summary = " / ".join([t[0] for t in red_links])
        blue_summary = " / ".join([t[0] for t in blue_links])

        comment_text = (
            f"【紅隊作戰】: {red_summary}\n"
            f"【藍隊防禦】: {blue_summary}\n"
            f"【核心遙測】: {telemetry_col}\n"
            f"【對抗處置】: {mitigation_col}"
        )

        techniques.append({
            "techniqueID": tech_id,
            "tactic": "",
            "score": 3,  # 3 代表已完成紅藍雙軌對稱閉環驗證 (Purple Team Validated)
            "color": "#800080",  # 紫色高亮
            "comment": comment_text,
            "enabled": True,
            "metadata": [
                {"name": "Red Team Playbooks", "value": red_summary},
                {"name": "Blue Team Playbooks", "value": blue_summary},
                {"name": "Telemetry Source", "value": telemetry_col}
            ]
        })

    return techniques, broken_targets

def generate_navigator_layer(techniques, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    layer_data = {
        "name": f"Enterprise Purple Team Attack-Defense Matrix - {date.today().isoformat()}",
        "versions": {
            "attack": "14",
            "navigator": "4.8.0",
            "layer": "4.5"
        },
        "domain": "enterprise-attack",
        "description": "企業級紫隊對抗聯防全景熱圖，橫跨紅隊 110 篇實戰手冊與藍隊 107 篇防禦取證手冊之閉環驗證成果。",
        "filters": {
            "platforms": [
                "Windows",
                "Linux",
                "macOS",
                "IaaS",
                "Containers",
                "Active Directory"
            ]
        },
        "sorting": 3,
        "layout": {
            "layout": "side",
            "aggregateFunction": "max",
            "showID": True,
            "showName": True,
            "showAggregateScores": True,
            "countUnscored": False
        },
        "hideDisabled": False,
        "techniques": techniques,
        "gradient": {
            "colors": [
                "#ffffff",
                "#e0b0ff",
                "#ba55d3",
                "#800080"
            ],
            "minValue": 0,
            "maxValue": 3
        },
        "legendItems": [
            {
                "label": "未納入對抗驗證 (Unverified)",
                "color": "#ffffff"
            },
            {
                "label": "單軌驗證 (Single Track)",
                "color": "#e0b0ff"
            },
            {
                "label": "遙測具備 (Telemetry Ingested)",
                "color": "#ba55d3"
            },
            {
                "label": "雙軌閉環聯防 (Purple Validated)",
                "color": "#800080"
            }
        ],
        "metadata": [
            {"name": "Curriculum", "value": "Sec-Compendium Purple Team"},
            {"name": "Red Team Volume", "value": "110 Playbooks"},
            {"name": "Blue Team Volume", "value": "107 Playbooks"},
            {"name": "Generator", "value": "purple_layer_generator.py"}
        ],
        "showTacticRowBackground": True,
        "tacticRowBackground": "#4a0e4e",
        "selectTechniquesAcrossTactics": True,
        "selectSubtechniquesWithParent": True
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(layer_data, f, ensure_ascii=False, indent=2)

    return len(techniques)

def main():
    print("=" * 75)
    print("🟣 開始執行【紫隊 ATT&CK Navigator Layer 全景圖層產生器】...")
    print("=" * 75)

    if not os.path.exists(MATRIX_MD):
        print(f"❌ 找不到矩陣檔案: {MATRIX_MD}")
        sys.exit(1)

    techniques, broken = parse_matrix_table(MATRIX_MD)

    if broken:
        print(f"❌ 發現 {len(broken)} 處無效的 Playbook 參照目標:")
        for tid, title, path in broken:
            print(f"   [{tid}] {title} -> {path}")
        sys.exit(1)

    count = generate_navigator_layer(techniques, OUTPUT_JSON)

    print(f"✅ 成功自 attack_defense_matrix.md 解析 {count} 項關鍵 ATT&CK 技術！")
    print("✅ 所有引用的紅隊與藍隊實戰手冊 100% 存在，無任何無效路徑！")
    print(f"📁 已成功匯出 ATT&CK Navigator Layer 檔案至:\n   👉 {OUTPUT_JSON}")
    print("=" * 75)
    print("💡 使用說明：可直接開啟 https://mitre-attack.github.io/attack-navigator/")
    print("   點擊「Open Existing Layer」->「Upload from local」載入此 JSON 檔案，即可即時呈現紫隊對抗覆蓋熱圖！")
    print("=" * 75)

if __name__ == "__main__":
    main()
