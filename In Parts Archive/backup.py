import telebot
import requests
from datetime import datetime, timedelta

# Telegram Bot API Token (replace with your actual token)
API_TOKEN = '7691675271:AAHWZYZlXnaPb7IDc1BYuwDiMqOHPOmGVhI'
bot = telebot.TeleBot(API_TOKEN)

# Finnhub API Key (replace with your actual API key)
FINNHUB_API_KEY = 'csq6po9r01qj9q8nbo3gcsq6po9r01qj9q8nbo40'

# Finnhub API URLs
FINNHUB_API_URLS = {
    'earnings': f'https://finnhub.io/api/v1/calendar/earnings?token={FINNHUB_API_KEY}',
    'ipo': f'https://finnhub.io/api/v1/calendar/ipo?token={FINNHUB_API_KEY}',
    'dividends': f'https://finnhub.io/api/v1/calendar/dividends?token={FINNHUB_API_KEY}'
}

def fetch_finnhub_data(url, start_date, end_date):
    """
    Fetches data from Finnhub API for a specific calendar type.
    """
    response = requests.get(url, params={'from': start_date, 'to': end_date})
    data = response.json()
    return data.get('earningsCalendar', []) if 'earnings' in url else data.get('ipoCalendar', [])

def format_calendar_data(data, calendar_type):
    """
    Formats data for display in Telegram.
    """
    if calendar_type == 'earnings':
        message = "📅 Upcoming Earnings Reports:\n\n"
        for entry in data[:10]:  # Limit to 10 entries
            date = entry.get('date')
            message += (f"Company: {entry.get('symbol')}\n"
                        f"Date: {date}\n"
                        f"Time: {entry.get('hour', 'N/A')}\n"
                        f"EPS Estimate: {entry.get('epsEstimate', 'N/A')}\n\n")
    elif calendar_type == 'ipo':
        message = "📅 Upcoming IPOs:\n\n"
        for entry in data[:10]:
            date = entry.get('date')
            message += (f"Company: {entry.get('symbol')}\n"
                        f"Date: {date}\n"
                        f"Exchange: {entry.get('exchange')}\n"
                        f"Price: {entry.get('price', 'N/A')}\n\n")
    else:
        message = "📅 Upcoming Dividends:\n\n"
        for entry in data[:10]:
            date = entry.get('date')
            message += (f"Company: {entry.get('symbol')}\n"
                        f"Date: {date}\n"
                        f"Dividend: {entry.get('amount', 'N/A')}\n\n")
    return message

# Define bot commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Welcome! Use /earnings, /ipo, or /dividends to get the latest calendar information."
    )

@bot.message_handler(commands=['earnings'])
def send_earnings(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_finnhub_data(FINNHUB_API_URLS['earnings'], today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'earnings'))

@bot.message_handler(commands=['ipo'])
def send_ipos(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_finnhub_data(FINNHUB_API_URLS['ipo'], today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'ipo'))

@bot.message_handler(commands=['dividends'])
def send_dividends(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_finnhub_data(FINNHUB_API_URLS['dividends'], today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'dividends'))

# Run the bot
bot.polling()
