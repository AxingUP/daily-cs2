"""
CS2 每日资讯主程序
"""
import sys
from pathlib import Path

# 将 src 的父目录添加到 Python 路径，使 src 成为一个可导入的包
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.config import load_config
from src.scrapers import HLTVScraper, SteamNewsScraper
from src.formatters import EmailFormatter
from src.email_sender import EmailSender


def main():
    """主函数"""
    print("开始获取 CS2 每日资讯...")

    # 1. 初始化配置
    config = load_config()
    print(f"配置加载成功")

    # 2. 爬取数据
    print("\n正在获取比赛数据...")
    hltv_scraper = HLTVScraper(config.hltv_base_url)
    matches = hltv_scraper.get_today_matches()
    print(f"获取到 {len(matches)} 场比赛")

    print("\n正在获取 Steam 新闻...")
    steam_scraper = SteamNewsScraper(config.steam_app_id)
    news = steam_scraper.get_latest_news(count=3)
    print(f"获取到 {len(news)} 条新闻")

    # 3. 格式化邮件
    print("\n正在格式化邮件...")
    formatter = EmailFormatter()
    email_content = formatter.format_email(matches, news)
    print("邮件格式化完成")

    # 4. 发送邮件
    print("\n正在发送邮件...")
    sender = EmailSender(config.email)
    success = sender.send_email(email_content)

    if success:
        print("\n✅ CS2 每日资讯发送成功！")
        return 0
    else:
        print("\n❌ CS2 每日资讯发送失败！")
        return 1


if __name__ == "__main__":
    sys.exit(main())
