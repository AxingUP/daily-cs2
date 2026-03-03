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
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
