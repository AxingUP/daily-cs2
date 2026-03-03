"""
比赛数据模型
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MatchStatus(Enum):
    """比赛状态"""
    COMPLETED = "completed"  # 已完成
    UPCOMING = "upcoming"    # 即将进行
    LIVE = "live"            # 进行中


@dataclass
class Match:
    """比赛数据"""
    tournament: str      # 赛事名称
    team1: str           # 队伍1
    team2: str           # 队伍2
    time: datetime       # 比赛时间
    score1: int | None   # 队伍1得分
    score2: int | None   # 队伍2得分
    status: MatchStatus  # 状态

    def format_time(self) -> str:
        """格式化时间"""
        if self.time:
            return self.time.strftime("%H:%M")
        return "--:--"

    def format_date(self) -> str:
        """格式化日期"""
        if self.time:
            return self.time.strftime("%Y-%m-%d")
        return "未知"

    def __str__(self) -> str:
        """字符串表示"""
        score_str = f"{self.score1}:{self.score2}" if self.score1 is not None else "VS"
        return f"{self.tournament} | {self.team1} {score_str} {self.team2}"
