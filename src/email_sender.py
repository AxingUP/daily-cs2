"""
邮件发送模块
使用 SMTP 协议发送邮件
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional
import time

from .config import EmailConfig


class EmailSender:
    """邮件发送器"""

    def __init__(self, config: EmailConfig):
        self.config = config
        self.max_retries = 3
        self.retry_delay = 5

    def send_email(self, content: str, subject: str = None) -> bool:
        """
        发送邮件

        Args:
            content: 邮件内容（HTML格式）
            subject: 邮件主题

        Returns:
            发送是否成功
        """
        if not subject:
            from datetime import datetime
            import pytz
            beijing_tz = pytz.timezone('Asia/Shanghai')
            now = datetime.now(beijing_tz)
            subject = f"CS2 每日资讯 - {now.strftime('%Y-%m-%d')}"

        for attempt in range(self.max_retries):
            try:
                return self._send_once(content, subject)
            except Exception as e:
                print(f"邮件发送失败（尝试 {attempt + 1}/{self.max_retries}）: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print("已达到最大重试次数，邮件发送失败")
                    return False

    def _send_once(self, content: str, subject: str) -> bool:
        """执行一次邮件发送"""
        if not self.config.to_emails:
            print("错误：未配置收件人邮箱")
            return False

        # 创建邮件对象
        message = MIMEMultipart('alternative')
        message['From'] = Header(self.config.email)
        message['To'] = Header(', '.join(self.config.to_emails), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')

        # 添加 HTML 内容
        html_part = MIMEText(content, 'html', 'utf-8')
        message.attach(html_part)

        # 连接 SMTP 服务器
        if self.config.smtp_port == 465:
            # SSL 连接
            server = smtplib.SMTP_SSL(self.config.smtp_server, self.config.smtp_port)
        else:
            # TLS 连接
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()

        # 登录并发送
        server.login(self.config.email, self.config.auth_code)
        server.sendmail(self.config.email, self.config.to_emails, message.as_string())
        server.quit()

        print(f"邮件发送成功，收件人: {', '.join(self.config.to_emails)}")
        return True
