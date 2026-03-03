# CS2 Daily News

自动化获取 CS2 每日新闻和赛事，并通过邮件发送的 GitHub Actions 工作流。

## 功能特性

- 📰 从 HLTV 获取 CS2 最新新闻
- ⚔️ 获取正在进行和即将进行的赛事信息
- 📧 每天早上 7 点（北京时间）自动发送精美 HTML 邮件
- 🔄 内置重试机制，自动处理网络错误
- 📬 支持多个收件人
- 🚫 使用 GitHub Secrets 安全存储敏感信息

## 配置步骤

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/daily-cs2.git
cd daily-cs2
```

### 2. 配置 GitHub Secrets

在 GitHub 仓库中进入 `Settings` -> `Secrets and variables` -> `Actions`，添加以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `SMTP_HOST` | SMTP 服务器地址 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `SMTP_SECURE` | 是否使用 SSL | `false` |
| `SMTP_USER` | 邮箱用户名 | `your-email@gmail.com` |
| `SMTP_PASSWORD` | 邮箱密码/应用专用密码 | `your-app-password` |
| `EMAIL_FROM` | 发件人显示名称 | `CS2 Daily News <your-email@gmail.com>` |
| `EMAIL_TO` | 收件人列表（逗号分隔） | `recipient1@example.com,recipient2@example.com` |
| `HLTV_BASE_URL` | HLTV 基础 URL（可选） | `https://hltv.org` |

### 3. 常用 SMTP 配置

#### Gmail
```
SMTP_HOST: smtp.gmail.com
SMTP_PORT: 587
SMTP_SECURE: false
SMTP_USER: your-email@gmail.com
SMTP_PASSWORD: [使用应用专用密码]
```

获取 Gmail 应用专用密码：
1. 进入 Google 账户设置
2. 安全性 -> 两步验证
3. 应用专用密码 -> 生成新密码

#### QQ 邮箱
```
SMTP_HOST: smtp.qq.com
SMTP_PORT: 587
SMTP_SECURE: false
SMTP_USER: your-email@qq.com
SMTP_PASSWORD: [使用授权码]
```

#### 163 邮箱
```
SMTP_HOST: smtp.163.com
SMTP_PORT: 465
SMTP_SECURE: true
SMTP_USER: your-email@163.com
SMTP_PASSWORD: [使用授权码]
```

#### Outlook
```
SMTP_HOST: smtp-mail.outlook.com
SMTP_PORT: 587
SMTP_SECURE: false
SMTP_USER: your-email@outlook.com
SMTP_PASSWORD: [你的密码]
```

### 4. 手动触发测试

在 GitHub 仓库中进入 `Actions` -> `CS2 Daily News` -> 点击 `Run workflow` 手动触发工作流进行测试。

## 工作流说明

### 调度时间
工作流默认在每天北京时间早上 7:00 自动执行（UTC 时间 23:00）。

### 执行流程
1. 拉取代码仓库
2. 设置 Node.js 环境
3. 安装依赖包
4. 执行 `node index.js` 获取数据并发送邮件
5. 报告执行状态

### 错误处理
代码内置了完善的错误处理机制：
- **网络错误重试**：请求失败时自动重试 3 次
- **403 限流处理**：遇到限流时等待 5 秒后重试
- **超时处理**：请求超时 30 秒后自动重试
- **连接验证**：发送邮件前验证 SMTP 连接

## 本地开发

### 安装依赖
```bash
npm install
```

### 配置环境变量
复制 `.env.example` 为 `.env` 并填写配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=CS2 Daily News <your-email@gmail.com>
EMAIL_TO=recipient1@example.com,recipient2@example.com
HLTV_BASE_URL=https://hltv.org
```

### 运行
```bash
npm start
```

## 项目结构

```
daily-cs2/
├── .github/
│   └── workflows/
│       └── cs2-daily-news.yml    # GitHub Actions 工作流配置
├── .env.example                  # 环境变量示例
├── index.js                      # 主程序
├── package.json                  # Node.js 依赖配置
└── README.md                     # 项目说明
```

## 邮件模板

邮件采用精美的 HTML 模板，包含：
- 📅 当前日期
- 📰 每日新闻列表
- ⚔️ 实时赛事进程
- 🔗 新闻和赛事详情链接

## 许可证

MIT License
