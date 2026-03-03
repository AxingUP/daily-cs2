"""
HLTV 爬虫
获取 CS2 赛事数据和赛程信息
"""
from datetime import datetime, date
from typing import List, Optional
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper
from ..models.match import Match, MatchStatus


class HLTVScraper(BaseScraper):
    """HLTV 爬虫"""

    def __init__(self, base_url: str = "https://hltv.org"):
        super().__init__()
        self.base_url = base_url

    def get_today_matches(self) -> List[Match]:
        """
        获取今日比赛数据

        Returns:
            比赛列表
        """
        matches = []

        # 获取今日比赛结果
        try:
            results = self._fetch_results()
            matches.extend(results)
        except Exception as e:
            print(f"获取比赛结果失败: {e}")

        # 获取即将进行的比赛
        try:
            upcoming = self._fetch_upcoming()
            matches.extend(upcoming)
        except Exception as e:
            print(f"获取即将进行的比赛失败: {e}")

        return matches

    def _fetch_results(self) -> List[Match]:
        """获取已完成的比赛结果"""
        matches = []
        url = f"{self.base_url}/results"

        try:
            response = self.get(url)
            soup = BeautifulSoup(response.text, 'lxml')

            # 查找比赛结果行
            result_rows = soup.select('a.result-con')

            for row in result_rows[:10]:  # 获取最新10场比赛
                try:
                    match = self._parse_result_row(row)
                    if match and self._is_today(match.time):
                        matches.append(match)
                except Exception as e:
                    print(f"解析比赛结果失败: {e}")
                    continue

        except Exception as e:
            print(f"获取比赛结果页面失败: {e}")

        return matches

    def _fetch_upcoming(self) -> List[Match]:
        """获取即将进行的比赛"""
        matches = []
        url = f"{self.base_url}/matches"

        try:
            response = self.get(url)
            soup = BeautifulSoup(response.text, 'lxml')

            # 查找即将进行的比赛
            upcoming_matches = soup.select('a.match-match')

            for match_div in upcoming_matches[:10]:  # 获取即将进行的10场比赛
                try:
                    match = self._parse_upcoming_match(match_div)
                    if match:
                        matches.append(match)
                except Exception as e:
                    print(f"解析即将进行的比赛失败: {e}")
                    continue

        except Exception as e:
            print(f"获取即将进行的比赛页面失败: {e}")

        return matches

    def _parse_result_row(self, row) -> Optional[Match]:
        """解析比赛结果行"""
        # 获取赛事名称
        tournament_elem = row.select_one('span.event-name')
        tournament = tournament_elem.text.strip() if tournament_elem else "未知赛事"

        # 获取队伍和比分
        team1_elem = row.select_one('div.team1 .team')
        team2_elem = row.select_one('div.team2 .team')
        score1_elem = row.select_one('div.team1 .score')
        score2_elem = row.select_one('div.team2 .score')

        if not team1_elem or not team2_elem:
            return None

        team1 = team1_elem.text.strip()
        team2 = team2_elem.text.strip()
        score1 = int(score1_elem.text.strip()) if score1_elem else None
        score2 = int(score2_elem.text.strip()) if score2_elem else None

        # 获取比赛时间
        time_elem = row.select_one('div.time')
        match_time = None
        if time_elem:
            time_str = time_elem.get('data-unix')
            if time_str:
                match_time = datetime.fromtimestamp(int(time_str) // 1000)

        return Match(
            tournament=tournament,
            team1=team1,
            team2=team2,
            time=match_time,
            score1=score1,
            score2=score2,
            status=MatchStatus.COMPLETED
        )

    def _parse_upcoming_match(self, match_div) -> Optional[Match]:
        """解析即将进行的比赛"""
        # 获取赛事名称
        tournament_elem = match_div.select_one('td.time-event .event-name')
        tournament = tournament_elem.text.strip() if tournament_elem else "未知赛事"

        # 获取队伍
        teams = match_div.select('td.team-cell .team')
        if len(teams) < 2:
            return None

        team1 = teams[0].text.strip()
        team2 = teams[1].text.strip()

        # 获取比赛时间
        time_elem = match_div.select_one('.time')
        match_time = None
        if time_elem:
            time_str = time_elem.get('data-unix')
            if time_str:
                match_time = datetime.fromtimestamp(int(time_str) // 1000)

        return Match(
            tournament=tournament,
            team1=team1,
            team2=team2,
            time=match_time,
            score1=None,
            score2=None,
            status=MatchStatus.UPCOMING
        )

    def _is_today(self, match_time: Optional[datetime]) -> bool:
        """检查比赛是否在今天"""
        if not match_time:
            return False
        return match_time.date() == date.today()
