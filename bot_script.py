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

# Finnhub API URLs
FINNHUB_API_URLS = {
    'earnings': f'https://finnhub.io/api/v1/calendar/earnings?token={FINNHUB_API_KEY}',
    'ipo': f'https://finnhub.io/api/v1/calendar/ipo?token={FINNHUB_API_KEY}',
    'dividends': f'https://finnhub.io/api/v1/calendar/dividends?token={FINNHUB_API_KEY}',
    'symbol_earnings': 'https://finnhub.io/api/v1/stock/earnings'
}

def fetch_calendar_data(url, start_date=None, end_date=None, params=None):
    """
    Fetches data from Finnhub API for a specific calendar type.
    """
    if params is None:
        params = {}
    if start_date and end_date:
        params.update({'from': start_date, 'to': end_date})
    response = requests.get(url, params=params)
    data = response.json()
    # Return the appropriate list based on the URL
    if 'earnings' in url:
        return data.get('earningsCalendar', [])
    elif 'ipo' in url:
        return data.get('ipoCalendar', [])
    elif 'dividends' in url:
        return data.get('dividendsCalendar', [])
    return []

def fetch_earnings_for_symbol(symbol):
    """
    Fetches the next earnings report data for a specific stock symbol.
    """
    url = f"{FINNHUB_API_URLS['symbol_earnings']}?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    return response.json()

def format_calendar_data(data, calendar_type):
    """
    Formats data for display in Telegram as a list.
    """
    if not isinstance(data, list):
        return "Error: Could not retrieve data. Please try again later."

    message = ""
    if calendar_type == 'earnings':
        message = "📅 *Upcoming Earnings Reports*\n\n"
        for entry in data[:10]:  # Limit to first 10 entries
            symbol = entry.get('symbol', 'N/A')
            date = entry.get('date', 'N/A')
            time = entry.get('hour', 'N/A')
            eps = entry.get('epsEstimate', 'N/A')
            message += f"Symbol: {symbol}\nDate: {date}\nTime: {time}\nEPS: {eps}\n\n"

    elif calendar_type == 'ipo':
        message = "📅 *Upcoming IPOs*\n\n"
        for entry in data[:10]:
            symbol = entry.get('symbol', 'N/A')
            date = entry.get('date', 'N/A')
            exchange = entry.get('exchange', 'N/A')
            price = entry.get('price', 'N/A')
            message += f"Symbol: {symbol}\nDate: {date}\nExchange: {exchange}\nPrice: {price}\n\n"

    elif calendar_type == 'dividends':
        message = "📅 *Upcoming Dividends*\n\n"
        for entry in data[:10]:
            symbol = entry.get('symbol', 'N/A')
            date = entry.get('date', 'N/A')
            dividend = entry.get('amount', 'N/A')
            message += f"Symbol: {symbol}\nDate: {date}\nDividend: {dividend}\n\n"

    return message

def format_earnings_search(data):
    """
    Formats the earnings report data for a single stock symbol search.
    """
    if not data:
        return "No upcoming earnings report found for this symbol."

    # Display the latest available earnings report data
    report = data[0]  # Get the first report from the returned list
    message = f"*Earnings Report for {report.get('symbol', 'N/A')}*\n"
    message += f"Date: {report.get('period', 'N/A')}\n"
    message += f"Actual EPS: {report.get('actual', 'N/A')}\n"
    message += f"Estimate EPS: {report.get('estimate', 'N/A')}\n"
    return message

# Define bot commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Welcome! Use /earning, /ipo, /dividends, or /search <symbol> to get the latest calendar information."
    )

@bot.message_handler(commands=['earning'])
def send_earning(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_calendar_data(FINNHUB_API_URLS['earnings'], today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'earnings'), parse_mode="Markdown")

@bot.message_handler(commands=['ipo'])
def send_ipos(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_calendar_data(FINNHUB_API_URLS['ipo'], today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'ipo'), parse_mode="Markdown")

@bot.message_handler(commands=['dividends'])
def send_dividends(message):
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    data = fetch_calendar_data(FINNHUB_API_URLS['dividends'], today, future_date)
    bot.send_message(message.chat.id, format_calendar_data(data, 'dividends'), parse_mode="Markdown")

@bot.message_handler(commands=['search'])
def search_earnings(message):
    """
    Searches for the next earnings report date for a specific stock symbol.
    """
    try:
        symbol = message.text.split()[1].upper()
    except IndexError:
        bot.send_message(message.chat.id, "Please provide a stock symbol. Example: /search AAPL")
        return
    
    data = fetch_earnings_for_symbol(symbol)
    bot.send_message(message.chat.id, format_earnings_search(data), parse_mode="Markdown")

# Run the bot
bot.polling()