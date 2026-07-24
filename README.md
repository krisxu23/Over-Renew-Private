# 🎮 Over-Renew

Overnode 免费服务器自动续期脚本，通过 Discord OAuth 登录面板并触发续期，支持 Telegram 通知与 cron-job.org 自动调度。

## 🔧 环境变量

| 变量 | 说明 | 示例 |
|---|---|---|
| 🔑 `DISCORD_TOKEN` | Discord 账号 Token（用于授权登录面板） | `MTM1...` |
| 📨 `TG_BOT` | Telegram 推送配置，格式 `chat_id,bot_token` | `123456,789:ABC...` |
| 🔁 `CRON_JOB` | cron-job.org 写回配置，格式 `api_key,job_id` | `cjk_xxx,123456` |
| 🛡️ `GOST_PROXY` | 可选，GOST 代理转发地址（用于切换出口IP） | `socks5://1.2.3.4:1080` |
| 🔐 `PRIVATE_REPO_TOKEN` | GitHub Token，用于拉取私库脚本及推回更新 | `ghp_xxx` |

## 🚀 运行

```bash
pip install requests
python over_renew.py
```

## ⚙️ 工作流程

1. 🌐 验证出口 IP
2. 🔑 Discord OAuth 登录获取 Session
3. 🔄 依次对 `SERVERS` 列表中的服务器执行续期
4. 📅 计算下次续期时间，就近写回 cron-job.org（两台相差 ≤5分钟则一并续期，否则分批触发）
5. 💾 续期成功的服务器自动更新脚本内 `LAST_RENEWED_XX` 时间戳
6. 📨 推送续期结果到 Telegram

## 📊 续期结果

- ✅ 续期成功
- ⌛️ 期限未至
- ❌ 续期失败

## 🖥 服务器配置

在 `SERVERS` 列表中增删服务器，`code` 字段需包含 `US` 或 `FR` 字样以匹配对应的 `LAST_RENEWED_XX` 字段。

```python
SERVERS = [
    {"name": "SERVERS1", "id": "12345678", "code": "Over-US 🇺🇸"},
    {"name": "SERVERS2",  "id": "12345678", "code": "Over-FR 🇫🇷"},
]
```
