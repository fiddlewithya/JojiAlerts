# JojiAlerts Telegram Bot

JojiAlerts is a Telegram bot that provides users with financial updates on upcoming earnings reports, IPO calendars, and dividend announcements for specific stock symbols. The bot uses the Finnhub API to gather real-time data and presents it in a Telegram-friendly format.

## Features

### Implemented Commands

- **/start** - Sends a welcome message and lists available commands.
- **/earning** - Displays a list of upcoming earnings reports.
- **/ipo** - Shows upcoming IPOs.
- **/dividends** - Lists upcoming dividend announcements.
- **/search <symbol>** - Allows users to search for the next earnings report date of a specific stock symbol.

### Requirements

- **Telegram API Token** - For bot integration on Telegram.
- **Finnhub API Key** - To access financial data such as earnings reports, IPOs, and dividends.

### Future Improvements

- **Daily Scheduled Updates**: Implement a scheduled feature to automatically send daily updates on specific earnings or IPOs.
- **Inline Query Support**: Add support for inline queries to make the bot interactive and responsive in group chats without specific commands.
- **Error Handling Enhancements**: Improve error handling to handle API downtime or data unavailability gracefully.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/JojiAlerts.git


Navigate to the project directory:

bash
Copy code
cd JojiAlerts
Install dependencies (e.g., requests and pyTelegramBotAPI):

bash
Copy code
pip install requests pyTelegramBotAPI
Set up your API tokens in bot_script.py.

Run the bot:

bash
Copy code
python bot_script.py
Usage
To interact with the bot, use the following commands in a Telegram chat:

/start - To see the welcome message.
/earning - To view upcoming earnings reports.
/ipo - To see upcoming IPOs.
/dividends - To check upcoming dividends.
/search <symbol> - To search for a specific stock's earnings report.

This bot is currently in development and can be expanded with more financial tools and features to provide an even richer experience for users.

