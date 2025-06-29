"""
Simple Yahoo Finance Stock Data Example
A quick example showing how to fetch and display stock data
"""

from stock_data_analyzer import StockAnalyzer

def main():
    # Get user input for stock symbol
    print("Yahoo Finance Stock Data Fetcher")
    print("=" * 35)
    
    symbol = input("Enter a stock symbol (e.g., AAPL, GOOGL, MSFT): ").strip().upper()
    
    if not symbol:
        symbol = "AAPL"  # Default to Apple
        print(f"Using default symbol: {symbol}")
    
    # Create analyzer instance
    analyzer = StockAnalyzer(symbol)
    
    # Display stock information
    analyzer.print_summary(include_news=True)
    
    # Get recent price data
    print(f"\nFetching recent price data for {symbol}...")
    recent_data = analyzer.get_historical_data(period="1mo")
    
    if recent_data is not None and not recent_data.empty:
        print(f"\nLast 5 trading days for {symbol}:")
        print("-" * 60)
        last_5_days = recent_data.tail(5)
        for date, row in last_5_days.iterrows():
            print(f"{date.strftime('%Y-%m-%d')}: "
                  f"Open: ${row['Open']:.2f}, "
                  f"High: ${row['High']:.2f}, "
                  f"Low: ${row['Low']:.2f}, "
                  f"Close: ${row['Close']:.2f}, "
                  f"Volume: {row['Volume']:,}")
        
        # Calculate some basic statistics
        current_price = recent_data['Close'].iloc[-1]
        month_high = recent_data['High'].max()
        month_low = recent_data['Low'].min()
        avg_volume = recent_data['Volume'].mean()
        
        print(f"\n{symbol} - 1 Month Statistics:")
        print("-" * 30)
        print(f"Current Price: ${current_price:.2f}")
        print(f"Month High: ${month_high:.2f}")
        print(f"Month Low: ${month_low:.2f}")
        print(f"Average Daily Volume: {avg_volume:,.0f}")
        
        # Calculate price change
        month_start_price = recent_data['Close'].iloc[0]
        price_change = current_price - month_start_price
        price_change_pct = (price_change / month_start_price) * 100
        
        print(f"Month Change: ${price_change:.2f} ({price_change_pct:+.2f}%)")
        
        # Show trend
        if price_change_pct > 0:
            print("📈 Stock is UP for the month")
        else:
            print("📉 Stock is DOWN for the month")
        
        # Show more detailed news
        print(f"\n{'='*60}")
        print("ADDITIONAL NEWS HEADLINES")
        print(f"{'='*60}")
        analyzer.print_news(limit=15)  # Increased from 5 to 15 articles
        
        # Show charts
        print(f"\n{'='*60}")
        print("STOCK CHARTS")
        print(f"{'='*60}")
        
        # Ask user if they want to see charts
        show_charts = input(f"\nWould you like to see price charts for {symbol}? (y/n): ").strip().lower()
        
        if show_charts in ['y', 'yes']:
            print(f"\nGenerating charts for {symbol}...")
            
            # Show basic price chart
            print("1. Displaying 6-month price chart...")
            analyzer.plot_price_chart(period="6mo", save_chart=True)
            
            # Show moving averages chart
            print("2. Displaying price chart with moving averages...")
            analyzer.plot_with_moving_averages(period="6mo", windows=[20, 50], save_chart=True)
            
            print(f"Charts have been displayed and saved as PNG files in the current directory.")
        else:
            print("Charts skipped. You can run the analyzer again to view charts.")
    
    else:
        print(f"Could not fetch data for {symbol}. Please check the symbol and try again.")
    
    print("\n" + "=" * 50)
    print("Analysis complete!")

if __name__ == "__main__":
    main()
