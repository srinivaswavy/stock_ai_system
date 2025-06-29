"""
Enhanced Stock Analysis with Charts and Full News
Shows comprehensive analysis including charts and detailed news summaries
"""

from stock_data_analyzer import StockAnalyzer
import matplotlib.pyplot as plt

def enhanced_stock_analysis(symbol):
    """
    Perform enhanced stock analysis with charts and detailed news
    
    Args:
        symbol (str): Stock ticker symbol
    """
    print(f"📊 ENHANCED STOCK ANALYSIS FOR {symbol.upper()}")
    print("=" * 60)
    
    # Create analyzer instance
    analyzer = StockAnalyzer(symbol)
    
    # Display comprehensive stock information
    print("📋 STOCK INFORMATION & NEWS")
    print("-" * 40)
    analyzer.print_summary(include_news=True)
    
    # Get and display detailed price analysis
    print(f"\n📈 PRICE ANALYSIS")
    print("-" * 40)
    recent_data = analyzer.get_historical_data(period="3mo")
    
    if recent_data is not None and not recent_data.empty:
        # Current price info
        current_price = recent_data['Close'].iloc[-1]
        prev_close = recent_data['Close'].iloc[-2]
        daily_change = current_price - prev_close
        daily_change_pct = (daily_change / prev_close) * 100
        
        # 3-month statistics
        high_3m = recent_data['High'].max()
        low_3m = recent_data['Low'].min()
        avg_volume = recent_data['Volume'].mean()
        
        # Price changes
        start_price = recent_data['Close'].iloc[0]
        total_change = current_price - start_price
        total_change_pct = (total_change / start_price) * 100
        
        print(f"Current Price: ${current_price:.2f}")
        print(f"Daily Change: ${daily_change:.2f} ({daily_change_pct:+.2f}%)")
        print(f"3-Month High: ${high_3m:.2f}")
        print(f"3-Month Low: ${low_3m:.2f}")
        print(f"3-Month Change: ${total_change:.2f} ({total_change_pct:+.2f}%)")
        print(f"Average Volume: {avg_volume:,.0f}")
        
        # Trend analysis
        if total_change_pct > 10:
            trend = "🚀 STRONG UPTREND"
        elif total_change_pct > 0:
            trend = "📈 UPTREND"
        elif total_change_pct > -10:
            trend = "📉 DOWNTREND"
        else:
            trend = "⬇️ STRONG DOWNTREND"
        print(f"3-Month Trend: {trend}")
        
        # Generate and display charts
        print(f"\n📊 GENERATING CHARTS")
        print("-" * 40)
        
        # Chart 1: 6-month price chart
        print("1. 6-Month Price Chart")
        analyzer.plot_price_chart(period="6mo", save_chart=True)
        
        # Chart 2: Price with moving averages
        print("2. Price Chart with Moving Averages")
        analyzer.plot_with_moving_averages(period="6mo", windows=[20, 50, 200], save_chart=True)
        
        # Chart 3: Volume analysis
        print("3. Volume Analysis")
        plot_volume_analysis(analyzer, period="3mo")
        
        print("✅ All charts generated and saved as PNG files")
        
        # Additional analysis
        print(f"\n🔍 ADDITIONAL ANALYSIS")
        print("-" * 40)
        
        # Moving averages analysis
        ma_data = analyzer.calculate_moving_averages(period="6mo", windows=[20, 50, 200])
        if ma_data is not None:
            latest_price = ma_data['Close'].iloc[-1]
            ma_20 = ma_data['MA_20'].iloc[-1]
            ma_50 = ma_data['MA_50'].iloc[-1]
            ma_200 = ma_data['MA_200'].iloc[-1]
            
            print(f"Technical Indicators:")
            print(f"  20-day MA: ${ma_20:.2f} {'✅' if latest_price > ma_20 else '❌'}")
            print(f"  50-day MA: ${ma_50:.2f} {'✅' if latest_price > ma_50 else '❌'}")
            print(f"  200-day MA: ${ma_200:.2f} {'✅' if latest_price > ma_200 else '❌'}")
            
            # Simple trend analysis
            if latest_price > ma_20 > ma_50 > ma_200:
                print("  Signal: 🟢 BULLISH (Price above all MAs)")
            elif latest_price < ma_20 < ma_50 < ma_200:
                print("  Signal: 🔴 BEARISH (Price below all MAs)")
            else:
                print("  Signal: 🟡 MIXED (Conflicting signals)")
        
        # Analyst recommendations
        recommendations = analyzer.get_stock_recommendations()
        if recommendations is not None and not recommendations.empty:
            print(f"\n📊 ANALYST RECOMMENDATIONS")
            print("-" * 40)
            latest_rec = recommendations.iloc[0]
            total_analysts = sum([latest_rec.get('strongBuy', 0), latest_rec.get('buy', 0), 
                                latest_rec.get('hold', 0), latest_rec.get('sell', 0), 
                                latest_rec.get('strongSell', 0)])
            
            if total_analysts > 0:
                buy_ratio = (latest_rec.get('strongBuy', 0) + latest_rec.get('buy', 0)) / total_analysts * 100
                print(f"Total Analysts: {total_analysts}")
                print(f"Buy/Strong Buy: {buy_ratio:.1f}%")
                print(f"Strong Buy: {latest_rec.get('strongBuy', 0)}")
                print(f"Buy: {latest_rec.get('buy', 0)}")
                print(f"Hold: {latest_rec.get('hold', 0)}")
                print(f"Sell: {latest_rec.get('sell', 0)}")
                print(f"Strong Sell: {latest_rec.get('strongSell', 0)}")
        
        # Extended news section
        print(f"\n📰 DETAILED NEWS ANALYSIS")
        print("-" * 40)
        analyzer.print_news(limit=20)  # Increased to 20 for comprehensive news coverage
        
    else:
        print(f"❌ Could not fetch data for {symbol}")

def plot_volume_analysis(analyzer, period="3mo"):
    """
    Plot volume analysis chart
    
    Args:
        analyzer: StockAnalyzer instance
        period: Time period for analysis
    """
    data = analyzer.get_historical_data(period=period)
    
    if data is None or data.empty:
        print("No data available for volume analysis")
        return
    
    # Create volume chart
    plt.figure(figsize=(12, 8))
    
    # Top subplot - Price
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Close'], label=f'{analyzer.symbol} Close Price', linewidth=2, color='blue')
    plt.title(f'{analyzer.symbol} Price and Volume Analysis - {period.upper()}')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Bottom subplot - Volume
    plt.subplot(2, 1, 2)
    colors = ['green' if close >= open_ else 'red' for close, open_ in zip(data['Close'], data['Open'])]
    plt.bar(data.index, data['Volume'], color=colors, alpha=0.7, label='Volume')
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.xticks(rotation=45)
    
    # Save chart
    filename = f"{analyzer.symbol}_volume_analysis_{period}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function for enhanced stock analysis"""
    print("🚀 ENHANCED STOCK ANALYZER WITH CHARTS & FULL NEWS")
    print("=" * 55)
    
    # Get user input
    symbol = input("Enter a stock symbol (e.g., AAPL, GOOGL, MSFT): ").strip().upper()
    
    if not symbol:
        symbol = "AAPL"  # Default to Apple
        print(f"Using default symbol: {symbol}")
    
    # Perform enhanced analysis
    enhanced_stock_analysis(symbol)
    
    print(f"\n🎉 ANALYSIS COMPLETE FOR {symbol}")
    print("=" * 50)
    print("📊 Charts saved as PNG files in current directory")
    print("📰 Full news summaries displayed above")
    print("📈 Technical analysis and recommendations included")

if __name__ == "__main__":
    main()
