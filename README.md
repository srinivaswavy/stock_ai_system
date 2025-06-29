# Yahoo Financ# Print formatted news (also returns data)
apple.print_news(limit=10)

# Get analyst recommendations
recommendations = apple.get_stock_recommendations()
print(recommendations)

# Get comprehensive analysis (returns structured data)
analysis = apple.get_comprehensive_analysis(period="3mo", include_news=True)
print(f"Current price: {analysis['stock_info']['Current Price']}")
print(f"Trend signal: {analysis['technical_analysis']['trend_signal']}")

# Get price statistics (returns data)
stats = apple.get_price_statistics(period="1mo")
print(f"Monthly return: {stats['change_pct']:.2f}%")
```

### 8. Interactive News Analysis:
```python
from stock_news_analyzer import interactive_news_browser
interactive_news_browser()  # Start interactive news browser
```

### 9. Compare Multiple Stocks (Now Returns Data):
```python
from stock_data_analyzer import analyze_multiple_stocks

# Compare tech stocks - now returns structured data
tech_stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]
results = analyze_multiple_stocks(tech_stocks, period="1y", show_chart=False)

# Use the returned data
print(f"Best performer: {results['summary']['best_performer']}")
print(f"Average return: {results['summary']['average_return']:.2f}%")

for stock in results['comparison_data']:
    print(f"{stock['symbol']}: {stock['return_pct']:.2f}%")
```

### 10. Programmatic Data Usage:
```python
# Get data without printing
analyzer = StockAnalyzer("TSLA")

# All these return structured data you can use programmatically:
stock_info = analyzer.get_stock_info()
news_data = analyzer.get_news(limit=5)
price_stats = analyzer.get_price_statistics(period="1mo")
comprehensive = analyzer.get_comprehensive_analysis()

# Save to JSON, database, or use in your application
import json
with open('stock_analysis.json', 'w') as f:
    json.dump(comprehensive, f, indent=2, default=str)
```

### 11. Compare Multiple Stocks:alyzer

A c### 2. Run the Simple Interactive Example:
`# Get custom date range
custom_data = apple.get_custom_date_range("2024-01-01", "2024-12-31")

# Get latest news
news = apple.get_news(limit=5)
for article in news:
    print(f"Title: {article['title']}")
    print(f"Publisher: {article['publisher']}")
    print(f"Link: {article['link']}")
    print()

# Print formatted news
apple.print_news(limit=10)

# Get analyst recommendations
recommendations = apple.get_stock_recommendations()
print(recommendations)
```

### 6. Interactive News Analysis:
```python
from stock_news_analyzer import interactive_news_browser
interactive_news_browser()  # Start interactive news browser
```

### 7. Compare Multiple Stocks:ershell
python simple_stock_example.py
```

### 3. Run the Enhanced Analyzer (Recommended):
```powershell
python enhanced_stock_analyzer.py
```

### 4. Run the News Analyzer:
```powershell
python stock_news_analyzer.py
```

### 5. Use the Main Analyzer Script:
```powershell
python stock_data_analyzer.py
```

### 6. Programmatic Usage Examples:
```powershell
python programmatic_usage_example.py
```

### 7. In Your Own Script:e Python toolkit for fetching and analyzing stock data using the Yahoo Finance API.

## Files in this project:

1. **`stock_data_analyzer.py`** - Main comprehensive stock analysis class with return data
2. **`simple_stock_example.py`** - Simple interactive example script with charts
3. **`enhanced_stock_analyzer.py`** - Advanced analyzer with full news and automatic charts
4. **`programmatic_usage_example.py`** - **NEW** - Examples of using returned data programmatically
5. **`stock_news_analyzer.py`** - Dedicated news analysis script with interactive features
6. **`test_data_availability.py`** - Test script to check data availability
7. **`requirements.txt`** - Python package dependencies

## Features

### StockAnalyzer Class Features:
- **Stock Information**: Get basic company info, current price, market cap, P/E ratio, etc.
- **Historical Data**: Fetch historical stock prices with customizable periods and intervals
- **Latest News**: Get real-time news articles with **FULL summaries** (no truncation)
- **Price Charts**: Generate beautiful price charts with optional saving
- **Volume Analysis**: Advanced volume charts with price correlation
- **Moving Averages**: Calculate and plot moving averages (20, 50, 200 day)
- **Technical Analysis**: Support/resistance levels, trend analysis
- **Financial Data**: Access income statements, balance sheets, and cash flow data
- **Dividend Data**: Get dividend history
- **Analyst Recommendations**: Get current analyst ratings and recommendations
- **Calendar Events**: Get upcoming earnings dates and other important events
- **Multi-Stock Comparison**: Compare performance of multiple stocks
- **🔥 PROGRAMMATIC USAGE**: **ALL functions now return structured data** for use in other applications

### Supported Time Periods:
- `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

### Supported Data Intervals:
- `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

## Installation

The required packages are already installed in your virtual environment. If you need to reinstall them:

```powershell
pip install -r requirements.txt
```

## Usage Examples

### 1. Run the Simple Interactive Example:
```powershell
python simple_stock_example.py
```

### 2. Use the Main Analyzer Script:
```powershell
python stock_data_analyzer.py
```

### 3. In Your Own Script:
```python
from stock_data_analyzer import StockAnalyzer

# Analyze a single stock
apple = StockAnalyzer("AAPL")

# Get basic info
apple.print_summary()

# Get historical data
data = apple.get_historical_data(period="1y")
print(data.head())

# Plot price chart
apple.plot_price_chart(period="6mo", save_chart=True)

# Plot with moving averages
apple.plot_with_moving_averages(period="1y", windows=[20, 50, 200])

# Get custom date range
custom_data = apple.get_custom_date_range("2024-01-01", "2024-12-31")
```

### 4. Compare Multiple Stocks:
```python
from stock_data_analyzer import analyze_multiple_stocks

# Compare tech stocks
tech_stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]
analyze_multiple_stocks(tech_stocks, period="1y")
```

## Popular Stock Symbols to Try:

**Technology:**
- AAPL (Apple)
- GOOGL (Google/Alphabet)
- MSFT (Microsoft)
- AMZN (Amazon)
- TSLA (Tesla)
- NVDA (NVIDIA)

**Finance:**
- JPM (JPMorgan Chase)
- BAC (Bank of America)
- WFC (Wells Fargo)

**Market Indices:**
- ^GSPC (S&P 500)
- ^DJI (Dow Jones)
- ^IXIC (NASDAQ)

## Chart Features

The analyzer can generate:
- **Price Charts**: Clean line charts showing stock price over time
- **Moving Average Charts**: Price with overlaid moving averages (20, 50, 200-day)
- **Volume Analysis Charts**: Price and volume correlation with color-coded bars
- **Comparison Charts**: Multiple stocks normalized for performance comparison
- **Technical Analysis Charts**: Support/resistance levels and trend indicators
- **High-Quality Exports**: Save charts as PNG files with 300 DPI resolution
- **Automatic Chart Generation**: Enhanced analyzer shows charts automatically

## Data Available

- **Price Data**: Open, High, Low, Close, Volume
- **Company Info**: Market cap, P/E ratio, dividend yield, sector, industry
- **Latest News**: Real-time news articles with **COMPLETE summaries** (no truncation)
- **Financial Statements**: Income statement, balance sheet, cash flow
- **Analyst Data**: Recommendations, price targets, ratings with percentages
- **Corporate Events**: Earnings dates, dividend dates, and other calendar events
- **Dividends**: Historical dividend payments
- **Technical Indicators**: Moving averages, price changes, trend analysis
- **Volume Analysis**: Daily volume with price correlation

## Notes

- Data is provided by Yahoo Finance and is subject to their terms of service
- Real-time data may have a 15-20 minute delay
- Historical data is generally accurate and comprehensive
- Some financial data may not be available for all stocks
- Charts require matplotlib and will display in separate windows

## Troubleshooting

If you encounter issues:
1. Check that the stock symbol is correct
2. Ensure you have an active internet connection
3. Some data may not be available for delisted or very new stocks
4. Try different time periods if data seems incomplete

Happy analyzing! 📈📊
