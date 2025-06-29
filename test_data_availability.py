"""
Test Yahoo Finance Data Availability
Simple script to test what data is available from Yahoo Finance
"""

import yfinance as yf

def test_stock_data(symbol="AAPL"):
    """Test what data is available for a stock"""
    print(f"Testing data availability for {symbol}")
    print("=" * 50)
    
    stock = yf.Ticker(symbol)
    
    # Test basic info
    print("\n1. Testing basic info...")
    try:
        info = stock.info
        print(f"✓ Basic info available: {len(info)} fields")
        print(f"Company: {info.get('longName', 'N/A')}")
        print(f"Current Price: {info.get('currentPrice', 'N/A')}")
    except Exception as e:
        print(f"✗ Error getting basic info: {e}")
    
    # Test news
    print("\n2. Testing news...")
    try:
        news = stock.news
        print(f"✓ News available: {len(news)} articles")
        if news:
            print(f"First article title: {news[0].get('title', 'N/A')}")
            print(f"Available news fields: {list(news[0].keys())}")
    except Exception as e:
        print(f"✗ Error getting news: {e}")
    
    # Test recommendations
    print("\n3. Testing recommendations...")
    try:
        recommendations = stock.recommendations
        if recommendations is not None:
            print(f"✓ Recommendations available: {recommendations.shape}")
            print(recommendations.head(2))
        else:
            print("✗ No recommendations available")
    except Exception as e:
        print(f"✗ Error getting recommendations: {e}")
    
    # Test calendar
    print("\n4. Testing calendar...")
    try:
        calendar = stock.calendar
        if calendar is not None:
            print(f"✓ Calendar available: {type(calendar)}")
            if isinstance(calendar, dict):
                print(f"Calendar keys: {list(calendar.keys())}")
            else:
                print(f"Calendar shape: {calendar.shape if hasattr(calendar, 'shape') else 'N/A'}")
        else:
            print("✗ No calendar available")
    except Exception as e:
        print(f"✗ Error getting calendar: {e}")
    
    # Test historical data
    print("\n5. Testing historical data...")
    try:
        hist = stock.history(period="5d")
        print(f"✓ Historical data available: {hist.shape}")
        print(f"Latest close: ${hist['Close'].iloc[-1]:.2f}")
    except Exception as e:
        print(f"✗ Error getting historical data: {e}")

if __name__ == "__main__":
    # Test multiple stocks
    symbols = ["AAPL", "GOOGL", "TSLA"]
    
    for symbol in symbols:
        test_stock_data(symbol)
        print("\n" + "="*70 + "\n")
