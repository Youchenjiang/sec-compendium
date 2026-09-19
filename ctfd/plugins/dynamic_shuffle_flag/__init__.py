import base64
import hashlib
import io
import os
import random
import zipfile
from urllib.parse import quote

import piexif
import redis
from CTFd.plugins import (
    bypass_csrf_protection,
    register_plugin_assets_directory,
    register_plugin_script,
)
from CTFd.plugins.flags import FLAG_CLASSES, BaseFlag
from CTFd.utils.user import authed, get_current_team, get_current_user
from flask import (
    Blueprint,
    Response,
    jsonify,
    make_response,
    render_template_string,
    request,
    send_from_directory,
    session,
)
from PIL import Image

FLAG_SALT = os.environ.get("CTFD_FLAG_SALT", "ncu_mis_flag_salt_2026")


PLUGIN_DIR = os.path.dirname(__file__)


ASSETS_DIR = os.path.join(PLUGIN_DIR, "assets")


def generate_dynamic_flag(base_flag_text, team_name):

    inner = base_flag_text.strip()

    if inner.startswith("NCUMIS{") and inner.endswith("}"):
        inner = inner[7:-1]

    clean_team = team_name.strip()

    if not clean_team:
        clean_team = "challenger"

    seed_str = f"{FLAG_SALT}:{clean_team}:{inner}"

    seed = int(hashlib.sha256(seed_str.encode("utf-8")).hexdigest(), 16)

    rng = random.Random(seed)

    n = len(clean_team)

    if n <= 2:
        chars_to_insert = list(clean_team)

    else:
        front_cnt = rng.randint(1, min(2, n - 1))  # NOSONAR

        back_cnt = rng.randint(1, min(2, n - front_cnt))  # NOSONAR

        front_chars = list(clean_team[:front_cnt])

        back_chars = list(clean_team[-back_cnt:])

        chars_to_insert = front_chars + back_chars

    rng.shuffle(chars_to_insert)  # NOSONAR

    flag_chars = list(inner)

    for ch in chars_to_insert:
        pos = rng.randint(0, len(flag_chars))  # NOSONAR

        flag_chars.insert(pos, ch)

    shuffled_body = "".join(flag_chars)

    return f"NCUMIS{{{shuffled_body}}}"


def get_current_player_name():

    team = get_current_team()

    if team:
        return team.name.strip()

    user = get_current_user()

    if user:
        return user.name.strip()

    return request.args.get("team", "").strip() or "challenger"


labs_bp = Blueprint("ncu_labs", __name__)


@labs_bp.before_request
def require_login_for_labs():
    if request.path.startswith("/labs/assets/") or "/visits" in request.path:
        return None
    if not authed():
        next_url = request.url
        login_url = f"/login?next={quote(next_url)}"
        register_url = "/register"
        return render_template_string(
            """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8">
  <title>請先登入 | 2026 中央資管 Mini-CTF</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/svg+xml" href="/files/6dc8cc9b0fe2eab996884f3a566129aa/favicon.svg">
  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body {
      background-color: #0b0f19;
      background-image: 
        radial-gradient(circle at 15% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(16, 185, 129, 0.15) 0%, transparent 40%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      color: #f8fafc;
    }
    .auth-card {
      background: rgba(18, 26, 44, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-radius: 20px;
      padding: 40px 32px;
      max-width: 480px;
      width: 100%;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 40px rgba(59, 130, 246, 0.1);
    }
    .icon { font-size: 42px; margin-bottom: 16px; }
    h2 { font-size: 22px; font-weight: 700; margin-bottom: 12px; color: #ffffff; }
    p { color: #94a3b8; font-size: 14.5px; line-height: 1.6; margin-bottom: 26px; }
    .btn-group { display: flex; gap: 12px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
    .btn-primary {
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      color: #ffffff;
      padding: 10px 24px;
      border-radius: 10px;
      text-decoration: none;
      font-weight: 600;
      font-size: 14.5px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.35);
    }
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
      background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }
    .btn-outline {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #e2e8f0;
      padding: 10px 22px;
      border-radius: 10px;
      text-decoration: none;
      font-weight: 600;
      font-size: 14.5px;
      transition: all 0.2s ease;
    }
    .btn-outline:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
    }
    .back-link { color: #64748b; font-size: 13.5px; text-decoration: none; transition: color 0.2s; }
    .back-link:hover { color: #94a3b8; }
  </style>
</head>
<body>
  <div class="auth-card">
    <div class="icon">🔒</div>
    <h2>需要登入才能下載題目素材</h2>
    <p>
      為確保每位挑戰者獲取專屬的<strong>個人動態解題檔案與 Flag</strong>，請先登入或註冊帳號再進行下載！
    </p>
    <div class="btn-group">
      <a href="{{ login_url }}" class="btn-primary">立即登入</a>
      <a href="{{ register_url }}" class="btn-outline">註冊新帳號</a>
    </div>
    <div>
      <a href="/challenges" class="back-link">&larr; 返回題目列表</a>
    </div>
  </div>
</body>
</html>""",
            login_url=login_url,
            register_url=register_url,
        )


@labs_bp.route("/labs/assets/<path:filename>")
def serve_lab_asset(filename):

    return send_from_directory(ASSETS_DIR, filename)


@labs_bp.route("/download/campus")
def download_campus():

    team_name = get_current_player_name()

    dynamic_flag = generate_dynamic_flag("senior_fled_to_kenting", team_name)

    src_img = os.path.join(ASSETS_DIR, "campus.jpg")

    if not os.path.exists(src_img):
        src_img = os.path.join(ASSETS_DIR, "base_campus.jpg")

    im = Image.open(src_img)

    # UTF-16LE encoding: Visible in Windows Explorer "詳細資料" (Details Tab)

    # but invisible to plain text search in Notepad++ due to UTF-16LE null bytes between characters!

    xp_bytes = dynamic_flag.encode("utf-16le")

    exif_dict = {
        "0th": {
            0x9C9C: xp_bytes,  # XPComment -> Windows Details: 備註
            0x9C9F: "交接實驗室設備".encode(
                "utf-16le"
            ),  # XPSubject -> Windows Details: 主旨
            0x9C9B: "學長逃跑現場".encode(
                "utf-16le"
            ),  # XPTitle -> Windows Details: 標題
            piexif.ImageIFD.Artist: f"Senior in Kenting for {team_name}".encode(
                "utf-8"
            ),
            piexif.ImageIFD.Software: "NCUMIS Camera".encode("utf-8"),
        },
        "Exif": {},
        "GPS": {
            piexif.GPSIFD.GPSLatitudeRef: "N",
            piexif.GPSIFD.GPSLatitude: ((21, 1), (56, 1), (53, 1)),
            piexif.GPSIFD.GPSLongitudeRef: "E",
            piexif.GPSIFD.GPSLongitude: ((120, 1), (46, 1), (47, 1)),
        },
        "1st": {},
        "thumbnail": None,
    }

    exif_bytes = piexif.dump(exif_dict)

    buf = io.BytesIO()

    im.save(buf, "jpeg", exif=exif_bytes)

    buf.seek(0)

    filename = f"disappeared_senior_for_{team_name}.jpg"

    encoded_name = quote(filename)

    resp = Response(buf.read(), mimetype="image/jpeg")

    resp.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_name}"

    return resp


@labs_bp.route("/download/cat")
def download_cat():

    team_name = get_current_player_name()

    dynamic_flag = generate_dynamic_flag("the_cat_is_innocent", team_name)

    src_img = os.path.join(ASSETS_DIR, "cat.jpg")

    if not os.path.exists(src_img):
        src_img = os.path.join(ASSETS_DIR, "base_cat.jpg")

    with open(src_img, "rb") as f:
        raw_cat = f.read()

    eof_idx = raw_cat.rfind(b"\xff\xd9")

    if eof_idx != -1:
        raw_cat = raw_cat[: eof_idx + 2]

    zip_buf = io.BytesIO()

    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("eaten_thesis.txt", f"{dynamic_flag}\n")

    final_bytes = raw_cat + zip_buf.getvalue()

    filename = f"cat_ate_my_thesis_for_{team_name}.jpg"

    encoded_name = quote(filename)

    resp = Response(final_bytes, mimetype="image/jpeg")

    resp.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_name}"

    return resp


@labs_bp.route("/download/check_graduation.exe")
def download_check_graduation_exe():

    team_name = get_current_player_name()

    dynamic_flag = generate_dynamic_flag("graduation_is_a_lie", team_name)

    exe_path = os.path.join(ASSETS_DIR, "base_check_graduation.exe")

    if not os.path.exists(exe_path):
        return "Binary not found", 404

    with open(exe_path, "rb") as f:
        content = f.read()

    target_placeholder = bytes(
        [
            0x14,
            0x19,
            0x0F,
            0x17,
            0x13,
            0x09,
            0x21,
            0x3D,
            0x28,
            0x3B,
            0x3E,
            0x2F,
            0x3B,
            0x2E,
            0x33,
            0x35,
            0x34,
            0x05,
            0x33,
            0x29,
            0x05,
            0x3B,
            0x05,
            0x36,
            0x33,
            0x3F,
            0x05,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x27,
        ]
    )

    new_flag_bytes = bytes([b ^ 0x5A for b in dynamic_flag.encode("utf-8")])

    if len(new_flag_bytes) < len(target_placeholder):
        new_flag_bytes = new_flag_bytes + bytes([0]) * (
            len(target_placeholder) - len(new_flag_bytes)
        )

    elif len(new_flag_bytes) > len(target_placeholder):
        new_flag_bytes = new_flag_bytes[: len(target_placeholder)]

    final_bin = content.replace(target_placeholder, new_flag_bytes)

    filename = f"mis_survival_game_for_{team_name}.exe"

    encoded_name = quote(filename)

    resp = Response(final_bin, mimetype="application/vnd.microsoft.portable-executable")

    resp.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_name}"

    return resp


@labs_bp.route("/download/check_graduation_mac")
def download_check_graduation_mac():
    team_name = get_current_player_name()
    dynamic_flag = generate_dynamic_flag("graduation_is_a_lie", team_name)

    mac_path = os.path.join(ASSETS_DIR, "base_check_graduation_mac")
    if not os.path.exists(mac_path):
        return "Binary not found", 404

    with open(mac_path, "rb") as f:
        content = f.read()

    target_placeholder = bytes(
        [
            0x14,
            0x19,
            0x0F,
            0x17,
            0x13,
            0x09,
            0x21,
            0x3D,
            0x28,
            0x3B,
            0x3E,
            0x2F,
            0x3B,
            0x2E,
            0x33,
            0x35,
            0x34,
            0x05,
            0x33,
            0x29,
            0x05,
            0x3B,
            0x05,
            0x36,
            0x33,
            0x3F,
            0x05,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x27,
        ]
    )
    new_flag_bytes = bytes([b ^ 0x5A for b in dynamic_flag.encode("utf-8")])
    if len(new_flag_bytes) < len(target_placeholder):
        new_flag_bytes = new_flag_bytes + bytes([0]) * (
            len(target_placeholder) - len(new_flag_bytes)
        )
    elif len(new_flag_bytes) > len(target_placeholder):
        new_flag_bytes = new_flag_bytes[: len(target_placeholder)]

    final_bin = content.replace(target_placeholder, new_flag_bytes)

    filename = f"mis_survival_game_for_{team_name}_mac"
    encoded_name = quote(filename)
    resp = make_response(final_bin)
    resp.headers["Content-Type"] = "application/octet-stream"
    resp.headers["Content-Disposition"] = (
        f"attachment; filename={filename}; filename*=UTF-8''{encoded_name}"
    )
    return resp


@labs_bp.route("/download/check_graduation")
def download_check_graduation():

    team_name = get_current_player_name()

    dynamic_flag = generate_dynamic_flag("graduation_is_a_lie", team_name)

    elf_path = os.path.join(ASSETS_DIR, "base_check_graduation")

    if not os.path.exists(elf_path):
        return "Binary not found", 404

    with open(elf_path, "rb") as f:
        content = f.read()

    target_placeholder = bytes(
        [
            0x14,
            0x19,
            0x0F,
            0x17,
            0x13,
            0x09,
            0x21,
            0x3D,
            0x28,
            0x3B,
            0x3E,
            0x2F,
            0x3B,
            0x2E,
            0x33,
            0x35,
            0x34,
            0x05,
            0x33,
            0x29,
            0x05,
            0x3B,
            0x05,
            0x36,
            0x33,
            0x3F,
            0x05,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x22,
            0x27,
        ]
    )

    new_flag_bytes = bytes([b ^ 0x5A for b in dynamic_flag.encode("utf-8")])

    if len(new_flag_bytes) < len(target_placeholder):
        new_flag_bytes = new_flag_bytes + bytes([0]) * (
            len(target_placeholder) - len(new_flag_bytes)
        )

    elif len(new_flag_bytes) > len(target_placeholder):
        new_flag_bytes = new_flag_bytes[: len(target_placeholder)]

    final_bin = content.replace(target_placeholder, new_flag_bytes)

    filename = f"mis_survival_game_for_{team_name}"

    encoded_name = quote(filename)

    resp = Response(final_bin, mimetype="application/octet-stream")

    resp.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_name}"

    return resp


@labs_bp.route("/labs/f12")
def lab_f12():

    team_name = get_current_player_name()

    full_flag = generate_dynamic_flag("do_not_touch_this_trash", team_name)

    mid = len(full_flag) // 2

    part1 = full_flag[:mid]

    part2 = full_flag[mid:]

    html = f"""<!DOCTYPE html>


<html>


<head>


    <meta charset="utf-8">


    <title>Web 挑戰：學長留下的屎山代碼</title>


    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">


    <style>


        body {{


            background: #0d1117 url("/labs/assets/server_room.jpg") no-repeat center center fixed;


            background-size: cover;


            color: #c9d1d9;


            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;


            display: flex;


            align-items: center;


            justify-content: center;


            min-height: 100vh;


            margin: 0;


        }}


        .overlay {{


            position: fixed; top: 0; left: 0; right: 0; bottom: 0;


            background: rgba(13, 17, 23, 0.85);


            backdrop-filter: blur(4px);


            z-index: 1;


        }}


        .card {{


            position: relative; z-index: 2;


            background: rgba(22, 27, 34, 0.95);


            border: 1px solid #ff7b72;


            border-radius: 12px;


            max-width: 680px; width: 90%;


            box-shadow: 0 12px 36px rgba(255, 100, 100, 0.2);


        }}


        .highlight {{ color: #58a6ff; font-weight: bold; }}


        .terminal-header {{


            background: #090d13;


            padding: 10px 18px;


            border-top-left-radius: 11px;


            border-top-right-radius: 11px;


            border-bottom: 1px solid #30363d;


            display: flex;


            align-items: center;


        }}


        .circle {{ width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }}


        .c-red {{ background: #ff5f56; }} .c-yellow {{ background: #ffbd2e; }} .c-green {{ background: #27c93f; }}


    </style>


</head>


<body>


    <div class="overlay"></div>


    <!-- [Part 1 of Flag - 學長留下的註解自白]: {part1} -->


    <div class="card">


        <div class="terminal-header">


            <span class="circle c-red"></span>


            <span class="circle c-yellow"></span>


            <span class="circle c-green"></span>


            <small class="text-danger ml-2 font-weight-bold">WARNING: LEGACY_TRASH_CODE.JS (LAST UPDATED 2016)</small>


        </div>


        <div class="p-5 text-center">


            <h2 class="text-warning mb-3">🗑️ 實驗室首頁年久失修（屎山代碼）</h2>


            <p class="lead">除錯苦主隊伍：<span class="highlight">{team_name}</span></p>


            <hr style="border-color: #30363d;">


            <p class="text-muted">這是十年前某位畢業學長留下的內部系統，畫面上空無一物是因為前端工程師跑路了。<br>請深入原始碼註解和 Cookie 翻出學長當年寫下的真正自白。</p>


            <div class="alert alert-dark border-danger mt-4 text-left font-italic small" style="background: #090d13;">


                <div>🧹 <strong>屎山考古指引：</strong></div>


                <div>1. 按下鍵盤 <strong>F12</strong> 打開開發者工具。</div>


                <div>2. 在 <strong>Elements (原始碼註解)</strong> 中挖出前半段 Flag。</div>


                <div>3. 在 <strong>Application -> Cookies (flag_part2)</strong> 翻出後半段 Flag。</div>


                <div>4. 將兩段拼湊為完整的 <code>NCUMIS{{...}}</code> 送出！</div>


            </div>


        </div>


    </div>


</body>


</html>"""

    resp = make_response(html)

    resp.set_cookie("flag_part2", part2, path="/")  # NOSONAR

    return resp


@labs_bp.route("/labs/crypto")
def lab_crypto():

    team_name = get_current_player_name()

    full_flag = generate_dynamic_flag("prof_please_sign_course", team_name)

    caesar_str = ""

    for c in full_flag:
        if "a" <= c <= "z":
            caesar_str += chr((ord(c) - ord("a") + 3) % 26 + ord("a"))

        elif "A" <= c <= "Z":
            caesar_str += chr((ord(c) - ord("A") + 3) % 26 + ord("A"))

        else:
            caesar_str += c

    b64_ciphertext = base64.b64encode(caesar_str.encode("utf-8")).decode("utf-8")

    html = f"""<!DOCTYPE html>


<html>


<head>


    <meta charset="utf-8">


    <title>選課求生指南：教授的機密加簽信</title>


    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">


    <link href="https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Noto+Serif+TC:wght@500;700&display=swap" rel="stylesheet">


    <style>


        body {{


            background: #12100e url("/labs/assets/professor.jpg") no-repeat center center fixed;


            background-size: cover;


            color: #2b2b2b;


            font-family: "Noto Serif TC", serif;


            display: flex;


            align-items: center;


            justify-content: center;


            min-height: 100vh;


            margin: 0;


            padding: 30px 15px;


        }}


        .bg-dimmer {{


            position: fixed; top: 0; left: 0; right: 0; bottom: 0;


            background: linear-gradient(135deg, rgba(10,8,6,0.85) 0%, rgba(20,15,10,0.7) 100%);


            backdrop-filter: blur(2px);


            z-index: 1;


        }}


        .letter-container {{


            position: relative; z-index: 2;


            background: #fbf7ee url("data:image/svg+xml,%3Csvg width=\'40\' height=\'40\' viewBox=\'0 0 40 40\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23d8cfbe\' fill-opacity=\'0.2\' fill-rule=\'evenodd\'%3E%3Cpath d=\'M0 40L40 0H20L0 20M40 40V20L20 40\'/%3E%3C/g%3E%3C/svg%3E");


            border: 2px solid #c8b99c;


            border-radius: 4px;


            max-width: 760px; width: 100%;


            padding: 45px 50px;


            box-shadow: 0 15px 45px rgba(0,0,0,0.6), inset 0 0 80px rgba(190,165,130,0.25);


        }}


        .letter-header {{


            border-bottom: 2px double #8c7b65;


            padding-bottom: 15px;


            margin-bottom: 25px;


            display: flex;


            justify-content: space-between;


            align-items: center;


        }}


        .univ-title {{ font-size: 1.3rem; font-weight: 700; color: #4a3824; letter-spacing: 2px; }}


        .stamp-box {{


            border: 2px solid #b22222;


            color: #b22222;


            font-size: 0.85rem;


            font-weight: bold;


            padding: 4px 10px;


            transform: rotate(-5deg);


            letter-spacing: 2px;


            text-transform: uppercase;


            box-shadow: 0 0 5px rgba(178,34,34,0.3);


        }}


        .cipher-paper {{


            background: #f1ebd9;


            border-left: 4px solid #8c7b65;


            padding: 18px;


            border: 2px solid #d32f2f;


        }}


    </style>


</head>


<body>


    <div class="bg-dimmer"></div>


    <div class="letter-container">


        <div class="letter-header">


            <div>


                <div class="univ-title">國立中央大學 資訊管理研究所</div>


                <small class="text-muted">COURSE REGISTRATION AUTHORIZATION DISPATCH</small>


            </div>


            <div class="stamp-box">加簽授權 APPROVED</div>


        </div>


        <p class="mb-2"><strong>致 搶不到熱門課程的研一隊伍：</strong> <u class="text-primary font-weight-bold">{team_name}</u></p>


        <p style="text-indent: 2em; line-height: 1.8; color: #3c3226;">


            聽說系上的熱門研究所課程一開放就被秒殺，幾十個同學擠在研究室門口排隊求加簽？


            教授特別把今年最後一份<strong>「人工加選授權密碼 (Add-Drop Code)」</strong>加密鎖在底下這封機密專箋中。


        </p>


        <p style="text-indent: 2em; line-height: 1.8; color: #3c3226;">


            教授特別聲明：<strong>「唯有具備密碼破譯能力的同學，方能取得最後的加簽通行證。」</strong>這份密文經過了兩重經典加密工法防護，你能抽絲剝繭還原出真正的 Flag 嗎？


        </p>


        <div class="cipher-paper text-center">


            {b64_ciphertext}


        </div>


        <p class="text-muted small" style="line-height: 1.6;">


            ※ 密件說明：請善用密碼學分析思維或前往 CTFd 平台購買 Hint 獲取破解線索。


        </p>


        <div class="signature-row">


            <div>


                <div class="wax-seal">NCU<br>MIS</div>


            </div>


            <div class="text-right">


                <div>被加簽信件淹沒的授課教授 留</div>


                <small class="text-muted">寫於 開學選課週的研究室</small>


            </div>


        </div>


    </div>


</body>


</html>"""

    return html


@labs_bp.route("/labs/sqli", methods=["GET"])
def lab_sqli_get():
    return _render_lab_sqli()


@labs_bp.route("/labs/sqli", methods=["POST"])
@bypass_csrf_protection
def lab_sqli_post():
    return _render_lab_sqli()


def _render_lab_sqli():

    team_name = get_current_player_name()

    dynamic_flag = generate_dynamic_flag("prof_also_overslept", team_name)

    msg = ""

    is_success = False

    if request.method == "POST":
        username = request.form.get("username", "").strip()

        password = request.form.get("password", "").strip()

        sqli_patterns = [
            "' or 1=1",
            "' or '1'='1",
            "' or ''='",
            "' or true",
            "' or 1=1#",
            "' or 1=1--",
            "admin'--",
            "admin' #",
        ]

        user_lower = username.lower().replace(" ", "")

        if any(p.replace(" ", "") in user_lower for p in sqli_patterns) or (
            "'" in username
            and ("or" in user_lower or "--" in username or "#" in username)
        ):
            is_success = True

            msg = f"🎉 <strong>漏洞利用成功！萬能密碼已繞過資料庫驗證。</strong><br>隊伍 <strong>{team_name}</strong> 取得後台真相 Flag：<br><code class='text-warning h5 mt-2 d-inline-block p-2 bg-dark rounded'>{dynamic_flag}</code>"

        elif username == "admin" and password == os.environ.get(
            "CHALLENGE_ADMIN_PASSWORD", "super_secret_password_nobody_knows"
        ):  # skipcq: BAN-B105, PTC-W1003 # nosec
            is_success = True

            msg = f"🎉 <strong>管理員登入成功！</strong><br>隊伍 <strong>{team_name}</strong> 專屬通關 Flag：<br><code class='text-warning h5 mt-2 d-inline-block p-2 bg-dark rounded'>{dynamic_flag}</code>"

        else:
            msg = "❌ <strong>身分驗證失敗！</strong> 帳號或密碼錯誤。若遭遇困難可至 CTFd 平台購買 Hint 獲取破解線索。"

    html = f"""<!DOCTYPE html>


<html>


<head>


    <meta charset="utf-8">


    <title>Web 挑戰：咪挺出席與成績管理系統</title>


    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">


    <style>


        body {{


            background: #0a0e17 url("/labs/assets/server_room.jpg") no-repeat center center fixed;


            background-size: cover;


            color: #c9d1d9;


            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;


            display: flex;


            align-items: center;


            justify-content: center;


            min-height: 100vh;


            margin: 0;


            padding: 20px;


        }}


        .bg-dimmer {{


            position: fixed; top: 0; left: 0; right: 0; bottom: 0;


            background: rgba(10, 14, 23, 0.85);


            backdrop-filter: blur(5px);


            z-index: 1;


        }}


        .login-card {{


            position: relative; z-index: 2;


            background: rgba(18, 26, 41, 0.92);


            border: 1px solid #1f6feb;


            border-radius: 12px;


            max-width: 520px; width: 100%;


            padding: 35px 40px;


            box-shadow: 0 16px 48px rgba(0, 80, 255, 0.25);


        }}


        .form-control {{


            background: #0b111a;


            border: 1px solid #30363d;


            color: #58a6ff;


            font-family: monospace;


        }}


        .form-control:focus {{


            background: #0b111a;


            border-color: #58a6ff;


            color: #58a6ff;


            box-shadow: 0 0 10px rgba(88, 166, 255, 0.3);


        }}


        .badge-status {{


            background: rgba(218, 54, 51, 0.2);


            color: #f85149;


            border: 1px solid #da3633;


            padding: 4px 10px;


            border-radius: 20px;


            font-size: 0.8rem;


        }}


    </style>


</head>


<body>


    <div class="bg-dimmer"></div>


    <div class="login-card">


        <div class="d-flex justify-content-between align-items-center mb-3">


            <h4 class="text-primary m-0">📊 咪挺出席與評鑑系統</h4>


            <span class="badge-status">● RESTRICTED ACCESS</span>


        </div>


        <p class="text-muted small mb-4">掌握全體研究生生殺大權 — 當前挑戰隊伍：<strong class="text-info">{team_name}</strong></p>


        {f"<div class='alert alert-{'success' if is_success else 'danger'} text-center'>{msg}</div>" if msg else ""}


        <form method="POST">


            <div class="form-group">


                <label class="small text-muted">管理員帳號 (Username)</label>


                <input type="text" name="username" class="form-control" placeholder="請輸入帳號" required autofocus>


            </div>


            <div class="form-group">


                <label class="small text-muted">管理員密碼 (Password)</label>


                <input type="password" name="password" class="form-control" placeholder="••••••••">


            </div>


            <button type="submit" class="btn btn-primary btn-block mt-4 font-weight-bold">


                ⚡ 登入系統驗證身分


            </button>


        </form>


        <div class="mt-4 pt-3 border-top border-secondary text-muted small text-center">


            🔒 內部安全聲明：本登入閘道受 SQL 身分驗證保護，未授權存取將被記錄。


        </div>


    </div>


</body>


</html>"""

    return html


class DynamicShuffleFlag(BaseFlag):
    name = "dynamic_shuffle"

    templates = {
        "create": "/plugins/dynamic_shuffle_flag/assets/create.html",
        "update": "/plugins/dynamic_shuffle_flag/assets/edit.html",
    }

    @staticmethod
    def compare(chal_key_obj, provided):

        saved = chal_key_obj.content

        data = chal_key_obj.data

        team = get_current_team()

        user = get_current_user()

        candidates = []

        if team and team.name:
            candidates.append(generate_dynamic_flag(saved, team.name.strip()))

        if user and user.name:
            candidates.append(generate_dynamic_flag(saved, user.name.strip()))

        if not candidates:
            return False

        provided_clean = provided.strip()

        if data == "case_insensitive":
            return any(provided_clean.lower() == c.lower() for c in candidates)

        else:
            return any(provided_clean == c for c in candidates)


r_visit_client = redis.Redis(host="cache", port=6379, db=0, decode_responses=True)


@labs_bp.route("/download/visits", methods=["GET"])
def api_get_site_visits():

    try:
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip and "," in ip:
            ip = ip.split(",")[0].strip()
        ip_throttle_key = f"throttle_ip_{ip}"

        has_session = session.get("site_visited_recorded")
        is_ip_throttled = r_visit_client.get(ip_throttle_key)

        if not r_visit_client.exists("site_total_visits"):
            r_visit_client.set("site_total_visits", 1)

        if not has_session and not is_ip_throttled:
            session["site_visited_recorded"] = True
            if ip:
                r_visit_client.setex(ip_throttle_key, 600, "1")
            count = r_visit_client.incr("site_total_visits")
        else:
            count = int(r_visit_client.get("site_total_visits") or 1)

        return jsonify({"count": count, "success": True})
    except Exception as e:
        return jsonify({"count": 1, "success": False, "error": str(e)})


def load(app):

    register_plugin_assets_directory(
        app, base_path="/plugins/dynamic_shuffle_flag/assets/"
    )

    register_plugin_script("/plugins/dynamic_shuffle_flag/assets/story_epilogue.js")

    FLAG_CLASSES["dynamic_shuffle"] = DynamicShuffleFlag

    app.register_blueprint(labs_bp)
