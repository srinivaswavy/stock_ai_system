"""
Example of using StockAnalyzer programmatically with returned data
Demonstrates how to use the analyzer functions to get structured data
"""

from stock_data_analyzer import StockAnalyzer
import json

def analyze_stock_programmatically(symbol):
    """
    Example of programmatic stock analysis using returned data
    
    Args:
        symbol (str): Stock ticker symbol
    
    Returns:
        dict: Complete analysis results
    """
    print(f"Analyzing {symbol} programmatically...")
    
    # Create analyzer
    analyzer = StockAnalyzer(symbol)
    
    # Get comprehensive analysis (returns structured data)
    analysis = analyzer.get_comprehensive_analysis(period="3mo", include_news=True, news_limit=5)
    
    # Get price statistics (returns structured data)
    price_stats = analyzer.get_price_statistics(period="1mo")
    
    # Get specific data components (all return data)
    stock_info = analyzer.get_stock_info()
    historical_data = analyzer.get_historical_data(period="1mo")
    news_data = analyzer.get_news(limit=5)
    recommendations = analyzer.get_stock_recommendations()
    
    # Process and use the returned data
    results = {
        'comprehensive_analysis': analysis,
        'price_statistics': price_stats,
        'raw_components': {
            'stock_info': stock_info,
            'news_count': len(news_data) if news_data else 0,
            'historical_data_points': len(historical_data) if historical_data is not None else 0,
            'has_recommendations': recommendations is not None and not recommendations.empty
        }
    }
    
    return results

def extract_key_insights(analysis_results):
    """
    Extract key insights from analysis results
    
    Args:
        analysis_results (dict): Results from analyze_stock_programmatically
    
    Returns:
        dict: Key insights
    """
    comp_analysis = analysis_results['comprehensive_analysis']
    price_stats = analysis_results['price_statistics']
    
    # Extract key metrics
    insights = {
        'symbol': comp_analysis['symbol'],
        'current_price': comp_analysis.get('stock_info', {}).get('Current Price', 'N/A'),
        'company_name': comp_analysis.get('stock_info', {}).get('Company Name', 'N/A'),
        'sector': comp_analysis.get('stock_info', {}).get('Sector', 'N/A'),
        'market_cap': comp_analysis.get('stock_info', {}).get('Market Cap', 'N/A'),
    }
    
    # Price performance
    if price_stats:
        insights.update({
            'monthly_change_pct': price_stats['change_pct'],
            'monthly_high': price_stats['high'],
            'monthly_low': price_stats['low'],
            'volatility': price_stats['volatility']
        })
    
    # Technical analysis
    tech_analysis = comp_analysis.get('technical_analysis', {})
    if tech_analysis:
        insights['trend_signal'] = tech_analysis.get('trend_signal', 'UNKNOWN')
        insights['above_ma_20'] = tech_analysis.get('price_above_ma_20', None)
        insights['above_ma_50'] = tech_analysis.get('price_above_ma_50', None)
    
    # Analyst sentiment
    analyst_data = comp_analysis.get('analyst_recommendations', {})
    if analyst_data:
        insights['analyst_buy_ratio'] = analyst_data.get('buy_ratio', 0)
        insights['total_analysts'] = analyst_data.get('total_analysts', 0)
    
    # News sentiment (basic count)
    news_data = comp_analysis.get('news', [])
    insights['recent_news_count'] = len(news_data)
    insights['top_news_headline'] = news_data[0]['title'] if news_data else 'No recent news'
    
    return insights

def compare_stocks_programmatically(symbols):
    """
    Compare multiple stocks using returned data
    
    Args:
        symbols (list): List of stock symbols
    
    Returns:
        dict: Comparison results
    """
    print(f"Comparing stocks: {', '.join(symbols)}")
    
    comparison_results = {}
    
    for symbol in symbols:
        try:
            analyzer = StockAnalyzer(symbol)
            
            # Get key data for comparison
            stock_info = analyzer.get_stock_info()
            price_stats = analyzer.get_price_statistics(period="1mo")
            analysis = analyzer.get_comprehensive_analysis(period="1mo", include_news=False)
            
            comparison_results[symbol] = {
                'current_price': stock_info.get('Current Price', 0) if stock_info else 0,
                'market_cap': stock_info.get('Market Cap', 0) if stock_info else 0,
                'pe_ratio': stock_info.get('PE Ratio', 0) if stock_info else 0,
                'monthly_change_pct': price_stats['change_pct'] if price_stats else 0,
                'volatility': price_stats['volatility'] if price_stats else 0,
                'trend_signal': analysis.get('technical_analysis', {}).get('trend_signal', 'UNKNOWN')
            }
            
        except Exception as e:
            comparison_results[symbol] = {'error': str(e)}
    
    return comparison_results

def main():
    """Main function demonstrating programmatic usage"""
    print("StockAnalyzer Programmatic Usage Examples")
    print("=" * 50)
    
    # Example 1: Single stock analysis
    print("\n1. Single Stock Analysis (Programmatic)")
    print("-" * 40)
    
    symbol = "AAPL"
    results = analyze_stock_programmatically(symbol)
    
    # Extract insights
    insights = extract_key_insights(results)
    
    print(f"Key Insights for {insights['symbol']}:")
    print(f"  Company: {insights['company_name']}")
    print(f"  Current Price: ${insights['current_price']}")
    print(f"  Monthly Change: {insights['monthly_change_pct']:.2f}%")
    print(f"  Trend Signal: {insights['trend_signal']}")
    print(f"  Recent News: {insights['recent_news_count']} articles")
    print(f"  Top Headline: {insights['top_news_headline'][:60]}...")
    
    # Example 2: Multi-stock comparison
    print("\n2. Multi-Stock Comparison (Programmatic)")
    print("-" * 40)
    
    stocks_to_compare = ["AAPL", "GOOGL", "MSFT"]
    comparison = compare_stocks_programmatically(stocks_to_compare)
    
    print("Stock Comparison Results:")
    for symbol, data in comparison.items():
        if 'error' not in data:
            print(f"  {symbol}: ${data['current_price']:.2f}, "
                  f"Change: {data['monthly_change_pct']:.2f}%, "
                  f"Trend: {data['trend_signal']}")
        else:
            print(f"  {symbol}: Error - {data['error']}")
    
    # Example 3: Using specific data components
    print("\n3. Working with Specific Data Components")
    print("-" * 40)
    
    analyzer = StockAnalyzer("TSLA")
    
    # Get news data only
    news = analyzer.get_news(limit=3)
    if news:
        print(f"Latest TSLA news ({len(news)} articles):")
        for i, article in enumerate(news, 1):
            print(f"  {i}. {article['title'][:50]}...")
    
    # Get price statistics only
    price_stats = analyzer.get_price_statistics(period="1mo")
    if price_stats:
        print(f"\nTSLA Price Stats:")
        print(f"  Current: ${price_stats['current_price']:.2f}")
        print(f"  Monthly Change: {price_stats['change_pct']:.2f}%")
        print(f"  Volatility: {price_stats['volatility']:.2f}%")
    
    # Example 4: Saving results to JSON
    print("\n4. Saving Analysis Results")
    print("-" * 40)
    
    # Save comprehensive analysis to JSON file
    filename = f"{symbol}_analysis.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"Analysis results saved to {filename}")
    print(f"File size: {len(json.dumps(results, default=str))} characters")
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")
    print("Functions now return structured data that can be used programmatically.")

if __name__ == "__main__":
    main()
