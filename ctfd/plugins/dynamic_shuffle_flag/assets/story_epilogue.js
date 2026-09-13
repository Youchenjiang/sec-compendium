(function () {
    "use strict";

    // ===== 全局 ECharts 圖表正體中文客製化 =====
    window.scoreboardChartOptions = {
        toolbox: {
            feature: {
                dataZoom: {
                    title: {
                        zoom: "區域縮放",
                        back: "區域縮放還原"
                    }
                },
                saveAsImage: {
                    title: "儲存為圖片",
                    lang: ["右鍵另存為圖片"]
                }
            }
        }
    };

    // ===== 劇情結局資料庫 =====
    const EPILOGUES = [
        {
            id: 37,
            keywords: ["歡迎", "welcome", "簽到"],
            title: "🌟【入學啟程：中央資管大家庭】",
            story: "恭喜你完成簽到！在未來的兩年裡，有學長姐與老師們陪伴你們一起探索學術與技術的精彩世界。歡迎加入中央資管大家庭！"
        },
        {
            id: 38,
            keywords: ["目擊", "照片", "osint", "campus", "kenting", "墾丁", "exif"],
            title: "🏖️【結局爆料：全網通緝叛逃學長】",
            story: "恭喜你從照片 EXIF 找到了學長在墾丁衝浪的自白！<br><br>系辦助教看到你的通報後震怒：<br><strong style='color:#ff7b72'>「難怪學長剛剛在 IG 發海邊打卡限動！立刻打電話叫他下週一早上 8 點回來報告 Paper！」</strong><br><br><em style='color:#8b949e'>（你成功阻止了一起研究生叛逃事件）</em>"
        },
        {
            id: 39,
            keywords: ["屎山", "代碼", "f12", "trash", "註解", "原始碼", "cookie"],
            title: "💥【結局爆料：實驗室伺服器危機】",
            story: "恭喜你拼湊出學長十年前寫在註解裡的自白：<code>do_not_touch_this_trash</code>！<br><br>但因為你剛才在 F12 裡不小心刪了一行註解，實驗室的主機風扇突然開始狂轉冒煙……<br><strong style='color:#d29922'>「快關掉瀏覽器裝作什麼事都沒發生！」</strong>"
        },
        {
            id: 40,
            keywords: ["加簽", "加選", "crypto", "密碼學", "caesar", "授權碼"],
            title: "🎓【結局爆料：加簽的殘酷真相】",
            story: "恭喜你成功解出加選授權碼！<br><br>正當你興高采烈衝去系辦要送出時，助教突然拍了拍你的肩膀：<br><strong style='color:#58a6ff'>「同學……教授剛剛走出辦公室宣佈，因為教室容納不下，這門課今年不開了……」</strong><br><br><em style='color:#8b949e'>（新生崩潰：那我剛才算凱撒密碼到底在忙什麼？！）</em>"
        },
        {
            id: 41,
            keywords: ["出席", "成績", "sqli", "咪挺", "injection", "萬能密碼"],
            title: "🏆【結局爆料：拯救全班的無名英雄】",
            story: "恭喜你用萬能密碼 <code>' OR 1=1 --</code> 成功潛入出席系統！<br><br>你順手把這學期全體研一新生的出席率改成了 100 分。教授隨後在 Line 大群廣播：<br><strong style='color:#3fb950'>「看在大家這學期全勤的份上，期末報告全部免試！」</strong><br><br><em style='color:#8b949e'>（你成為了拯救全班的無名英雄）</em>"
        },
        {
            id: 42,
            keywords: ["貓", "論文", "forensics", "cat", "steg", "隱寫", "innocent"],
            title: "🐱【結局爆料：這隻貓咪要來咪挺了】",
            story: "恭喜你剖開圖片提取出學長「其實連 Abstract 都沒寫」的自白！<br><br>教授看完這份自白檔案後默默把貓咪抱到椅子上：<br><strong style='color:#bc8cff'>「這隻貓咪看起來比學長誠實，下週開始由這隻貓代替學長來 Meeting 報告。」</strong>"
        },
        {
            id: 43,
            keywords: ["生存", "模擬", "審查", "畢業", "graduation", "reverse", "逆向", "binary"],
            title: "🎓【結局爆料：恭喜碩士順利登頂】",
            story: "恭喜你成功通關資管碩士生涯模擬器！<br><br>不論你是靠神乎其技的時間管理能力，還是靠強大的逆向分析實力通關，系主任都對你的實力深感佩服：<br><strong style='color:#3fb950'>「這位同學兼具頂尖的資安實力與超強抗壓性，下週開始由你擔任研究室大組長！」</strong>"
        }
    ];

    function getEpilogue(chalName, chalId) {
        // 1. 優先以 ID 精確對應
        if (chalId) {
            const byId = EPILOGUES.find(e => e.id === parseInt(chalId));
            if (byId) return byId;
        }

        // 2. 備援以關鍵字無衝突比對
        const lower = (chalName || "").toLowerCase();
        for (const e of EPILOGUES) {
            if (e.keywords.some(k => lower.includes(k.toLowerCase()))) return e;
        }
        return { title: "🎉【解題成功！】", story: "恭喜你成功解開這道題目！<br>繼續加油，研究生地獄還有更多關卡等著你！" };
    }

    function showModal(epilogue) {
        if (!epilogue) return;

        // 移除任何殘留彈窗
        const old = document.getElementById("ncumis-epilogue");
        if (old) old.remove();

        const el = document.createElement("div");
        el.id = "ncumis-epilogue";
        el.style.cssText = [
            "position:fixed", "inset:0", "z-index:999999",
            "background:rgba(0,0,0,.82)", "backdrop-filter:blur(5px)",
            "display:flex", "align-items:center", "justify-content:center",
            "padding:16px"
        ].join(";");

        el.innerHTML = `
          <div style="background:#161b22;border:2px solid #58a6ff;border-radius:14px;
               max-width:560px;width:100%;padding:28px;
               box-shadow:0 16px 48px rgba(0,100,255,.4);
               color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
            <div style="font-size:1.25rem;font-weight:700;color:#58a6ff;
                 border-bottom:1px solid #30363d;padding-bottom:10px;margin-bottom:16px;
                 display:flex;justify-content:space-between;align-items:center;">
              <span>${epilogue.title}</span>
              <button id="ncumis-close" style="background:none;border:none;
                color:#8b949e;font-size:1.6rem;cursor:pointer;line-height:1;padding:0 4px">&times;</button>
            </div>
            <div style="font-size:1rem;line-height:1.8;color:#e6edf3;margin-bottom:22px;">
              ${epilogue.story}
            </div>
            <div style="text-align:right">
              <button id="ncumis-ok"
                style="background:#238636;color:#fff;border:1px solid rgba(240,246,252,.1);
                  padding:9px 22px;border-radius:6px;font-weight:700;cursor:pointer;font-size:1rem;">
                太棒了！繼續闖關 🚀
              </button>
            </div>
          </div>`;

        document.body.appendChild(el);

        const close = () => { const m = document.getElementById("ncumis-epilogue"); if (m) m.remove(); };
        document.getElementById("ncumis-close").addEventListener("click", close, { once: true });
        document.getElementById("ncumis-ok").addEventListener("click", close, { once: true });
        el.addEventListener("click", (ev) => { if (ev.target === el) close(); });
    }

    // ===== 取得當前題目名稱與 ID =====
    function getChalName() {
        const el = document.querySelector(".challenge-name");
        return el ? el.innerText.trim() : "";
    }

    function getChalId() {
        const el = document.querySelector("#challenge-id") || document.querySelector(".challenge-id") || document.querySelector("input[name='challenge_id']");
        return el ? parseInt(el.value) : null;
    }

    // ===== 方法一：Hook CTFd.pages.challenge.submitChallenge =====
    let hooked = false;
    let hookAttempts = 0;

    function tryHook() {
        if (hooked || hookAttempts++ > 150) return; // 15 秒超時

        const fn = window.CTFd &&
                   window.CTFd.pages &&
                   window.CTFd.pages.challenge &&
                   window.CTFd.pages.challenge.submitChallenge;

        if (typeof fn !== "function") {
            setTimeout(tryHook, 100);
            return;
        }

        const original = window.CTFd.pages.challenge.submitChallenge;
        window.CTFd.pages.challenge.submitChallenge = async function (chalId, submission) {
            const result = await original.call(this, chalId, submission);
            try {
                if (result && result.data && result.data.status === "correct") {
                    const name = getChalName();
                    setTimeout(() => showModal(getEpilogue(name, chalId)), 500);
                }
            } catch (e) {}
            return result;
        };

        hooked = true;
        console.log("[NCUMIS] submitChallenge hook ok");
    }

    // ===== 方法二：MutationObserver 備援（觀察 class 屬性變化） =====
    let lastShown = 0;

    const observer = new MutationObserver((mutations) => {
        if (hooked) return; // 已有 CTFd hook，跳過
        for (const m of mutations) {
            if (m.type === "attributes" && m.attributeName === "class" &&
                m.target.classList && m.target.classList.contains("alert-success")) {
                if (Date.now() - lastShown < 2000) return;
                lastShown = Date.now();
                const name = getChalName();
                const id = getChalId();
                setTimeout(() => showModal(getEpilogue(name, id)), 500);
                return;
            }
            if (m.type === "childList") {
                for (const node of m.addedNodes) {
                    if (node.nodeType !== 1) continue;
                    const hit = (node.classList && node.classList.contains("alert-success")) ||
                                (node.querySelector && node.querySelector(".alert-success"));
                    if (hit) {
                        if (Date.now() - lastShown < 2000) return;
                        lastShown = Date.now();
                        const name = getChalName();
                        const id = getChalId();
                        setTimeout(() => showModal(getEpilogue(name, id)), 500);
                        return;
                    }
                }
            }
        }
    });

    // ===== 啟動 =====
    function init() {
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ["class"]
        });
        tryHook();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

})();
