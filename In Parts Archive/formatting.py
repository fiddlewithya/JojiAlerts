# formatting.py

def format_calendar_data(data, calendar_type):
    """
    Formats data for display in Telegram as a table.
    """
    if calendar_type == 'earnings':
        message = "📅 *Upcoming Earnings Reports*\n\n"
        message += "`{:<10} {:<15} {:<10} {:<10}`\n".format("Symbol", "Date", "Time", "EPS Estimate")
        message += "`{:<10} {:<15} {:<10} {:<10}`\n".format("------", "----------", "------", "-------------")
        
        for entry in data[:10]:  # Limit to first 10 entries
            symbol = entry.get('symbol', 'N/A')[:10]
            date = entry.get('date', 'N/A')[:15]
            time = entry.get('hour', 'N/A')[:10]
            eps = str(entry.get('epsEstimate', 'N/A'))[:10]
            message += "`{:<10} {:<15} {:<10} {:<10}`\n".format(symbol, date, time, eps)
    return message

def format_earnings_search(data):
    """
    Formats the earnings report data for a single stock symbol search.
    """
    if not data:
        return "No upcoming earnings report found for this symbol."

    # Display the latest available earnings report data
    report = data[0]
    message = f"*Earnings Report for {report.get('symbol', 'N/A')}*\n"
    message += f"Date: {report.get('period', 'N/A')}\n"
    message += f"Actual EPS: {report.get('actual', 'N/A')}\n"
    message += f"Estimate EPS: {report.get('estimate', 'N/A')}\n"
    return message
