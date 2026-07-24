# Overnode 自动续期脚本配置指南

## 📋 必需的 GitHub Secrets 配置

进入你的 GitHub 仓库：**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### 1. DISCORD_TOKEN（必填）
**说明**：你的 Discord 账号 Token

**获取方法**：
1. 在浏览器打开 Discord：https://discord.com/channels/1268504004904615948
2. 确保你已加入 Overnode 服务器
3. 按 `F12` 打开开发者工具
4. 点击 **Network**（网络）标签
5. 刷新页面或发送一条消息
6. 点击任意请求 → **Headers** → **Request Headers**
7. 找到 `authorization:` 复制后面的完整值

**格式**：`MTAxxxxxxxxxxxxx.GYxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### 2. GUILD_ID（必填）
**说明**：Overnode Discord 服务器 ID

**值**：`1268504004904615948`

---

### 3. SERVERS（必填）
**说明**：你的服务器列表

**格式**：`name1,id1,code1;name2,id2,code2`

**获取服务器 ID**：
1. 访问 https://console.overnode.fr/
2. 用 Discord 登录
3. 点击你的服务器
4. 从 URL 中获取 ID：
   ```
   https://console.overnode.fr/server/abc12345/overview
                                     ^^^^^^^^
                                     这就是 ID
   ```

**示例**：
```
MyServer1,abc12345,Over-US 🇺🇸;MyServer2,def67890,Over-FR 🇫🇷
```

**单服务器示例**：
```
MyServer,abc12345,Over-US 🇺🇸
```

**注意**：
- `code` 字段必须包含 `US` 或 `FR` 用于匹配续期时间戳
- 多个服务器用分号 `;` 分隔
- 每个服务器 3 个字段用逗号 `,` 分隔

---

### 4. TG_BOT（可选）
**说明**：Telegram 推送通知配置

**格式**：`chat_id,bot_token`

**获取方法**：
1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot` 创建 Bot
3. 获得 `bot_token`
4. 搜索 `@userinfobot` 获取你的 `chat_id`

**示例**：
```
123456789,123456:ABCdefGHIjklMNOpqrSTUvwxYZ
```

---

### 5. CRON_JOB（可选）
**说明**：cron-job.org 自动调度配置

**格式**：`api_key,job_id`

**获取方法**：
1. 注册 https://cron-job.org/
2. 创建定时任务
3. 获取 API Key 和 Job ID

**示例**：
```
cjk_abcdefghijk,123456
```

---

### 6. GOST_PROXY（可选）
**说明**：GOST 代理配置（用于切换出口 IP）

**格式**：`socks5://ip:port` 或 `http://ip:port`

**示例**：
```
socks5://1.2.3.4:1080
```

---

## 🚀 使用步骤

### 1. 创建仓库并上传文件
```bash
git clone https://github.com/你的用户名/你的仓库.git
cd 你的仓库
# 复制 over_renew.py 和 .github/workflows/over-renew.yml
git add .
git commit -m "Add Overnode auto renew script"
git push
```

### 2. 配置 GitHub Secrets
按照上面的说明，在 GitHub 仓库设置中添加所有必需的 Secrets

### 3. 手动测试
进入 **Actions** → **Overnode Auto Renew** → **Run workflow** → **Run workflow**

### 4. 查看运行日志
在 **Actions** 标签页查看运行结果

---

## 📊 运行结果说明

| 状态 | 说明 |
|------|------|
| ✅ 续期成功 | 服务器已成功续期 |
| ⌛️ 期限未至 | 还不到续期时间 |
| ❌ 续期失败 | 续期出错，查看日志 |

---

## 🔧 故障排查

### 问题 1：登录失败（401 错误）
**原因**：Discord Token 无效或 Guild ID 错误

**解决**：
1. 确认你已加入 Overnode Discord 服务器
2. 重新获取 Discord Token
3. 检查 `GUILD_ID` 是否为 `1268504004904615948`

### 问题 2：未配置 SERVERS 错误
**原因**：没有设置 `SERVERS` 环境变量

**解决**：
在 GitHub Secrets 中添加 `SERVERS` 配置

### 问题 3：续期失败
**原因**：服务器 ID 错误或服务器已被删除

**解决**：
1. 登录 Overnode 控制台确认服务器存在
2. 检查 `SERVERS` 配置中的服务器 ID 是否正确

---

## 📅 自动运行时间

默认每天 UTC 00:00（北京时间 08:00）自动运行

**修改运行时间**：
编辑 `.github/workflows/over-renew.yml` 中的 cron 表达式：
```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 时间，改成你需要的时间
```

---

## 🔒 安全提示

- ❌ 不要在代码中硬编码 Token
- ❌ 不要将 Secrets 提交到 Git
- ✅ 所有敏感信息都使用 GitHub Secrets
- ✅ 定期更新 Discord Token（如果失效）

---

## 📞 支持

如遇问题，请检查：
1. GitHub Actions 运行日志
2. Discord Token 是否有效
3. 服务器 ID 是否正确
4. 是否加入了 Overnode Discord 服务器
