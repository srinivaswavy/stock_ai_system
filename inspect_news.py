"""
Test Yahoo Finance News Structure
Detailed inspection of the news data structure
"""

import yfinance as yf
import json

def inspect_news_structure(symbol="AAPL"):
    """Inspect the detailed structure of news data"""
    print(f"Detailed news inspection for {symbol}")
    print("=" * 50)
    
    stock = yf.Ticker(symbol)
    
    try:
        news = stock.news
        print(f"Number of news articles: {len(news)}")
        
        if news:
            print(f"\nFirst article structure:")
            first_article = news[0]
            print(f"Keys: {list(first_article.keys())}")
            
            for key, value in first_article.items():
                print(f"\n{key}:")
                if isinstance(value, dict):
                    print(f"  Type: dict with keys: {list(value.keys())}")
                    # Print first few items if it's a dict
                    for k, v in list(value.items())[:3]:
                        print(f"    {k}: {str(v)[:100]}...")
                elif isinstance(value, list):
                    print(f"  Type: list with {len(value)} items")
                    if value:
                        print(f"    First item: {str(value[0])[:100]}...")
                else:
                    print(f"  Type: {type(value).__name__}")
                    print(f"  Value: {str(value)[:200]}...")
        
        # Try alternative methods to get news
        print(f"\n{'='*50}")
        print("Trying alternative news methods...")
        
        # Method 1: Check if there's a get_news method
        if hasattr(stock, 'get_news'):
            try:
                alt_news = stock.get_news()
                print(f"get_news() returned: {type(alt_news)} with {len(alt_news) if alt_news else 0} items")
            except Exception as e:
                print(f"get_news() failed: {e}")
        
        # Method 2: Check news in info
        try:
            info = stock.info
            if 'news' in info:
                info_news = info['news']
                print(f"info['news'] returned: {type(info_news)} with {len(info_news) if info_news else 0} items")
            else:
                print("No 'news' key in stock.info")
        except Exception as e:
            print(f"Checking info['news'] failed: {e}")
            
    except Exception as e:
        print(f"Error inspecting news: {e}")

if __name__ == "__main__":
    inspect_news_structure("AAPL")
