# api_requests.py
import requests

FINNHUB_API_KEY = 'csq6po9r01qj9q8nbo3gcsq6po9r01qj9q8nbo40'
FINNHUB_API_URLS = {
    'earnings': f'https://finnhub.io/api/v1/calendar/earnings?token={FINNHUB_API_KEY}',
    'ipo': f'https://finnhub.io/api/v1/calendar/ipo?token={FINNHUB_API_KEY}',
    'dividends': f'https://finnhub.io/api/v1/calendar/dividends?token={FINNHUB_API_KEY}',
    'symbol_earnings': 'https://finnhub.io/api/v1/stock/earnings'
}

def fetch_calendar_data(url, start_date=None, end_date=None, params=None):
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
    url = f"{FINNHUB_API_URLS['symbol_earnings']}?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    return response.json()
