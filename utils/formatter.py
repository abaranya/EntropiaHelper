from datetime import datetime

# Formatting functions
# utils/formatter.py
class Formatter:
    def __init__(self, currency_symbol="PED", date_format="yyyy-MM-dd"):
        self.currency_symbol = currency_symbol
        self.date_format = date_format
        self.layout = []

    def format_currency(self, amount):
        if isinstance(amount, (int, float)):
            return f"{self.currency_symbol} {amount:.2f}"
        return str(amount)  # Return as string if not a number, could also return "N/A" or similar

    def format_percentage(self, percentage):
        if isinstance(percentage, (int, float)):
            return f"{percentage:.2f}%"
        return str(percentage)  # Return as string if not a number, could also return "N/A" or similar

    def format_date(self, date):
        if isinstance(date, datetime):
            return date.strftime(self.date_format)
        return date  # Return empty string if the date is not a datetime instance

    def format_text(self, text):
        return str(text)  # Additional text formatting logic can go here

    def format(self, value, column):
        func = self.layout[column]
        return func(value) if func else str(value)  # Default to str if no specific func

    def setLayout(self, layout):
        self.layout = layout
