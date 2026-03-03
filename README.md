# CS2 每日资讯

自动获取 CS2 每日信息（赛事赛程、游戏更新），并通过 QQ 邮箱 SMTP 发送到指定邮箱。

## 功能特性

- 🏆 自动获取今日比赛结果
- 📅 自动获取即将进行的比赛赛程
- 📝 自动获取 CS2 游戏更新和新闻
- 📧 精美的 HTML 邮件格式
- ⏰ 每日北京时间早上 8:00 自动发送

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/daily-cs2.git
cd daily-cs2
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入以下信息：

**单个收件人：**
```env
QQ_EMAIL=your_qq_email@qq.com
QQ_AUTH_CODE=your_qq_auth_code
TO_EMAIL=recipient@example.com
```

**多个收件人（用逗号或分号分隔）：**
```env
QQ_EMAIL=your_qq_email@qq.com
QQ_AUTH_CODE=your_qq_auth_code
TO_EMAIL=user1@example.com,user2@example.com,user3@example.com
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 本地测试

```bash
python src/main.py
```

## GitHub Actions 部署

### 配置 GitHub Secrets

在 GitHub 仓库的 Settings -> Secrets and variables -> Actions 中添加以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|--------------|------|------|
| `QQ_EMAIL` | 发件 QQ 邮箱 | `123456789@qq.com` |
| `QQ_AUTH_CODE` | QQ 邮箱授权码 | 在邮箱设置中生成 |
| `TO_EMAIL` | 收件人邮箱（支持多个，用逗号分隔） | `user1@example.com,user2@example.com` |

### 获取 QQ 邮箱授权码

1. 登录 QQ 邮箱网页版
2. 进入「设置」→「账户」
3. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」
4. 开启「IMAP/SMTP服务」
5. 按提示发送短信验证
6. 获取授权码（16位字符串）

### 手动触发

在 GitHub 仓库的 Actions 页面，选择「CS2 Daily News」工作流，点击「Run workflow」即可手动触发。

## 项目结构

```
daily-cs2/
├── .github/
│   └── workflows/
│       └── cs2-daily-news.yml       # GitHub Action 工作流
├── src/
│   ├── __init__.py
│   ├── main.py                       # 主程序入口
│   ├── config.py                     # 配置管理
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py           # 爬虫基类
│   │   ├── hltv.py                   # HLTV 赛事数据爬取
│   │   └── steam_news.py             # Steam 新闻爬取
│   ├── models/
│   │   ├── __init__.py
│   │   └── match.py                  # 比赛数据模型
│   ├── formatters/
│   │   ├── __init__.py
│   │   └── email_formatter.py       # 邮件格式化
│   └── email_sender.py               # 邮件发送
├── requirements.txt                  # Python 依赖
├── .env.example                      # 环境变量示例
└── README.md                         # 项目文档
```

## 技术栈

- **Python 3.11+**
- **requests**: HTTP 请求
- **BeautifulSoup4**: HTML 解析
- **python-dotenv**: 环境变量管理
- **GitHub Actions**: 自动化工作流

## 注意事项

- HLTV 可能修改页面结构，需要持续维护
- GitHub Actions 有运行时间限制（免费版 2000 分钟/月）
- 邮件发送失败时会有重试机制（最多重试 3 次）
- 时区处理：GitHub Action 运行在 UTC，程序内部转换为北京时间

## 许可证

MIT License
