import urllib.request
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os

GMAIL_USER = os.environ.get("GMAIL_USER", "g1014308@gmail.com")
GMAIL_APP_PASS = os.environ.get("GMAIL_APP_PASS", "")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "g1014308@gmail.com")

LOG_FILE = "/home/ubuntu/ctf_email_results.log"


def log(msg):
    now = datetime.datetime.now().isoformat()
    line = f"[{now}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch_top10_users():
    import subprocess

    cmd = [
        "docker",
        "exec",
        "ctfd-db-1",
        "mysql",
        "-uctfd",
        "-pctfd",
        "ctfd",
        "-e",
        "SELECT id, name, email FROM users WHERE banned = 0 AND hidden = 0;",
    ]
    res = subprocess.run(  # skipcq: BAN-B603, BAN-B607 # nosec
        cmd, shell=False, capture_output=True, text=True, check=False
    )
    users_by_id = {}
    users_by_name = {}
    for line in res.stdout.strip().splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 3:
            uid, uname, uemail = parts[0].strip(), parts[1].strip(), parts[2].strip()
            users_by_id[uid] = uemail
            users_by_name[uname] = uemail

    url = "https://im2026ctf.duckdns.org/api/v1/scoreboard"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    top_list = []
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("data", [])[:10]:
                name = item["name"]
                pos = item["pos"]
                score = item["score"]
                account_id = str(item.get("account_id", ""))
                email = users_by_id.get(account_id) or users_by_name.get(name)
                top_list.append(
                    {"rank": pos, "name": name, "score": score, "email": email}
                )
    except Exception as e:
        log(f"Error fetching scoreboard via API: {e}")
    return top_list


def create_email_html(name, rank):
    return f"""\
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{
      margin: 0;
      padding: 12px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #f8fafc;
      color: #1e293b;
      -webkit-text-size-adjust: 100%;
    }}
    .card {{
      max-width: 480px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      overflow: hidden;
    }}
    .header {{
      background: #1e3a8a;
      padding: 20px 16px;
      text-align: center;
      color: #ffffff;
    }}
    .header h1 {{
      margin: 0;
      font-size: 19px;
      font-weight: 700;
    }}
    .content {{
      padding: 20px 16px;
      font-size: 15px;
      line-height: 1.6;
    }}
    .intro {{
      margin-bottom: 16px;
    }}
    .box {{
      background: #f1f5f9;
      border-radius: 8px;
      padding: 14px;
      margin: 16px 0;
    }}
    .item {{
      margin-bottom: 8px;
    }}
    .item:last-child {{
      margin-bottom: 0;
    }}
    .label {{
      font-weight: 700;
      color: #0f172a;
    }}
    .footer {{
      padding: 14px 16px;
      text-align: center;
      font-size: 12px;
      color: #64748b;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>🎉 Mini-CTF 恭喜破關 ☕</h1>
    </div>
    <div class="content">
      <div class="intro">
        <strong>{name}</strong> 同學你好：<br><br>
        恭喜你在本次 Mini-CTF 資安破冰賽榮登 <strong>TOP 10（第 {rank} 名）</strong>！獲得星巴克飲料券獎勵。
      </div>

      <div class="box">
        <div class="item">
          <span class="label">📍 時間：</span>9/15（二）企業電腦網路下課時
        </div>
        <div class="item">
          <span class="label">🏢 地點：</span>課堂現場找助教
        </div>
        <div class="item">
          <span class="label">🔖 憑證：</span>出示 CTF 登入畫面或學生證
        </div>
      </div>

      <div style="font-size: 14px; color: #475569;">
        感謝你的熱情參與，下週二課堂見！
      </div>
    </div>
    <div class="footer">
      <strong>NCU 網安實驗室 | CYberMaw</strong><br>
      國立中央大學 資訊管理學系
    </div>
  </div>
</body>
</html>
"""


def main():
    log("=== Starting Final Contest Top 10 Email Dispatch ===")
    winners = fetch_top10_users()
    if not winners:
        log("No winners found! Aborting.")
        return

    log(f"Found {len(winners)} winners.")

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(GMAIL_USER, GMAIL_APP_PASS)

    sent_summary = []

    for w in winners:
        rank = w["rank"]
        name = w["name"]
        email = w["email"]
        score = w["score"]

        if not email:
            log(f"Warning: No email for {name} (Rank {rank})")
            sent_summary.append(f"❌ Rank {rank}: {name} ({score} 分) - 無 Email")
            continue

        subject = "【中央資管 Mini-CTF】恭喜破關！榮登 TOP 10 ☕"
        html = create_email_html(name, rank)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"NCU 網安實驗室 | CYberMaw <{GMAIL_USER}>"
        msg["To"] = email
        msg.attach(MIMEText(html, "html", "utf-8"))

        try:
            server.sendmail(GMAIL_USER, [email], msg.as_string())
            log(f"Sent email to {name} <{email}> (Rank {rank})")
            sent_summary.append(f"✅ Rank {rank}: {name} ({score} 分) -> {email}")
        except Exception as e:
            log(f"Failed to send to {email}: {e}")
            sent_summary.append(
                f"❌ Rank {rank}: {name} ({score} 分) -> {email} (Error: {e})"
            )

    # Send admin report email
    admin_sub = "【CTF 結算報告】前十名得獎信件發送完畢"
    admin_body = "Hi 助教 / 主辦人：\n\nMini-CTF 賽事已於 9/10 10:00 正式結束！\n以下為系統自動結算並發送信件之結果：\n\n"
    admin_body += "\n".join(sent_summary)
    admin_body += "\n\n得獎同學憑證領取時間：9/15（二）企業電腦網路下課時\n\nNCU 網安實驗室 | CYberMaw 自動化排程系統"

    admin_msg = MIMEText(admin_body, "plain", "utf-8")
    admin_msg["Subject"] = admin_sub
    admin_msg["From"] = f"NCU 網安實驗室 | CYberMaw <{GMAIL_USER}>"
    admin_msg["To"] = ADMIN_EMAIL

    try:
        server.sendmail(GMAIL_USER, [ADMIN_EMAIL], admin_msg.as_string())
        log("Admin summary email sent.")
    except Exception as e:
        log(f"Failed to send admin summary: {e}")

    server.quit()
    log("=== Email Dispatch Completed ===")


if __name__ == "__main__":
    main()
