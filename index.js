require('dotenv').config();
const nodemailer = require('nodemailer');
const { HLTV } = require('hltv-api');

/**
 * Logger utility
 */
const logger = {
  info: (message) => console.log(`[INFO] ${new Date().toISOString()} - ${message}`),
  error: (message, error) => console.error(`[ERROR] ${new Date().toISOString()} - ${message}`, error?.message || error),
  success: (message) => console.log(`[SUCCESS] ${new Date().toISOString()} - ${message}`)
};

/**
 * Fetch CS2 news from HLTV API
 * @returns {Promise<Array>}
 */
async function fetchCS2News() {
  try {
    logger.info('Fetching CS2 news from HLTV API...');

    const news = await HLTV.getNews();

    // Format news items
    const formattedNews = news.slice(0, 10).map(item => ({
      id: item.id || Date.now().toString(),
      title: item.title || 'No title',
      url: item.link || `https://www.hltv.org/news/${item.id || ''}`,
      date: new Date().toISOString()
    }));

    logger.success(`Fetched ${formattedNews.length} news items`);
    return formattedNews;
  } catch (error) {
    logger.error('Failed to fetch CS2 news', error);
    return [];
  }
}

/**
 * Fetch matches from HLTV API
 * @returns {Promise<Array>}
 */
async function fetchMatches() {
  try {
    logger.info('Fetching CS2 matches from HLTV API...');

    // Get live matches
    const liveMatches = await HLTV.getMatches({ pages: 1 });

    // Get upcoming matches
    const upcomingMatches = await HLTV.getMatches({ pages: 1 });

    // Format match items
    const formattedMatches = [];

    // Process live matches
    if (liveMatches && Array.isArray(liveMatches)) {
      for (const match of liveMatches.slice(0, 5)) {
        if (match.live) {
          formattedMatches.push({
            id: match.id || Date.now().toString(),
            team1: match.team1?.name || 'Unknown',
            team2: match.team2?.name || 'Unknown',
            mapInfo: match.maps?.map(m => m.name).join(', ') || 'Live now',
            status: 'LIVE',
            url: match.link || `https://www.hltv.org/matches/${match.id || ''}`
          });
        }
      }
    }

    // Process upcoming matches
    if (upcomingMatches && Array.isArray(upcomingMatches)) {
      const upcoming = upcomingMatches
        .filter(m => !m.live && m.event)
        .slice(0, 5);

      for (const match of upcoming) {
        formattedMatches.push({
          id: match.id || Date.now().toString(),
          team1: match.team1?.name || 'Unknown',
          team2: match.team2?.name || 'Unknown',
          mapInfo: match.date ? new Date(match.date).toLocaleDateString('zh-CN') : 'Upcoming',
          status: 'UPCOMING',
          url: match.link || `https://www.hltv.org/matches/${match.id || ''}`
        });
      }
    }

    logger.success(`Fetched ${formattedMatches.length} matches`);
    return formattedMatches;
  } catch (error) {
    logger.error('Failed to fetch matches', error);
    return [];
  }
}

/**
 * Generate HTML email content
 * @param {Array} news - News items
 * @param {Array} matches - Match items
 * @returns {string}
 */
function generateEmailContent(news, matches) {
  const date = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });

  let content = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .container {
      background-color: #ffffff;
      border-radius: 8px;
      padding: 30px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header {
      text-align: center;
      padding-bottom: 20px;
      border-bottom: 2px solid #ff6b00;
      margin-bottom: 20px;
    }
    .header h1 {
      color: #ff6b00;
      margin: 0;
      font-size: 28px;
    }
    .date {
      color: #666;
      margin-top: 10px;
      font-size: 14px;
    }
    .section {
      margin-bottom: 30px;
    }
    .section h2 {
      color: #ff6b00;
      border-left: 4px solid #ff6b00;
      padding-left: 10px;
      margin-bottom: 15px;
    }
    .news-item {
      padding: 15px;
      margin-bottom: 10px;
      background-color: #f9f9f9;
      border-radius: 4px;
      border-left: 3px solid #ddd;
    }
    .news-item:hover {
      border-left-color: #ff6b00;
      background-color: #fff;
    }
    .news-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 5px;
    }
    .news-link {
      color: #ff6b00;
      text-decoration: none;
    }
    .news-link:hover {
      text-decoration: underline;
    }
    .match-item {
      padding: 15px;
      margin-bottom: 10px;
      background-color: ${matches.length > 0 ? '#f0f8ff' : '#f9f9f9'};
      border-radius: 4px;
      border-left: 3px solid ${matches.length > 0 ? '#00ff00' : '#ddd'};
    }
    .match-live {
      display: inline-block;
      background-color: #ff0000;
      color: white;
      padding: 2px 8px;
      border-radius: 3px;
      font-size: 12px;
      font-weight: bold;
      margin-right: 10px;
    }
    .match-upcoming {
      display: inline-block;
      background-color: #00a8ff;
      color: white;
      padding: 2px 8px;
      border-radius: 3px;
      font-size: 12px;
      font-weight: bold;
      margin-right: 10px;
    }
    .match-teams {
      font-size: 16px;
      font-weight: 600;
      margin-top: 5px;
    }
    .match-map {
      color: #666;
      font-size: 14px;
      margin-top: 3px;
    }
    .match-link {
      color: #ff6b00;
      text-decoration: none;
      font-size: 12px;
    }
    .footer {
      text-align: center;
      padding-top: 20px;
      border-top: 1px solid #ddd;
      margin-top: 30px;
      color: #666;
      font-size: 12px;
    }
    .no-data {
      color: #999;
      font-style: italic;
      padding: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎮 CS2 每日资讯</h1>
      <p class="date">${date}</p>
    </div>
`;

  // Add news section
  content += `
    <div class="section">
      <h2>📰 每日新闻</h2>
`;
  if (news.length > 0) {
    news.forEach(item => {
      content += `
      <div class="news-item">
        <div class="news-title">
          <a href="${item.url}" class="news-link">${item.title}</a>
        </div>
      </div>
`;
    });
  } else {
    content += `<p class="no-data">暂无新闻数据</p>`;
  }
  content += `    </div>
`;

  // Add matches section
  content += `
    <div class="section">
      <h2>⚔️ 赛事进程</h2>
`;
  if (matches.length > 0) {
    matches.forEach(item => {
      const statusBadge = item.status === 'LIVE'
        ? '<span class="match-live">LIVE</span>'
        : '<span class="match-upcoming">UPCOMING</span>';
      content += `
      <div class="match-item">
        ${statusBadge}
        <div class="match-teams">${item.team1} vs ${item.team2}</div>
        <div class="match-map">${item.mapInfo}</div>
        <a href="${item.url}" class="match-link">查看详情 &rarr;</a>
      </div>
`;
    });
  } else {
    content += `<p class="no-data">暂无比赛数据</p>`;
  }
  content += `    </div>
`;

  // Add footer
  content += `
    <div class="footer">
      <p>本邮件由 CS2 Daily News 自动发送 | 数据来源: HLTV</p>
      <p>如需取消订阅，请联系管理员</p>
    </div>
  </div>
</body>
</html>
`;

  return content;
}

/**
 * Send email via SMTP
 * @param {string} subject - Email subject
 * @param {string} htmlContent - HTML content
 * @returns {Promise<void>}
 */
async function sendEmail(subject, htmlContent) {
  try {
    logger.info('Creating email transporter...');

    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASSWORD
      },
      tls: {
        rejectUnauthorized: false
      }
    });

    // Verify connection
    await transporter.verify();
    logger.success('SMTP connection verified');

    const recipients = process.env.EMAIL_TO.split(',').map(e => e.trim());

    logger.info(`Sending email to ${recipients.length} recipient(s)...`);

    const mailOptions = {
      from: process.env.EMAIL_FROM || process.env.SMTP_USER,
      to: recipients.join(', '),
      subject: subject,
      html: htmlContent
    };

    const info = await transporter.sendMail(mailOptions);
    logger.success(`Email sent successfully! Message ID: ${info.messageId}`);
  } catch (error) {
    logger.error('Failed to send email', error);
    throw error;
  }
}

/**
 * Main function
 */
async function main() {
  try {
    logger.info('Starting CS2 Daily News job...');

    // Fetch news and matches
    const news = await fetchCS2News();
    const matches = await fetchMatches();

    if (news.length === 0 && matches.length === 0) {
      logger.info('No data fetched, skipping email');
      return;
    }

    // Generate email content
    const emailContent = generateEmailContent(news, matches);

    // Send email
    const date = new Date().toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    const subject = `[CS2 每日资讯] ${date}`;

    await sendEmail(subject, emailContent);

    logger.success('Job completed successfully!');
  } catch (error) {
    logger.error('Job failed', error);
    process.exit(1);
  }
}

// Run the job
if (require.main === module) {
  main();
}

module.exports = { main, fetchCS2News, fetchMatches, generateEmailContent };
