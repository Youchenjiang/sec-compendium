#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <windows.h>
#ifndef ENABLE_VIRTUAL_TERMINAL_PROCESSING
#define ENABLE_VIRTUAL_TERMINAL_PROCESSING 0x0004
#endif
#endif

// ======================================================================
//  國立中央大學資訊管理學系 碩士生涯模擬器 (12 回合終端遊戲 v4.6 - 彩蛋修復版)
// ======================================================================

// 系統基礎顏色
#define C_RESET       "\033[0m"

// 體力與壓力：生理/心理健康指標 (綠 / 黃 / 紅)
#define C_GREEN       "\033[1;32m" // 安全 / 充沛 / 放鬆
#define C_YELLOW      "\033[1;33m" // 注意 / 疲憊 / 緊繃
#define C_RED         "\033[1;31m" // 危險 / 瀕死 / 崩潰

// 論文進度：學術研究累進指標 (藍 / 青 / 紫)
#define C_PAPER_LOW   "\033[1;94m" // 起步階段 (< 50%)
#define C_PAPER_MID   "\033[1;36m" // 穩步突破 (50% ~ 99%)
#define C_PAPER_HIGH  "\033[1;35m" // 完稿達標 (>= 100%)

const unsigned char ENCRYPTED_FLAG[64] = {
    0x14, 0x19, 0x0f, 0x17, 0x13, 0x09, 0x21, 0x3d, 0x28, 0x3b,
    0x3e, 0x2f, 0x3b, 0x2e, 0x33, 0x35, 0x34, 0x05, 0x33, 0x29,
    0x05, 0x3b, 0x05, 0x36, 0x33, 0x3f, 0x05, 0x22, 0x22, 0x22,
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
    0x22, 0x22, 0x22, 0x27, 0x00
};
const unsigned char XOR_KEY = 0x5A;

void enable_virtual_terminal() {
#ifdef _WIN32
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut != INVALID_HANDLE_VALUE) {
        DWORD dwMode = 0;
        if (GetConsoleMode(hOut, &dwMode)) {
            dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
            SetConsoleMode(hOut, dwMode);
        }
    }
#endif
}

void clear_screen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void to_lower_str(char* str) {
    for (int i = 0; str[i]; i++) {
        if (str[i] >= 'A' && str[i] <= 'Z') {
            str[i] = (char)(str[i] + ('a' - 'A'));
        }
    }
}

const char* get_hp_color(int hp) {
    if (hp >= 60) return C_GREEN;
    if (hp >= 25) return C_YELLOW;
    return C_RED;
}

const char* get_stress_color(int stress) {
    if (stress >= 75) return C_RED;
    if (stress >= 40) return C_YELLOW;
    return C_GREEN;
}

const char* get_paper_color(int paper) {
    if (paper >= 100) return C_PAPER_HIGH;
    if (paper >= 50) return C_PAPER_MID;
    return C_PAPER_LOW;
}

const char* get_coffee_color(int coffee) {
    return coffee > 0 ? C_GREEN : C_RED;
}

// 即時計算選了之後該數值會變成的狀態顏色
const char* calc_hp_color(int cur_hp, int delta) {
    int next_hp = cur_hp + delta;
    if (next_hp > 100) next_hp = 100;
    if (next_hp < 0) next_hp = 0;
    return get_hp_color(next_hp);
}

const char* calc_stress_color(int cur_stress, int delta) {
    int next_stress = cur_stress + delta;
    if (next_stress > 100) next_stress = 100;
    if (next_stress < 0) next_stress = 0;
    return get_stress_color(next_stress);
}

const char* calc_paper_color(int cur_paper, int delta) {
    int next_paper = cur_paper + delta;
    if (next_paper < 0) next_paper = 0;
    return get_paper_color(next_paper);
}

void make_bar(char* buf, int val, int max_val) {
    int filled = (val * 10) / max_val;
    if (filled < 0) filled = 0;
    if (filled > 10) filled = 10;
    for (int i = 0; i < filled; i++) buf[i] = '#';
    for (int i = filled; i < 10; i++) buf[i] = '-';
    buf[10] = '\0';
}

void render_screen(int round_num, const char* sem_name, int hp, int stress, int paper, int coffee, const char* msg) {
    clear_screen();
    const char* hp_c = get_hp_color(hp);
    const char* st_c = get_stress_color(stress);
    const char* pa_c = get_paper_color(paper);
    const char* cf_c = get_coffee_color(coffee);

    char hp_bar[16], stress_bar[16], paper_bar[16];
    make_bar(hp_bar, hp, 100);
    make_bar(stress_bar, stress, 100);
    make_bar(paper_bar, paper, 100);

    printf("==============================================================================\n");
    printf("        國立中央大學資訊管理學系 《咪挺、肝與黑咖啡》 (12 回合修羅場 v4.2)\n");
    printf("==============================================================================\n");
    printf(" 💚 體力: [%s] %s%3d/100%s | 🧠 壓力: [%s] %s%3d/100%s\n", 
           hp_bar, hp_c, hp < 0 ? 0 : hp, C_RESET,
           stress_bar, st_c, stress > 100 ? 100 : stress, C_RESET);
    printf(" 📑 論文: [%s] %s%3d%%%s   | ☕ 咖啡: %s%d 罐%s | 📅 回合: 第 %d/12 回合 (%s)\n", 
           paper_bar, pa_c, paper, C_RESET,
           cf_c, coffee, C_RESET, round_num, sem_name);
    printf("==============================================================================\n");
    if (msg && msg[0] != '\0') {
        printf("%s\n", msg);
        printf("------------------------------------------------------------------------------\n");
    }
}

int show_settlement(int is_victory, const char* reason, int hp, int stress, int paper) {
    clear_screen();
    const char* hp_c = get_hp_color(hp);
    const char* st_c = get_stress_color(stress);
    const char* pa_c = get_paper_color(paper);

    printf("==============================================================================\n");
    printf("                國立中央大學資訊管理學系 《咪挺、肝與黑咖啡》 結算報告\n");
    printf("==============================================================================\n\n");
    
    printf(" 【個人修業數值統計】\n");
    printf("   * 💚 最終體力值：%s%d / 100%s\n", hp_c, hp < 0 ? 0 : hp, C_RESET);
    printf("   * 🧠 最終壓力值：%s%d / 100%s\n", st_c, stress > 100 ? 100 : stress, C_RESET);
    printf("   * 📑 總論文進度：%s%d%% / 100%%%s\n\n", pa_c, paper, C_RESET);
    
    printf("------------------------------------------------------------------------------\n");
    if (is_victory) {
        char decrypted[64];
        for (int i = 0; i < 64; i++) {
            if (ENCRYPTED_FLAG[i] == 0x00) {
                decrypted[i] = '\0';
                break;
            }
            decrypted[i] = (char)(ENCRYPTED_FLAG[i] ^ XOR_KEY);
        }
        decrypted[63] = '\0';
        
        // 按照超越 100% 的進度比例給予不同分級榮譽與口委評語
        if (paper >= 180) {
            printf(" 🎓 [審查結果]：👑🌟 %s超越極限！恭喜達成【資管傳奇所神】傳奇榮耀！%s 🌟👑\n", C_PAPER_HIGH, C_RESET);
            printf(" 📜 [口委評語]：%s『論文進度高達 %d%%！口委全體起立鼓掌，指導教授感動落淚，系主任當場詢問要不要直接聘為助理教授！』%s\n\n", C_GREEN, paper, C_RESET);
        } else if (paper >= 150) {
            printf(" 🎓 [審查結果]：🏆✨ %s驚為天人！恭喜以【特優第一名】成績榮耀畢業！%s ✨🏆\n", C_PAPER_HIGH, C_RESET);
            printf(" 📜 [口委評語]：%s『論文進度達到 %d%%！口委一致推薦直接投稿 IEEE/ACM 頂級期刊，教授強力推薦留讀博士班！』%s\n\n", C_GREEN, paper, C_RESET);
        } else if (paper >= 120) {
            printf(" 🎓 [審查結果]：🎉🎉 %s恭喜以【優等成績】高分通過口試！順利取得碩士學位！%s 🎉🎉\n", C_GREEN, C_RESET);
            printf(" 📜 [口委評語]：%s『論文進度達 %d%%，實驗數據扎實且論點清晰，教授在台下頻頻點頭讚賞！』%s\n\n", C_GREEN, paper, C_RESET);
        } else {
            printf(" 🎓 [審查結果]：🎉 %s恭喜通過口試！順利取得國立中央大學資管碩士學位！%s 🎉\n", C_GREEN, C_RESET);
            printf(" 📜 [口委評語]：%s『論文進度 %d%% 壓線達標，雖有驚無險但架構完整，祝未來求職順利！』%s\n\n", C_GREEN, paper, C_RESET);
        }

        printf(" 🏆 [畢業證書驗證碼 Flag]：%s%s%s\n\n", C_PAPER_HIGH, decrypted, C_RESET);
        printf(" 📌 (請完整複製上方包含 NCUMIS{...} 的字串，提交至 CTFd 平台獲得分數！)\n");
    } else {
        printf(" ❌ [審查結果]：%s很遺憾，本次修業未達口試通過標準！%s\n", C_RED, C_RESET);
        printf(" ⚠️ [原因說明]：%s%s%s\n", C_RED, reason, C_RESET);
    }
    printf("==============================================================================\n\n");
    
    while (1) {
        printf(" 請選擇下一步行動：\n");
        printf("  [1] 重新開始一段新的碩士生涯 (Restart)\n");
        printf("  [2] 結束並退出遊戲 (Exit)\n\n");
        printf(" 請輸入選項代號 [1-2]: ");
        fflush(stdout);
        
        char buf[64];
        if (scanf("%63s", buf) != 1) continue;
        if (strcmp(buf, "1") == 0 || strcmp(buf, "r") == 0 || strcmp(buf, "R") == 0) {
            return 1; // Restart
        }
        if (strcmp(buf, "2") == 0 || strcmp(buf, "q") == 0 || strcmp(buf, "Q") == 0 || strcmp(buf, "exit") == 0) {
            printf("\n[*] 感謝遊玩！祝您在中央資管研究所研究順利、順利畢業！\n");
            fflush(stdout);
#ifdef _WIN32
            Sleep(800);
#endif
            return 0; // Exit
        }
        printf("\n[!] ⚠️ 無效輸入，請輸入 1 (重新開始) 或 2 (退出)！\n\n");
    }
}

int show_easter_egg(int egg_type) {
    clear_screen();
    char decrypted[64];
    for (int i = 0; i < 64; i++) {
        if (ENCRYPTED_FLAG[i] == 0x00) {
            decrypted[i] = '\0';
            break;
        }
        decrypted[i] = (char)(ENCRYPTED_FLAG[i] ^ XOR_KEY);
    }
    decrypted[63] = '\0';

    printf("==============================================================================\n");
    if (egg_type == 99) {
        printf("       ⚡ [隱藏結局 1/3]：時空跳躍・助教的極速除錯通道 (Debug Warp) ⚡\n");
        printf("==============================================================================\n\n");
        printf(" 🌀 眼前時空劇烈扭曲，管二館的時鐘瘋狂倒轉旋轉...\n");
        printf(" ✨ 你輸入了內部除錯代碼 [99]，瞬間跳過 12 個月的 Meeting、專案與論文地獄！\n");
        printf(" 🚀 穿越蟲洞直接降落在兩年後的碩士學位口試會場！\n\n");
        printf("------------------------------------------------------------------------------\n");
        printf(" 【時空旅者修業數據】\n");
        printf("   * 💚 體力值：%s100 / 100 (無消耗完美狀態)%s\n", C_GREEN, C_RESET);
        printf("   * 🧠 壓力值：%s0 / 100 (零壓力神仙體驗)%s\n", C_GREEN, C_RESET);
        printf("   * 📑 論文進度：%s999%% (超越光速完成)%s\n\n", C_PAPER_HIGH, C_RESET);
        printf(" 🎓 [審查結果]：⏩✨ %s【時空旅者・跳級神童】%s ✨⏩\n", C_PAPER_HIGH, C_RESET);
        printf(" 📜 [口委評語]：%s『系統紀錄顯示你只用了 0.01 秒就完成兩年學業... 雖然不知道你怎麼辦到的，但既然系統全亮綠燈，那就直接頒發畢業證書吧！』%s\n\n", C_GREEN, C_RESET);
    } else if (egg_type == 100) {
        printf("       💀 [隱藏結局 2/3]：駭客入侵・取得管二館最高權限 (Root Privilege) 💀\n");
        printf("==============================================================================\n\n");
        printf(" 🖥️ [ALERT] Access Granted! # uid=0(root) gid=0(root) groups=0(root)\n");
        printf(" 💻 終端機黑底綠字瘋狂刷屏，你成功入侵了中央資管系辦伺服器核心數據庫！\n");
        printf(" 💉 執行指令：UPDATE student_status SET status='PASSED', gpa=4.3 WHERE id='YOU';\n\n");
        printf("------------------------------------------------------------------------------\n");
        printf(" 【駭客特權修業數據】\n");
        printf("   * 💚 體力值：%s99999 / 99999 (已鎖定最高血量)%s\n", C_GREEN, C_RESET);
        printf("   * 🧠 壓力值：%s0 / 0 (壓力數據表已遭 DROP TABLE)%s\n", C_GREEN, C_RESET);
        printf("   * 📑 論文進度：%s404%% (Access Override)%s\n\n", C_PAPER_HIGH, C_RESET);
        printf(" 🎓 [審查結果]：🕶️🏴‍☠️ %s【駭客教父・頂級資安大老】%s 🏴‍☠️🕶️\n", C_PAPER_HIGH, C_RESET);
        printf(" 📜 [口委評語]：%s『口試當天，口委們發現自己的電腦桌布全被你換成貓咪照片，成績系統已被寫入永久通過。資安教授欣慰微笑：「你已掌握本系最強精髓，准予最高榮譽畢業！」』%s\n\n", C_GREEN, C_RESET);
    } else if (egg_type == 101) {
        printf("       💖 [隱藏結局 3/3]：信仰充能・中央資管真愛大圓滿 (MIS Overdrive) 💖\n");
        printf("==============================================================================\n\n");
        printf(" 💖 [信仰爆發]：偵測到純度 100%% 的中央資管忠誠信仰 (ilovencumis)！\n");
        printf(" 🌲 中大湖的黑天鵝為你振翅高歌，百花川的花瓣如雨灑落，宵夜街阿姨送你永久加飯！\n");
        printf(" ☕ 管二館全體教授深受感動，聯名奉上無限續杯【特濃黑咖啡】！\n\n");
        printf("------------------------------------------------------------------------------\n");
        printf(" 【真愛信仰修業數據】\n");
        printf("   * 💚 體力值：%s200 / 100 (特濃黑咖啡無限暴擊)%s\n", C_GREEN, C_RESET);
        printf("   * 🧠 壓力值：%s-100 / 100 (幸福感爆棚完全無壓力)%s\n", C_GREEN, C_RESET);
        printf("   * 📑 論文進度：%s520%% (中大真愛無價)%s\n\n", C_PAPER_HIGH, C_RESET);
        printf(" 🎓 [審查結果]：🌲💖 %s【中央之光・資管傳奇守護者】%s 💖🌲\n", C_PAPER_HIGH, C_RESET);
        printf(" 📜 [口委評語]：%s『在其他研究生被論文折磨得不成人形時，只有你始終深愛著中大與資管系！這股正能量感動了整個管院，口委全票通過並頒發中大榮譽校友徽章！』%s\n\n", C_GREEN, C_RESET);
    }

    printf(" 🏆 [畢業證書驗證碼 Flag]：%s%s%s\n\n", C_PAPER_HIGH, decrypted, C_RESET);
    printf(" 📌 (請完整複製上方包含 NCUMIS{...} 的字串，提交至 CTFd 平台獲得分數！)\n");
    printf("==============================================================================\n\n");

    while (1) {
        printf(" 請選擇下一步行動：\n");
        printf("  [1] 重新開始一段新的碩士生涯 (Restart)\n");
        printf("  [2] 結束並退出遊戲 (Exit)\n\n");
        printf(" 請輸入選項代號 [1-2]: ");
        fflush(stdout);
        
        char buf[64];
        if (scanf("%63s", buf) != 1) continue;
        if (strcmp(buf, "1") == 0 || strcmp(buf, "r") == 0 || strcmp(buf, "R") == 0) {
            return 1; // Restart
        }
        if (strcmp(buf, "2") == 0 || strcmp(buf, "q") == 0 || strcmp(buf, "Q") == 0 || strcmp(buf, "exit") == 0) {
            printf("\n[*] 感謝遊玩！祝您在中央資管研究所研究順利、順利畢業！\n");
            fflush(stdout);
#ifdef _WIN32
            Sleep(800);
#endif
            return 0; // Exit
        }
        printf("\n[!] ⚠️ 無效輸入，請輸入 1 (重新開始) 或 2 (退出)！\n\n");
    }
}

int get_choice(int max_opt) {
    char buf[64];
    if (max_opt >= 4) {
        printf("請輸入行動代號 [1-4]: ");
    } else {
        printf("請輸入行動代號 [1-3]: ");
    }
    fflush(stdout);
    if (scanf("%63s", buf) != 1) return 0;
    
    // Convert to lowercase for reliable case-insensitive comparison
    char lower_buf[64];
    strncpy(lower_buf, buf, sizeof(lower_buf) - 1);
    lower_buf[sizeof(lower_buf) - 1] = '\0';
    to_lower_str(lower_buf);
    
    // Easter Egg 1: Debug code
    if (strcmp(lower_buf, "99") == 0 || strcmp(lower_buf, "debug") == 0 || strcmp(lower_buf, "warp") == 0) {
        return 99;
    }
    // Easter Egg 2: Root / Hacker
    if (strcmp(lower_buf, "root") == 0 || strcmp(lower_buf, "admin") == 0 || strcmp(lower_buf, "sudo") == 0 || strcmp(lower_buf, "hack") == 0) {
        return 100;
    }
    // Easter Egg 3: Central MIS Love (ilovencumis)
    if (strcmp(lower_buf, "ilovencumis") == 0 || strcmp(lower_buf, "ilovecentralmis2026") == 0 || strcmp(lower_buf, "ncu") == 0 || strcmp(lower_buf, "mis") == 0 || strcmp(lower_buf, "love") == 0) {
        return 101;
    }
    
    int c = atoi(buf);
    if (c >= 1 && c <= max_opt) return c;
    return 0;
}

int main() {
    enable_virtual_terminal();

    while (1) {
        int hp = 100;
        int stress = 0;
        int paper = 0;
        int coffee = 1;
        int choice = 0;
        int game_state = 0; // 0: running, 1: win, 2: lose, 99-101: easter eggs
        char msg[256] = "[*] 歡迎來到管二館！展開為期 12 個關鍵月份的中央資管碩士修羅場。";

        // ===== 第 1 回合：碩一上 9月 =====
        while (1) {
            render_screen(1, "碩一上 9月", hp, stress, paper, coffee, msg);
            printf("【情境：迎新與選指導教授】各大研究室都在招收新生，你打算？\n\n");
            printf(" [1] 研讀資安頂級期刊，爭取加入系上資安大老研究室 (%s論文+16%%%s, %s體力-20%s, %s壓力+10%s)\n",
                   calc_paper_color(paper, 16), C_RESET,
                   calc_hp_color(hp, -20), C_RESET,
                   calc_stress_color(stress, 10), C_RESET);
            printf(" [2] 到處打聽各教授評價，加入風氣平衡的實驗室 (%s論文+10%%%s, %s體力-10%s, %s壓力+0%s)\n",
                   calc_paper_color(paper, 10), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_stress_color(stress, 0), C_RESET);
            printf(" [3] 天天去宵夜街大吃大喝，回宿舍打電動放鬆心情 (%s體力+25%s, %s壓力-20%s, %s論文+0%%%s)\n",
                   calc_hp_color(hp, 25), C_RESET,
                   calc_stress_color(stress, -20), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { paper += 16; hp -= 20; stress += 10; snprintf(msg, sizeof(msg), "[*] 📖 研讀 20 篇頂尖論文，成功進入資安實驗室！(論文+16%%, 體力-20, 壓力+10)"); }
        else if (choice == 2) { paper += 10; hp -= 10; snprintf(msg, sizeof(msg), "[*] 💬 加入風氣自由的實驗室，穩健展開碩士生涯！(論文+10%%, 體力-10, 壓力+0)"); }
        else if (choice == 3) { hp += 25; if (hp > 100) hp = 100; stress -= 20; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 🎮 宵夜街與遊戲大滿足，身心完全充電！(體力+25, 壓力-20, 論文+0%%)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 2 回合：碩一上 10月 =====
        while (1) {
            render_screen(2, "碩一上 10月", hp, stress, paper, coffee, msg);
            printf("【情境：研究所修課海嘯】必修課與進階演算法專案排山倒海而來，你打算？\n\n");
            printf(" [1] 作業複製貼上網路現成程式碼，被助教抓包約談 (%s壓力+40%s, %s體力-10%s, %s論文+0%%%s)\n",
                   calc_stress_color(stress, 40), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            printf(" [2] 與同屆同學組讀書會分工協作完成作業 (%s論文+12%%%s, %s體力-15%s, %s壓力-5%s)\n",
                   calc_paper_color(paper, 12), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, -5), C_RESET);
            printf(" [3] 通宵單打獨鬥肝 code，力求每門課拿 A+ (%s論文+18%%%s, %s體力-30%s, %s壓力+20%s)\n",
                   calc_paper_color(paper, 18), C_RESET,
                   calc_hp_color(hp, -30), C_RESET,
                   calc_stress_color(stress, 20), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { hp -= 10; stress += 40; snprintf(msg, sizeof(msg), "[!] ⚠️ 抄襲被助教抓包，差點被送學術倫理委員會！(壓力+40, 體力-10, 論文+0%%)"); }
        else if (choice == 2) { paper += 12; hp -= 15; stress -= 5; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 🤝 讀書會分工合作順利完成作業！(論文+12%%, 體力-15, 壓力-5)"); }
        else if (choice == 3) { paper += 18; hp -= 30; stress += 20; snprintf(msg, sizeof(msg), "[*] 💻 通宵完成演算法大專案，奪得全班最高分！(論文+18%%, 體力-30, 壓力+20)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 3 回合：碩一上 12月 =====
        while (1) {
            render_screen(3, "碩一上 12月", hp, stress, paper, coffee, msg);
            printf("【情境：期末專題與研究方向確立】學期末教授在 Meeting 詢問大家的論文想法，你打算？\n\n");
            printf(" [1] 精心準備 2 個可行性高的研究方向跟教授深入討論 (%s論文+14%%%s, %s體力-15%s, %s壓力-10%s)\n",
                   calc_paper_color(paper, 14), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, -10), C_RESET);
            printf(" [2] 報告時狂畫生成式 AI 未來大餅，被教授當場痛電 (%s壓力+35%s, %s體力-10%s, %s論文+0%%%s)\n",
                   calc_stress_color(stress, 35), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            printf(" [3] 參考畢業學長題目，選擇穩健延伸的架構 (%s論文+16%%%s, %s體力-25%s, %s壓力+15%s)\n",
                   calc_paper_color(paper, 16), C_RESET,
                   calc_hp_color(hp, -25), C_RESET,
                   calc_stress_color(stress, 15), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { paper += 14; hp -= 15; stress -= 10; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 🌟 教授對你的可行題材大加讚賞，方向確定！(論文+14%%, 體力-15, 壓力-10)"); }
        else if (choice == 2) { hp -= 10; stress += 35; snprintf(msg, sizeof(msg), "[!] ❌ 教授眉頭深鎖：『這太天馬行空了，重寫！』(壓力+35, 體力-10, 論文+0%%)"); }
        else if (choice == 3) { paper += 16; hp -= 25; stress += 15; snprintf(msg, sizeof(msg), "[*] 📚 站在學長的肩膀上延伸，架構清晰！(論文+16%%, 體力-25, 壓力+15)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 4 回合：碩一下 3月 =====
        while (1) {
            render_screen(4, "碩一下 3月", hp, stress, paper, coffee, msg);
            printf("【情境：開學論文計畫書草稿】教授要求繳交一份 10 頁的論文計畫書草稿，你打算？\n\n");
            printf(" [1] 跑去百花川賞櫻發呆一整天，進度完全停滯 (%s體力+30%s, %s壓力-25%s, %s論文+0%%%s)\n",
                   calc_hp_color(hp, 30), C_RESET,
                   calc_stress_color(stress, -25), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            printf(" [2] 閉關研究室兩週，研讀 40 篇頂級文獻完成草稿 (%s論文+20%%%s, %s體力-30%s, %s壓力+20%s)\n",
                   calc_paper_color(paper, 20), C_RESET,
                   calc_hp_color(hp, -30), C_RESET,
                   calc_stress_color(stress, 20), C_RESET);
            printf(" [3] 請教畢業學長論文架構，少走許多彎路 (%s論文+14%%%s, %s體力-15%s, %s壓力-5%s)\n",
                   calc_paper_color(paper, 14), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, -5), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { hp += 30; if (hp > 100) hp = 100; stress -= 25; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 🌸 百花川風景如畫，身心舒暢但進度停滯！(體力+30, 壓力-25, 論文+0%%)"); }
        else if (choice == 2) { paper += 20; hp -= 30; stress += 20; snprintf(msg, sizeof(msg), "[*] 📑 論文計畫書架構扎實完整，審查順利過關！(論文+20%%, 體力-30, 壓力+20)"); }
        else if (choice == 3) { paper += 14; hp -= 15; stress -= 5; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 💡 學長悉心指導，架構精簡扼要！(論文+14%%, 體力-15, 壓力-5)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 5 回合：碩一下 5月 =====
        while (1) {
            render_screen(5, "碩一下 5月", hp, stress, paper, coffee, msg);
            printf("【情境：國際研討會截稿 48 小時】教授希望大家投稿國外研討會，截稿只剩 48 小時！你打算？\n\n");
            printf(" [1] 與實驗室夥伴合寫，各寫一半章節分工完稿 (%s論文+14%%%s, %s體力-15%s, %s壓力+5%s)\n",
                   calc_paper_color(paper, 14), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, 5), C_RESET);
            printf(" [2] 壓力太大躲在研究室追劇，被教授突然出現在身後撞見 (%s論文-5%%%s, %s壓力+45%s)\n",
                   calc_paper_color(paper, -5), C_RESET,
                   calc_stress_color(stress, 45), C_RESET);
            printf(" [3] 連續 48 小時不眠不休肝出滿版 Paper 壓線送出 (%s論文+22%%%s, %s體力-35%s, %s壓力+25%s)\n",
                   calc_paper_color(paper, 22), C_RESET,
                   calc_hp_color(hp, -35), C_RESET,
                   calc_stress_color(stress, 25), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { paper += 14; hp -= 15; stress += 5; snprintf(msg, sizeof(msg), "[*] 👥 雙人合力完稿，效率極高且壓力分散！(論文+14%%, 體力-15, 壓力+5)"); }
        else if (choice == 2) { paper -= 5; if (paper < 0) paper = 0; stress += 45; snprintf(msg, sizeof(msg), "[!] 😱 追劇被教授當場抓包，被痛斥論文進度落後！(論文-5%%, 壓力+45)"); }
        else if (choice == 3) { paper += 22; hp -= 35; stress += 25; snprintf(msg, sizeof(msg), "[*] 🚀 壓線送出研討會論文，研究進度大躍進！(論文+22%%, 體力-35, 壓力+25)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 6 回合：碩一下 7月 =====
        while (1) {
            render_screen(6, "碩一下 7月", hp, stress, paper, coffee, msg);
            printf("【情境：暑期全職研究生修煉】大學生都放暑假了，管二館只剩你們在通宵跑實驗，你打算？\n\n");
            printf(" [1] 參加系上產學合作專案賺取生活費 (%s獲得咖啡+1%s, %s論文+12%%%s, %s體力-15%s, %s壓力+5%s)\n",
                   C_GREEN, C_RESET,
                   calc_paper_color(paper, 12), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, 5), C_RESET);
            printf(" [2] 留在研究室搭建 GPU 深度學習環境跑模型 (%s論文+18%%%s, %s體力-25%s, %s壓力+15%s)\n",
                   calc_paper_color(paper, 18), C_RESET,
                   calc_hp_color(hp, -25), C_RESET,
                   calc_stress_color(stress, 15), C_RESET);
            printf(" [3] 回老家爽放一個月暑假補眠充電 (%s體力+35%s, %s壓力-30%s, %s論文+0%%%s)\n",
                   calc_hp_color(hp, 35), C_RESET,
                   calc_stress_color(stress, -30), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { coffee++; paper += 12; hp -= 15; stress += 5; snprintf(msg, sizeof(msg), "[*] 💼 產學合作順利完成，廠商贈送特濃黑咖啡！(獲得咖啡+1, 論文+12%%, 體力-15, 壓力+5)"); }
        else if (choice == 2) { paper += 18; hp -= 25; stress += 15; snprintf(msg, sizeof(msg), "[*] 🖥️ GPU 伺服器連續運轉一週，跑出第一批模型數據！(論文+18%%, 體力-25, 壓力+15)"); }
        else if (choice == 3) { hp += 35; if (hp > 100) hp = 100; stress -= 30; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 🏡 回家吃到媽媽做的菜，身心放鬆！(體力+35, 壓力-30, 論文+0%%)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 7 回合：碩二上 9月 =====
        while (1) {
            render_screen(7, "碩二上 9月", hp, stress, paper, coffee, msg);
            printf("【情境：碩二開學：指導教授的靈魂拷問】教授問：『大家暑假的實驗跑得如何？』你打算？\n\n");
            printf(" [1] 藉口說伺服器硬碟損壞數據遺失 (%s壓力+45%s, %s體力-10%s, %s論文+0%%%s)\n",
                   calc_stress_color(stress, 45), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            printf(" [2] 展示暑期跑出的完整 Baseline 實驗圖表 (%s論文+15%%%s, %s體力-15%s, %s壓力-10%s)\n",
                   calc_paper_color(paper, 15), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, -10), C_RESET);
            printf(" [3] 拿出初步的 Prototype Demo 給教授確認 (%s論文+10%%%s, %s體力-10%s, %s壓力+5%s)\n",
                   calc_paper_color(paper, 10), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_stress_color(stress, 5), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { hp -= 10; stress += 45; snprintf(msg, sizeof(msg), "[!] ⚡ 教授臉色鐵青：『不用找藉口，下週沒進度就延畢！』(壓力+45, 體力-10, 論文+0%%)"); }
        else if (choice == 2) { paper += 15; hp -= 15; stress -= 10; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 📊 數據詳實，教授非常滿意你的實驗進度！(論文+15%%, 體力-15, 壓力-10)"); }
        else if (choice == 3) { paper += 10; hp -= 10; stress += 5; snprintf(msg, sizeof(msg), "[*] 📱 Demo 順利展示，教授給了許多寶貴反饋！(論文+10%%, 體力-10, 壓力+5)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 8 回合：碩二上 11月 =====
        while (1) {
            render_screen(8, "碩二上 11月", hp, stress, paper, coffee, msg);
            printf("【情境：論文題目正式公開審查 (Proposal)】系辦舉辦論文公開發表會，你打算？\n\n");
            printf(" [1] 準備精美投影片與架構圖，在台上自信答辯 (%s論文+18%%%s, %s體力-25%s, %s壓力-10%s)\n",
                   calc_paper_color(paper, 18), C_RESET,
                   calc_hp_color(hp, -25), C_RESET,
                   calc_stress_color(stress, -10), C_RESET);
            printf(" [2] 請指導教授幫忙在台下護航打圓場 (%s論文+12%%%s, %s體力-15%s, %s壓力+10%s)\n",
                   calc_paper_color(paper, 12), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, 10), C_RESET);
            printf(" [3] 緊張忘詞，被評審委員大修架構 (%s論文+4%%%s, %s體力-10%s, %s壓力+40%s)\n",
                   calc_paper_color(paper, 4), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_stress_color(stress, 40), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { paper += 18; hp -= 25; stress -= 10; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 🎤 答辯流暢，評審委員一致通過開題審查！(論文+18%%, 體力-25, 壓力-10)"); }
        else if (choice == 2) { paper += 12; hp -= 15; stress += 10; snprintf(msg, sizeof(msg), "[*] 🛡️ 教授關鍵護航，有驚無險過關！(論文+12%%, 體力-15, 壓力+10)"); }
        else if (choice == 3) { paper += 4; hp -= 10; stress += 40; snprintf(msg, sizeof(msg), "[!] 😰 報告表現失常，被委員提出大量修改意見！(論文+4%%, 體力-10, 壓力+40)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 9 回合：碩二上 1月 =====
        while (1) {
            render_screen(9, "碩二上 1月", hp, stress, paper, coffee, msg);
            printf("【情境：寒假衝刺：核心模型突破】模型準確率卡在瓶頸，無法達到預期標準！你打算？\n\n");
            printf(" [1] 寒假跑去墾丁衝浪渡假，遇到失蹤學長 (%s體力+30%s, %s壓力-30%s, %s論文+0%%%s)\n",
                   calc_hp_color(hp, 30), C_RESET,
                   calc_stress_color(stress, -30), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            printf(" [2] 重新推導公式，設計全新特徵模組突破瓶頸 (%s論文+22%%%s, %s體力-30%s, %s壓力+20%s)\n",
                   calc_paper_color(paper, 22), C_RESET,
                   calc_hp_color(hp, -30), C_RESET,
                   calc_stress_color(stress, 20), C_RESET);
            printf(" [3] 調整超參數，改用多模型融合暴力搜尋 (%s論文+14%%%s, %s體力-15%s, %s壓力+10%s)\n",
                   calc_paper_color(paper, 14), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, 10), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { hp += 30; if (hp > 100) hp = 100; stress -= 30; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] 🏖️ 墾丁海風舒服，遇到失蹤學長一起衝浪！(體力+30, 壓力-30, 論文+0%%)"); }
        else if (choice == 2) { paper += 22; hp -= 30; stress += 20; snprintf(msg, sizeof(msg), "[*] 💡 公式推導成功，模型準確率突破歷史新高！(論文+22%%, 體力-30, 壓力+20)"); }
        else if (choice == 3) { paper += 14; hp -= 15; stress += 10; snprintf(msg, sizeof(msg), "[*] ⚙️ 模型融合奏效，達到口試要求標準！(論文+14%%, 體力-15, 壓力+10)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 10 回合：碩二下 3月 =====
        while (1) {
            render_screen(10, "碩二下 3月", hp, stress, paper, coffee, msg);
            printf("【情境：撰寫 80 頁完整論文初稿】畢業倒數計時！必須將研究成果撰寫成正式論文，你打算？\n\n");
            printf(" [1] 用 Google 翻譯草率應付，被教授圈滿江紅退件 (%s壓力+40%s, %s體力-10%s, %s論文+0%%%s)\n",
                   calc_stress_color(stress, 40), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            printf(" [2] 請英文流利的同學幫忙校稿與潤飾寫作 (%s論文+16%%%s, %s體力-15%s, %s壓力-10%s)\n",
                   calc_paper_color(paper, 16), C_RESET,
                   calc_hp_color(hp, -15), C_RESET,
                   calc_stress_color(stress, -10), C_RESET);
            printf(" [3] 每天在管二館寫 15 頁 LaTeX 狂肝論文初稿 (%s論文+20%%%s, %s體力-30%s, %s壓力+20%s)\n",
                   calc_paper_color(paper, 20), C_RESET,
                   calc_hp_color(hp, -30), C_RESET,
                   calc_stress_color(stress, 20), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { hp -= 10; stress += 40; snprintf(msg, sizeof(msg), "[!] ⚠️ 機器翻譯語句不通順，被教授全篇退件重寫！(壓力+40, 體力-10, 論文+0%%)"); }
        else if (choice == 2) { paper += 16; hp -= 15; stress -= 10; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] ✍️ 同門精心潤飾，論文架構無懈可擊！(論文+16%%, 體力-15, 壓力-10)"); }
        else if (choice == 3) { paper += 20; hp -= 30; stress += 20; snprintf(msg, sizeof(msg), "[*] 📝 80 頁 LaTeX 排版精美，完整論文初稿出爐！(論文+20%%, 體力-30, 壓力+20)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 11 回合：碩二下 5月 =====
        while (1) {
            render_screen(11, "碩二下 5月", hp, stress, paper, coffee, msg);
            printf("【情境：論文口試預演 (Mock Defense)】指導教授安排實驗室內部預演挑毛病，你打算？\n\n");
            printf(" [1] 請同學喝特濃咖啡拜託手下留情 (%s獲得咖啡+1%s, %s論文+10%%%s, %s體力+15%s, %s壓力-15%s)\n",
                   C_GREEN, C_RESET,
                   calc_paper_color(paper, 10), C_RESET,
                   calc_hp_color(hp, 15), C_RESET,
                   calc_stress_color(stress, -15), C_RESET);
            printf(" [2] 虛心接受所有批評，連夜將實驗與論文修改完美 (%s論文+16%%%s, %s體力-20%s, %s壓力+10%s)\n",
                   calc_paper_color(paper, 16), C_RESET,
                   calc_hp_color(hp, -20), C_RESET,
                   calc_stress_color(stress, 10), C_RESET);
            printf(" [3] 當場跟教授爭辯實驗設計，場面陷入冰點 (%s壓力+45%s, %s體力-10%s, %s論文+0%%%s)\n",
                   calc_stress_color(stress, 45), C_RESET,
                   calc_hp_color(hp, -10), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { coffee++; paper += 10; hp += 15; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0; snprintf(msg, sizeof(msg), "[*] ☕ 同學們深受感動，回贈你一罐最後衝刺的特濃黑咖啡！(獲得咖啡+1, 論文+10%%, 體力+15, 壓力-15)"); }
        else if (choice == 2) { paper += 16; hp -= 20; stress += 10; snprintf(msg, sizeof(msg), "[*] ✨ 將預演所有盲點修正完畢，萬事俱備！(論文+16%%, 體力-20, 壓力+10)"); }
        else if (choice == 3) { hp -= 10; stress += 45; snprintf(msg, sizeof(msg), "[!] ⚡ 場面降至冰點，口試前夕壓力爆棚！(壓力+45, 體力-10, 論文+0%%)"); }
        if (hp <= 0) { if (show_settlement(0, "你在研究室體力透支昏倒，醒來發現被辦了休學手續...", hp, stress, paper)) continue; else break; }
        if (stress >= 100) { if (show_settlement(0, "壓力值破表，心態崩潰決定退學去墾丁衝浪跟失蹤學長會合...", hp, stress, paper)) continue; else break; }

        // ===== 第 12 回合：碩二下 7月 (Final Defense) =====
        while (1) {
            render_screen(12, "碩二下 7月", hp, stress, paper, coffee, msg);
            printf("【情境：碩士論文最終口試 (Final Defense)】三位口試委員就座，你深吸一口氣開始報告...\n\n");
            printf(" [1] 緊張結巴一直看手錶，勉強講完簡報 (%s論文+2%%%s, %s壓力+25%s)\n",
                   calc_paper_color(paper, 2), C_RESET,
                   calc_stress_color(stress, 25), C_RESET);
            printf(" [2] 從容自信專業發表兩年來扎實的研究成果！ (%s論文+15%%%s, %s壓力-20%s)\n",
                   calc_paper_color(paper, 15), C_RESET,
                   calc_stress_color(stress, -20), C_RESET);
            printf(" [3] 搬出指導教授名號瘋狂拍口委馬屁 (%s壓力+40%s, %s論文+0%%%s)\n",
                   calc_stress_color(stress, 40), C_RESET,
                   calc_paper_color(paper, 0), C_RESET);
            if (coffee > 0) {
                printf(" [4] 喝掉庫存的【特濃黑咖啡】 (%s體力立即+35%s, %s壓力-15%s)\n",
                       calc_hp_color(hp, 35), C_RESET,
                       calc_stress_color(stress, -15), C_RESET);
            }
            printf("\n");
            choice = get_choice(coffee > 0 ? 4 : 3);
            if (choice >= 99 && choice <= 101) { game_state = choice; break; }
            if (choice == 4) {
                if (coffee > 0) {
                    coffee--; hp += 35; if (hp > 100) hp = 100; stress -= 15; if (stress < 0) stress = 0;
                    snprintf(msg, sizeof(msg), "[*] ☕ 咕嚕咕嚕... 喝下特濃黑咖啡！體力+35，壓力-15！");
                }
                continue;
            }
            if (choice >= 1 && choice <= 3) break;
            snprintf(msg, sizeof(msg), "[!] ⚠️ 請輸入有效選項 [1-%d]！", coffee > 0 ? 4 : 3);
        }
        if (game_state >= 99 && game_state <= 101) { if (show_easter_egg(game_state)) continue; else break; }
        if (choice == 1) { paper += 2; stress += 25; }
        else if (choice == 2) { paper += 15; stress -= 20; if (stress < 0) stress = 0; }
        else if (choice == 3) { stress += 40; }

        if (paper >= 100 && hp > 0 && stress < 100) {
            if (show_settlement(1, "口試通過", hp, stress, paper)) continue;
            else break;
        } else {
            char fail_reason[128];
            snprintf(fail_reason, sizeof(fail_reason), "總論文進度僅達 %d%% (需達 100%% 以上)，口試委員一致建議延畢再戰！", paper);
            if (show_settlement(0, fail_reason, hp, stress, paper)) continue;
            else break;
        }
    }

    return 0;
}
