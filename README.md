# 🎮 Overnode 自动续期

Overnode 免费服务器自动续期脚本，通过 Discord OAuth 登录并自动续期服务器。

## ⚡ 快速开始

### 1️⃣ 获取必要信息

#### Discord Token
1. 打开 https://discord.com/channels/1268504004904615948
2. 按 `F12` → **Network** 标签 → 刷新页面
3. 任意请求 → **Headers** → 复制 `authorization` 的值

#### 服务器 ID
1. 登录 https://console.overnode.fr/
2. 点击你的服务器
3. 从 URL 复制服务器 ID：
   ```
   https://console.overnode.fr/server/abc12345/overview
                                     ^^^^^^^^
   ```

### 2️⃣ 配置 GitHub Secrets

进入仓库 **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下 Secrets：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DISCORD_TOKEN` | Discord Token（必填） | `MTAxxxxx.GYxxx.xxxxx` |
| `GUILD_ID` | Discord 服务器 ID（必填） | `1268504004904615948` |
| `SERVERS` | 服务器列表（必填） | `MyServer,abc12345,Over-US 🇺🇸` |
| `NODE_LINK` | 代理节点链接（可选，绕过 VPN 检测） | `vless://...`、`hysteria2://...`、`vmess://...`、`trojan://...` 等 |
| `TG_BOT` | Telegram 推送（可选） | `123456,bot_token` |
| `CF_API_TOKEN` | Cloudflare API Token（可选，自动更新 cron） | 见下方教程 |
| `CF_ACCOUNT_ID` | Cloudflare 账户 ID（可选） | 见下方教程 |
| `CF_WORKER_NAME` | Cloudflare Worker 名称（可选） | `overnode-cron` |

**SERVERS 格式说明**：
- 单服务器：`名称,ID,标识`
- 多服务器：`名称1,ID1,标识1;名称2,ID2,标识2`
- 标识必须包含 `US` 或 `FR`

**示例**：
```
Server1,a1b2c3d4,Over-US 🇺🇸;Server2,e5f6g7h8,Over-FR 🇫🇷
```

### 3️⃣ 获取 Cloudflare API Token（可选，自动更新 cron）

续期后脚本会自动把下次运行时间写入 Cloudflare Worker 的 Cron 触发器，无需修改 GitHub Actions schedule。

#### 获取 CF_ACCOUNT_ID

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 右侧 URL 是 `https://dash.cloudflare.com/你的账户ID`
3. 复制这串 ID（是一串哈希值）

#### 获取 CF_API_TOKEN

1. 进入 [API Tokens 页面](https://dash.cloudflare.com/profile/api-tokens)
2. 点击 **Create Token** → **Create Custom Token**
3. 填写：
   - **Token name**: `overnode-cron`
   - **Permissions** → 选择：
     - `Workers` → `Edit`
   - **Account Resources** → 选择你的账户
4. 点击 **Continue to summary** → **Create Token**
5. **立即复制并保存 Token**（关闭后不可再次查看）

#### 配置 Secrets

回到 GitHub 仓库 **Settings → Secrets and variables → Actions**，添加：

| Secret | 值 |
|--------|-----|
| `CF_API_TOKEN` | 上一步复制的 Token |
| `CF_ACCOUNT_ID` | 你的 Cloudflare 账户 ID |
| `CF_WORKER_NAME` | 你的 Worker 名称（如 `overnode-cron`） |

### 4️⃣ 手动测试

进入 **Actions** → **Overnode Auto Renew** → **Run workflow**

### 5️⃣ 查看结果

在 **Actions** 页面查看运行日志

---

## 📊 运行状态

- ✅ **续期成功** - 服务器已续期
- ⌛️ **期限未至** - 还不到续期时间
- ❌ **续期失败** - 查看日志排查问题

---

## 🔧 故障排查

### ❌ 登录失败 401
- 重新获取 Discord Token
- 确认已加入 Overnode Discord 服务器
- 检查 `GUILD_ID = 1268504004904615948`

### ❌ 未配置 SERVERS
- 在 GitHub Secrets 中添加 `SERVERS` 变量

### ❌ 续期失败
- 检查服务器 ID 是否正确
- 登录控制台确认服务器存在

---

## 📅 运行计划

- 续期成功后，脚本自动将下次运行时间写入 **Cloudflare Worker Cron 触发器**
- Cloudflare 每天北京时间 08:01 额外触发一次作为保险
- 支持手动触发（Actions → Run workflow）

---

## 📖 详细文档

查看 Cloudflare API 文档获取更多信息

---

## 🔒 安全提示

- ✅ 使用 GitHub Secrets 存储敏感信息
- ❌ 不要在代码中硬编码 Token
- 🔄 Token 失效时及时更新

---

## 📦 文件说明

```
.
├── over_renew.py              # 主脚本
├── .github/
│   └── workflows/
│       └── over-renew.yml     # GitHub Actions 配置
└── README.md                  # 本文件
```

---

## 🌟 功能特性

- 🔐 Discord OAuth 自动登录
- 🔄 自动续期服务器
- 📨 Telegram 通知支持
- ⏰ 定时任务调度
- 📊 详细运行日志

---

**创建时间**：2026-07-24  
**版本**：1.0.0
