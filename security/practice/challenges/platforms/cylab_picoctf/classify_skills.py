"""Classify the CyLab challenge snapshot into teaching skills.

IDs listed in SKILLS were placed one by one; IDs also in NAME_ONLY were placed
from the title alone (mostly picoCTF 2026, not yet checked against their
descriptions). Anything unlisted falls back to its official-category default.

Usage: python classify_skills.py [snapshot.csv] [output.csv]
"""
import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

SKILLS = {
    "M1 編碼與資料表示": {67, 710, 371, 86, 58, 404, 414, 390, 35, 239, 742, 762, 724, 730},
    "M2 前端暴露與 HTTP": {275, 18, 426, 427, 469, 4, 161, 132, 476, 274, 406, 349, 296, 295, 291,
                         152, 131, 9, 356},
    "M3 封包分析": {286, 459, 30, 84, 264, 362, 115, 110, 103, 237, 311, 42, 32},
    "M4 認證、Session 與 Cookie": {245, 246, 247, 248, 249, 712, 173, 46, 288, 124, 177, 236, 25,
                                 520, 521, 419, 739, 749, 743, 765, 467, 66, 278, 200, 69, 355},
    "M5 伺服器端注入與輸入信任": {492, 488, 304, 303, 358, 729, 752, 443, 88, 174, 128, 80, 59, 8,
                              108, 202, 484, 376, 180, 270, 482, 445, 185},
    "M6 古典密碼與雜湊": {144, 68, 62, 475, 243, 373, 316, 312, 309, 308, 307, 289, 280, 210, 158,
                       64, 43, 40, 38, 31, 21, 3, 148, 114, 407, 253, 254, 418, 261, 474, 473, 351},
    "M7a 檔案、中繼資料與隱寫": {186, 408, 44, 450, 444, 423, 530, 524, 523, 519, 460, 698, 129, 265,
                             52, 19, 279, 74, 290, 112, 350, 305, 359, 268, 420, 481, 139, 26, 28,
                             101, 53, 205, 51, 81, 415, 432, 348, 354, 141, 117, 206, 47, 36, 56,
                             70, 27, 13, 83, 54},
    "M7b 磁碟、記憶體、日誌與 Git 調查": {505, 506, 507, 704, 301, 300, 137, 113, 285, 284, 87, 383,
                                   453, 454, 413, 456, 720, 721, 705, 706, 707, 130},
    "M7c 讀程式找密鑰（入門逆向）": {7, 104, 472, 12, 60, 71, 77, 45, 65, 10, 175, 121, 314, 287,
                              256, 400, 401, 402, 271, 294, 375, 428, 116},
    "Linux、工具與程式操作": {147, 170, 22, 156, 34, 176, 85, 37, 424, 189, 163, 320, 322, 240, 241,
                          250, 238, 242, 442, 425, 471, 527, 411, 405, 410, 766, 764, 735, 757,
                          740, 759, 741, 734, 461, 462, 463, 166, 48, 251, 384, 363, 347, 377,
                          378, 436, 437, 91, 49, 15, 82, 748, 756, 732, 483},
    "現代密碼學（RSA／AES／XOR 等）": set(),
    "二進位逆向（組語、除錯器）": set(),
    "Binary Exploitation（pwn）": set(),
    "進階 Web（XSS、WASM 等）": {726, 496, 447, 360, 344, 282, 277, 204, 190, 182, 153, 33, 29},
    "AI": set(),
    "Blockchain": set(),
}

DEFAULT = {
    "Cryptography": "現代密碼學（RSA／AES／XOR 等）",
    "Reverse Engineering": "二進位逆向（組語、除錯器）",
    "Binary Exploitation": "Binary Exploitation（pwn）",
    "Web Exploitation": "進階 Web（XSS、WASM 等）",
    "Forensics": "M7a 檔案、中繼資料與隱寫",
    "General Skills": "Linux、工具與程式操作",
    "Artificial Intelligence": "AI",
    "Blockchain": "Blockchain",
}

NAME_ONLY = {710, 742, 762, 724, 730, 729, 752, 698, 704, 720, 721,
             705, 706, 707, 766, 764, 735, 757, 740, 759, 741, 734, 748, 756, 732, 726}


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "cylab_all_challenges_2026-08-08.csv"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "cylab_skill_classification_2026-08-08.csv"

    by_id = {}
    for skill, ids in SKILLS.items():
        for i in ids:
            assert i not in by_id, f"{i} in both {by_id[i]} and {skill}"
            by_id[i] = skill
    assert NAME_ONLY <= set(by_id), NAME_ONLY - set(by_id)

    rows = list(csv.DictReader(src.open(encoding="utf-8-sig")))
    assert set(by_id) <= {int(r["ID"]) for r in rows}
    out, total, easy, basis = [], Counter(), Counter(), Counter()
    for r in rows:
        cid = int(r["ID"])
        skill = by_id.get(cid) or DEFAULT[r["分類"]]
        how = "依題名推測" if cid in NAME_ONLY else "逐題歸類" if cid in by_id else "官方分類預設"
        out.append({"ID": cid, "題目名稱": r["題目名稱"], "官方分類": r["分類"],
                    "難易度": r["難易度"], "技能": skill, "歸類依據": how})
        total[skill] += 1
        easy[skill] += r["難易度"] == "1"
        basis[skill, how] += 1

    with dst.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(sorted(out, key=lambda x: (list(SKILLS).index(x["技能"]), x["難易度"], -x["ID"])))

    print("| 技能 | 題數 | Easy | 逐題歸類 | 依題名推測 | 官方分類預設 |")
    print("|---|---|---|---|---|---|")
    for s in SKILLS:
        print(f"| {s} | {total[s]} | {easy[s]} | {basis[s, '逐題歸類']} | {basis[s, '依題名推測']} | {basis[s, '官方分類預設']} |")
    print(f"| 合計 | {sum(total.values())} | {sum(easy.values())} | | | |")


if __name__ == "__main__":
    main()
