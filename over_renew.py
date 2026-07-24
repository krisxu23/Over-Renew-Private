#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import time
import datetime
import urllib.request
import urllib.parse
import requests

# ============================================================
# 环境变量解析
# ============================================================

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"].strip()
GUILD_ID      = os.environ.get("GUILD_ID", "1268504004904615948").strip()

_tg        = os.environ.get("TG_BOT", "").split(",")
TG_CHAT_ID = _tg[0].strip() if len(_tg) > 0 else ""
TG_TOKEN   = _tg[1].strip() if len(_tg) > 1 else ""

IS_PROXY      = os.environ.get("IS_PROXY", "false").lower() == "true"
PROXY_SERVER  = os.environ.get("PROXY_SERVER", "").strip() or "http://127.0.0.1:1080"

# 解析 SERVERS 环境变量
_servers_env = os.environ.get("SERVERS", "").strip()
if _servers_env:
    SERVERS = []
    for srv_str in _servers_env.split(";"):
        parts = [p.strip() for p in srv_str.split(",")]
        if len(parts) == 3:
            SERVERS.append({"name": parts[0], "id": parts[1], "code": parts[2]})
else:
    SERVERS = [
        {"name": "FreeZero", "id": "6348f48a", "code": "Over-US 🇺🇸"},
        {"name": "FreeOne",  "id": "23e794e1", "code": "Over-FR 🇫🇷"},
    ]

DISCORD_API  = "https://discord.com/api/v9"
CLIENT_ID    = "972921155205877860"
REDIRECT_URI = "https://console.overnode.fr/auth/discord/callback"
SITE_URL     = "https://console.overnode.fr"
UA           = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"

# === AUTO-UPDATED ===
LAST_RENEWED_US = "2026-07-19 21:59:25"
LAST_RENEWED_FR = "2026-07-19 21:59:25"
# ===================


# ============================================================
# 工具函数
# ============================================================

def now_str():
    utc_now = datetime.datetime.utcnow()
    bj_now  = utc_now + datetime.timedelta(hours=8)
    return bj_now.strftime('%Y-%m-%d %H:%M:%S')

def log(msg):
    print(msg, flush=True)

def parse_dt(dt_str: str) -> datetime.datetime:
    dt_str = dt_str.replace("+00:00", "").replace("Z", "")
    if "." in dt_str:
        return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f")
    return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")

def fmt_remaining(total_sec: int) -> str:
    if total_sec <= 0:
        return "已过期"
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    return f"{h}h {m}m"

def send_tg(lines: list):
    if not TG_TOKEN or not TG_CHAT_ID:
        return
    msg  = "\n".join(lines)
    url  = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TG_CHAT_ID, "text": msg}).encode()
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15):
            log("📨 TG 推送成功")
    except Exception as e:
        log(f"⚠️ TG 推送失败：{e}")


# ============================================================
# 创建 requests Session
# ============================================================

def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "user-agent":      UA,
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    })
    if IS_PROXY:
        session.proxies.update({
            "http":  PROXY_SERVER,
            "https": PROXY_SERVER,
        })
    return session


# ============================================================
# Discord OAuth → connect.sid
# ============================================================

def login_via_discord(session: requests.Session):

    log("🔍 验证 Discord Token...")
    try:
        test_resp = session.get(
            f"{DISCORD_API}/users/@me",
            headers={"authorization": DISCORD_TOKEN},
            timeout=10
        )
        log(f"   Token 验证状态码: {test_resp.status_code}")
        if test_resp.status_code == 200:
            user_data = test_resp.json()
            username = user_data.get('username', 'Unknown')
            user_id = user_data.get('id', 'Unknown')
            log(f"   ✅ Token 有效，用户: {username} (ID: {user_id})")
        else:
            log(f"   ❌ Token 无效，响应: {test_resp.text[:200]}")
            raise RuntimeError("Discord Token 验证失败")
    except Exception as e:
        log(f"   ❌ Token 验证异常: {e}")
        raise

    log("🔗 步骤1: 获取 State...")
    resp = session.get(
        f"{SITE_URL}/auth/discord/login",
        headers={"accept": "text/html,*/*"},
        allow_redirects=False,
        timeout=20,
    )
    log(f"   状态码: {resp.status_code}")

    location = resp.headers.get("location", "")
    log(f"   Location: {location[:100]}...")

    state = None
    if location and "discord.com" in location:
        parsed = urllib.parse.urlparse(location)
        qs     = urllib.parse.parse_qs(parsed.query)
        state  = qs.get("state", [None])[0]
        log(f"   ✅ State: {state[:20]}...")
    else:
        raise RuntimeError(f"未获取到 Discord 重定向，location: '{location}'")

    log("🎫 步骤2: Discord OAuth 授权...")
    redirect_uri_encoded = urllib.parse.quote(REDIRECT_URI, safe="")
    oauth_url = (
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri_encoded}"
        f"&scope=identify%20email%20guilds.join"
        f"&state={state}"
    )

    resp = session.post(
        oauth_url,
        json={
            "guild_id":         GUILD_ID,
            "permissions":      "0",
            "authorize":        True,
            "integration_type": 0,
            "location_context": {
                "guild_id":     "10000",
                "channel_id":   "10000",
                "channel_type": 10000,
            },
        },
        headers={
            "accept":        "*/*",
            "authorization": DISCORD_TOKEN,
            "content-type":  "application/json",
            "origin":        "https://discord.com",
            "referer": (
                f"https://discord.com/oauth2/authorize"
                f"?client_id={CLIENT_ID}"
                f"&redirect_uri={redirect_uri_encoded}"
                f"&response_type=code"
                f"&scope=identify+email+guilds.join"
                f"&state={state}"
            ),
        },
        timeout=20,
    )

    log(f"   状态码: {resp.status_code}")

    if resp.status_code == 401:
        log(f"   ❌ 响应: {resp.text[:300]}")
        raise RuntimeError("Discord Token 无效或已过期")
    if resp.status_code == 429:
        log(f"   ❌ 频率限制: {resp.text[:300]}")
        raise RuntimeError("Discord API 频率限制（Rate Limit）")
    if resp.status_code != 200:
        log(f"   ❌ 响应: {resp.text[:300]}")
        raise RuntimeError(f"Discord OAuth 响应码: {resp.status_code}")

    location = resp.json().get("location", "")
    log(f"   Callback Location: {location[:100]}...")

    if not location:
        log(f"   ❌ 完整响应: {resp.text[:500]}")
        raise RuntimeError("无法从 OAuth 响应中提取 Redirect Location")

    code = urllib.parse.parse_qs(urllib.parse.urlparse(location).query).get("code", [None])[0]
    if not code:
        raise RuntimeError("无法从 Redirect URL 提取 Code")
    log(f"   ✅ Code: {code[:20]}...")

    log("🔄 步骤3: Callback 换取 Session...")
    cb_resp = session.get(
        f"{REDIRECT_URI}?code={code}&state={state}",
        headers={
            "accept":  "text/html,application/xhtml+xml,*/*;q=0.8",
            "referer": "https://discord.com/",
        },
        allow_redirects=True,
        timeout=20,
    )

    log(f"   最终 URL: {cb_resp.url}")
    log(f"   状态码: {cb_resp.status_code}")

    log("🍪 当前所有 Cookies:")
    for cookie in session.cookies:
        value_preview = cookie.value[:30] + "..." if len(cookie.value) > 30 else cookie.value
        log(f"   {cookie.name} = {value_preview}")
        log(f"      domain: {cookie.domain}, path: {cookie.path}, secure: {cookie.secure}")

    sid = session.cookies.get("connect.sid")
    if not sid:
        log("   ⚠️ 未找到 connect.sid，尝试验证登录状态...")

    log("✅ 步骤4: 验证登录状态...")
    verify = session.get(f"{SITE_URL}/api/user", timeout=10)
    log(f"   /api/user 状态码: {verify.status_code}")

    if verify.status_code == 200:
        user_info = verify.json()
        log(f"   ✅ 登录成功！用户: {user_info.get('username', 'Unknown')}")
    else:
        log(f"   ❌ 登录验证失败")
        log(f"   响应头: {dict(verify.headers)}")
        log(f"   响应体: {verify.text[:500]}")

        if verify.status_code in [301, 302, 303, 307, 308]:
            log(f"   重定向到: {verify.headers.get('location', 'N/A')}")

        raise RuntimeError(f"登录验证失败，/api/user 返回: {verify.status_code}")


# ============================================================
# 执行续期
# ============================================================

def do_renew(session: requests.Session, sid: str) -> dict:
    resp = session.post(
        f"{SITE_URL}/api/server/{sid}/renewal/renew",
        headers={
            "accept":  "application/json, text/plain, */*",
            "origin":  SITE_URL,
            "referer": f"{SITE_URL}/server/{sid}/overview",
        },
        timeout=20,
    )
    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text[:300]}

    if resp.status_code not in (200, 400):
        raise RuntimeError(f"续期请求失败，状态码: {resp.status_code}，响应: {data}")

    return data


# ============================================================
# 主流程
# ============================================================

def run():
    server_names = " | ".join(s["code"] for s in SERVERS)
    log("=" * 50)
    log(f"🎮 Over-Renew 启动")
    log(f"🕐 运行时间: {now_str()}")
    log(f"🖥 服务器: {server_names}")
    log("=" * 50)

    session = create_session()

    log("🌐 验证出口 IP...")
    try:
        ip_resp   = session.get("https://api.ipify.org/?format=json", timeout=10)
        ip        = ip_resp.json().get("ip", "")
        ip_masked = re.sub(r'(\d+\.\d+\.)\d+\.\d+', r'\g<1>**.**', ip)
        log(f"📍 出口 IP 确认：{ip_masked}")
    except Exception as e:
        log(f"⚠️ IP 验证失败：{e}")

    log("🔑 Discord OAuth 登录...")
    try:
        login_via_discord(session)
    except Exception as e:
        log(f"❌ 登录失败：{e}")
        send_tg([
            "🎮 Over 续期通知",
            f"🕐 运行时间: {now_str()}",
            f"🖥 服务器: {server_names}",
            "❌ 登录失败",
            f"📝 {e}",
        ])
        return

    log("✅ Discord OAuth 登录完成")
    log("=" * 50)


if __name__ == "__main__":
    run()
