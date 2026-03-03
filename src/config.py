"""
配置管理模块
从环境变量读取配置信息
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class EmailConfig:
    """邮件配置"""
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.qq.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    email: str = os.getenv("QQ_EMAIL", "")
    auth_code: str = os.getenv("QQ_AUTH_CODE", "")
    to_emails: list[str] = field(default_factory=list)

    def __post_init__(self):
        """在实例化后初始化收件人邮箱列表"""
        to_email_str = os.getenv("TO_EMAIL", "")
        if to_email_str:
            # 支持逗号或分号分隔的邮箱
            emails = [e.strip() for e in to_email_str.replace(';', ',').split(',')]
            self.to_emails = [e for e in emails if e]


@dataclass
class Config:
    """全局配置"""
    email: EmailConfig = field(default_factory=EmailConfig)
    hltv_base_url: str = os.getenv("HLTV_BASE_URL", "https://hltv.org")
    steam_app_id: int = int(os.getenv("STEAM_APP_ID", "730"))


def load_config() -> Config:
    """加载配置"""
    return Config()
