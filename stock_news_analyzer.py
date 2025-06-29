"""
Stock News Analyzer
A focused script for fetching and analyzing the latest stock news using Yahoo Finance
"""

from stock_data_analyzer import StockAnalyzer
import webbrowser
from datetime import datetime

def analyze_stock_news(symbol, num_articles=10):
    """
    Analyze and display news for a specific stock
    
    Args:
        symbol (str): Stock ticker symbol
        num_articles (int): Number of news articles to fetch
    """
    print(f"\n{'='*70}")
    print(f"STOCK NEWS ANALYSIS FOR {symbol.upper()}")
    print(f"{'='*70}")
    
    analyzer = StockAnalyzer(symbol)
    
    # Get basic stock info first
    info = analyzer.get_stock_info()
    if info:
        print(f"\nCompany: {info.get('Company Name', 'N/A')}")
        print(f"Current Price: ${info.get('Current Price', 'N/A')}")
        print(f"Sector: {info.get('Sector', 'N/A')}")
    
    # Get and display news
    analyzer.print_news(limit=num_articles)
    
    # Get recommendations if available
    print(f"\n{'='*70}")
    print("ANALYST RECOMMENDATIONS")
    print(f"{'='*70}")
    
    recommendations = analyzer.get_stock_recommendations()
    if recommendations is not None and not recommendations.empty:
        print("\nLatest Analyst Recommendations:")
        print(recommendations.head())
    else:
        print("No analyst recommendations available.")
    
    # Get calendar events
    print(f"\n{'='*70}")
    print("UPCOMING EVENTS")
    print(f"{'='*70}")
    
    calendar = analyzer.get_calendar_events()
    if calendar is not None:
        # Handle different calendar data structures
        if isinstance(calendar, dict):
            print("\nUpcoming Calendar Events:")
            for key, value in calendar.items():
                print(f"{key}: {value}")
        elif hasattr(calendar, 'empty') and not calendar.empty:
            print("\nUpcoming Calendar Events:")
            print(calendar)
        else:
            print("Calendar events data structure not recognized or empty.")
    else:
        print("No upcoming events available.")

def compare_news_sentiment(symbols):
    """
    Compare news sentiment across multiple stocks
    
    Args:
        symbols (list): List of stock ticker symbols
    """
    print(f"\n{'='*80}")
    print("MULTI-STOCK NEWS COMPARISON")
    print(f"{'='*80}")
    
    for symbol in symbols:
        print(f"\n{'-'*60}")
        print(f"NEWS FOR {symbol.upper()}")
        print(f"{'-'*60}")
        
        analyzer = StockAnalyzer(symbol)
        
        # Get basic info
        info = analyzer.get_stock_info()
        if info:
            print(f"Company: {info.get('Company Name', 'N/A')}")
            print(f"Current Price: ${info.get('Current Price', 'N/A')}")
        
        # Get top 3 news articles
        news = analyzer.get_news(limit=3)
        if news:
            print(f"\nTop 3 News Headlines:")
            for i, article in enumerate(news, 1):
                print(f"{i}. {article['title']}")
                print(f"   Date: {article['published_date']}")
                print(f"   Publisher: {article['publisher']}")
                print()
        else:
            print("No news available for this stock.")

def interactive_news_browser():
    """
    Interactive news browser for stocks
    """
    print("Interactive Stock News Browser")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Get news for a single stock")
        print("2. Compare news for multiple stocks")
        print("3. Get detailed news with links")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").strip().upper()
            if symbol:
                num_articles = input("Number of articles (default 5): ").strip()
                num_articles = int(num_articles) if num_articles.isdigit() else 5
                analyze_stock_news(symbol, num_articles)
        
        elif choice == '2':
            symbols_input = input("Enter stock symbols separated by commas: ").strip()
            if symbols_input:
                symbols = [s.strip().upper() for s in symbols_input.split(',')]
                compare_news_sentiment(symbols)
        
        elif choice == '3':
            symbol = input("Enter stock symbol: ").strip().upper()
            if symbol:
                analyzer = StockAnalyzer(symbol)
                news = analyzer.get_news(limit=10)
                
                if news:
                    print(f"\nDetailed news for {symbol}:")
                    for i, article in enumerate(news, 1):
                        print(f"\n{i}. {article['title']}")
                        print(f"   Publisher: {article['publisher']}")
                        print(f"   Date: {article['published_date']}")
                        print(f"   Summary: {article['summary']}")
                        print(f"   Link: {article['link']}")
                        
                        # Option to open link
                        open_link = input("   Open this link in browser? (y/n): ").strip().lower()
                        if open_link == 'y':
                            try:
                                webbrowser.open(article['link'])
                                print("   Link opened in browser.")
                            except:
                                print("   Could not open link.")
                        print("-" * 60)
                else:
                    print(f"No news available for {symbol}")
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

def get_trending_stocks_news():
    """
    Get news for trending/popular stocks
    """
    trending_stocks = [
        "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", 
        "NVDA", "META", "NFLX", "AMD", "INTC"
    ]
    
    print(f"\n{'='*80}")
    print("TRENDING STOCKS NEWS SUMMARY")
    print(f"{'='*80}")
    
    for symbol in trending_stocks:
        print(f"\n{symbol}:")
        print("-" * 20)
        
        analyzer = StockAnalyzer(symbol)
        
        # Get basic info
        info = analyzer.get_stock_info()
        if info:
            current_price = info.get('Current Price', 'N/A')
            company_name = info.get('Company Name', 'N/A')
            print(f"{company_name} - ${current_price}")
        
        # Get top news headline
        news = analyzer.get_news(limit=1)
        if news:
            article = news[0]
            print(f"Latest: {article['title']}")
            print(f"Date: {article['published_date']}")
        else:
            print("No recent news available")
        
        print()

# Example usage
if __name__ == "__main__":
    print("Stock News Analyzer")
    print("=" * 30)
    
    # Example 1: Analyze news for a specific stock
    print("\n1. Example: Apple (AAPL) News Analysis")
    analyze_stock_news("AAPL", num_articles=5)
    
    # Example 2: Compare news for tech stocks
    print("\n2. Example: Tech Stocks News Comparison")
    tech_stocks = ["AAPL", "GOOGL", "MSFT"]
    compare_news_sentiment(tech_stocks)
    
    # Example 3: Trending stocks summary
    print("\n3. Example: Trending Stocks News Summary")
    get_trending_stocks_news()
    
    print("\n" + "="*60)
    print("To use the interactive news browser, uncomment the line below:")
    print("# interactive_news_browser()")
    print("="*60)
