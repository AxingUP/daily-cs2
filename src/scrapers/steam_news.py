"""
Steam 新闻爬虫
获取 CS2 游戏更新和新闻
"""
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper


class SteamNewsScraper(BaseScraper):
    """Steam 新闻爬虫"""

    def __init__(self, app_id: int = 730):
        super().__init__()
        self.app_id = app_id
        self.api_url = "https://store.steampowered.com/api/featured"

    def get_latest_news(self, count: int = 3) -> List[Dict[str, str]]:
        """
        获取最新的 Steam 新闻

        Args:
            count: 获取新闻数量

        Returns:
            新闻列表，每条新闻包含 title, url, date, content
        """
        news_list = []

        try:
            # 使用 Steam Store API 获取应用新闻
            url = f"https://store.steampowered.com/api/newsforapp/v2"
            params = {
                'appid': self.app_id,
                'count': count,
                'maxlength': 300
            }

            response = self.get(url, params=params)
            data = response.json()

            news_items = data.get('appnews', {}).get('newsitems', [])

            for item in news_items:
                news_list.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'date': item.get('date', 0),
                    'content': item.get('contents', '').strip()[:500],  # 限制内容长度
                    'author': item.get('author', '')
                })

        except Exception as e:
            print(f"获取 Steam 新闻失败: {e}")

        return news_list
