"""
邮件格式化器
将比赛数据和新闻格式化为 HTML 邮件
"""
from datetime import datetime
from typing import List, Dict
import pytz

from ..models.match import Match, MatchStatus


class EmailFormatter:
    """邮件格式化器"""

    def __init__(self):
        self.beijing_tz = pytz.timezone('Asia/Shanghai')

    def format_email(self, matches: List[Match], news: List[Dict[str, str]]) -> str:
        """
        格式化邮件内容

        Args:
            matches: 比赛列表
            news: 新闻列表

        Returns:
            HTML 格式的邮件内容
        """
        now = datetime.now(self.beijing_tz)
        date_str = now.strftime("%Y年%m月%d日")

        # 分离已完成和即将进行的比赛
        completed_matches = [m for m in matches if m.status == MatchStatus.COMPLETED]
        upcoming_matches = [m for m in matches if m.status == MatchStatus.UPCOMING]

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CS2 每日资讯</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .date {{
            font-size: 16px;
            opacity: 0.9;
        }}
        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}
        .section:last-child {{
            border-bottom: none;
        }}
        .section-title {{
            font-size: 22px;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .match-item {{
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .match-tournament {{
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }}
        .match-teams {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 16px;
            font-weight: 600;
        }}
        .match-score {{
            font-size: 18px;
            color: #667eea;
        }}
        .match-time {{
            font-size: 12px;
            color: #999;
            margin-top: 5px;
        }}
        .news-item {{
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }}
        .news-title {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }}
        .news-title a {{
            color: #667eea;
            text-decoration: none;
        }}
        .news-title a:hover {{
            text-decoration: underline;
        }}
        .news-content {{
            font-size: 14px;
            color: #666;
            line-height: 1.8;
        }}
        .news-meta {{
            font-size: 12px;
            color: #999;
            margin-top: 8px;
        }}
        .empty {{
            text-align: center;
            color: #999;
            padding: 20px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            background-color: #f9f9f9;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 CS2 每日资讯</h1>
            <p class="date">{date_str}</p>
        </div>

        {self._format_completed_section(completed_matches)}
        {self._format_upcoming_section(upcoming_matches)}
        {self._format_news_section(news)}

        <div class="footer">
            <p>本邮件由 GitHub Actions 自动发送</p>
        </div>
    </div>
</body>
</html>"""
        return html

    def _format_completed_section(self, matches: List[Match]) -> str:
        """格式化已完成比赛部分"""
        if not matches:
            return ""

        matches_html = "\n".join(self._format_completed_match(m) for m in matches)

        return f"""        <div class="section">
            <h2 class="section-title">🏆 今日比赛结果</h2>
            {matches_html}
        </div>"""

    def _format_completed_match(self, match: Match) -> str:
        """格式化单个已完成比赛"""
        return f"""            <div class="match-item">
                <div class="match-tournament">{match.tournament}</div>
                <div class="match-teams">
                    <span>{match.team1}</span>
                    <span class="match-score">{match.score1} - {match.score2}</span>
                    <span>{match.team2}</span>
                </div>
                <div class="match-time">{match.format_date()} {match.format_time()}</div>
            </div>"""

    def _format_upcoming_section(self, matches: List[Match]) -> str:
        """格式化即将进行的比赛部分"""
        if not matches:
            return ""

        matches_html = "\n".join(self._format_upcoming_match(m) for m in matches)

        return f"""        <div class="section">
            <h2 class="section-title">📅 即将进行的比赛</h2>
            {matches_html}
        </div>"""

    def _format_upcoming_match(self, match: Match) -> str:
        """格式化单个即将进行的比赛"""
        return f"""            <div class="match-item" style="border-left-color: #f39c12;">
                <div class="match-tournament">{match.tournament}</div>
                <div class="match-teams">
                    <span>{match.team1}</span>
                    <span class="match-score">VS</span>
                    <span>{match.team2}</span>
                </div>
                <div class="match-time">{match.format_date()} {match.format_time()}</div>
            </div>"""

    def _format_news_section(self, news: List[Dict[str, str]]) -> str:
        """格式化新闻部分"""
        if not news:
            return ""

        news_html = "\n".join(self._format_news_item(n) for n in news)

        return f"""        <div class="section">
            <h2 class="section-title">📝 游戏更新</h2>
            {news_html}
        </div>"""

    def _format_news_item(self, news_item: Dict[str, str]) -> str:
        """格式化单个新闻"""
        from datetime import datetime
        date_time = datetime.fromtimestamp(news_item.get('date', 0))

        return f"""            <div class="news-item">
                <div class="news-title">
                    <a href="{news_item.get('url', '#')}" target="_blank">{news_item.get('title', '未知标题')}</a>
                </div>
                <div class="news-content">{news_item.get('content', '无内容')}</div>
                <div class="news-meta">{date_time.strftime('%Y-%m-%d %H:%M')} | {news_item.get('author', '未知作者')}</div>
            </div>"""
