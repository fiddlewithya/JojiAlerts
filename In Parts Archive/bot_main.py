# bot_main.py
import telebot
from datetime import datetime, timedelta
from api_requests import fetch_calendar_data, fetch_earnings_for_symbol
from formatting import format_calendar_data, format_earnings_search

# Replace with your actual tokens
API_TOKEN = '7691675271:AAHWZYZlXnaPb7IDc1BYuwDiMqOHPOmGVhI'
bot = telebot.TeleBot(API_TOKEN)

# Command: /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Welcome! Use /earnings, /ipo, /dividends, or /search <symbol> to get the latest calendar information."
    )

# Command: /earnings
@bot.message_handler(commands=['earnings'])
def send_earnings(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_calendar_data('https://finnhub.io/api/v1/calendar/earnings', today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'earnings'), parse_mode="Markdown")

# Command: /ipo
@bot.message_handler(commands=['ipo'])
def send_ipos(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_calendar_data('https://finnhub.io/api/v1/calendar/ipo', today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'ipo'), parse_mode="Markdown")

# Command: /dividends
@bot.message_handler(commands=['dividends'])
def send_dividends(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_calendar_data('https://finnhub.io/api/v1/calendar/dividends', today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'dividends'), parse_mode="Markdown")

# Command: /search <symbol>
@bot.message_handler(commands=['search'])
def search_earnings(message):
    try:
        symbol = message.text.split()[1].upper()
    except IndexError:
        bot.send_message(message.chat.id, "Please provide a stock symbol. Example: /search AAPL")
        return
    
    data = fetch_earnings_for_symbol(symbol)
    bot.send_message(message.chat.id, format_earnings_search(data), parse_mode="Markdown")

# Run the bot
bot.polling()
