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

**SERVERS 格式说明**：
- 单服务器：`名称,ID,标识`
- 多服务器：`名称1,ID1,标识1;名称2,ID2,标识2`
- 标识必须包含 `US` 或 `FR`

**示例**：
```
Server1,a1b2c3d4,Over-US 🇺🇸;Server2,e5f6g7h8,Over-FR 🇫🇷
```

### 3️⃣ 手动测试

进入 **Actions** → **Overnode Auto Renew** → **Run workflow**

### 4️⃣ 查看结果

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

默认每天 UTC 00:00（北京时间 08:00）自动运行

修改 `.github/workflows/over-renew.yml` 可更改运行时间

---

## 📖 详细文档

查看 [OVERNODE_CONFIG.md](./OVERNODE_CONFIG.md) 了解完整配置说明

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
├── OVERNODE_CONFIG.md         # 详细配置文档
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
