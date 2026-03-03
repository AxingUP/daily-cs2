"""
爬虫基类
提供通用的 HTTP 请求功能
"""
import requests
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """爬虫基类"""

    def __init__(self):
        self.session = requests.Session()
        # 使用更完整的请求头模拟真实浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })

    def get(self, url: str, params: dict = None, timeout: int = 30) -> requests.Response:
        """
        发送 GET 请求

        Args:
            url: 请求 URL
            params: 查询参数
            timeout: 超时时间（秒）

        Returns:
            Response 对象
        """
        response = self.session.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response
