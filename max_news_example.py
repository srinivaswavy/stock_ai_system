"""
Maximum News Coverage Example
Demonstrates how to get the largest possible amount of news content
"""

from stock_data_analyzer import StockAnalyzer

def demonstrate_maximum_news(symbol):
    """
    Demonstrate maximum news coverage capabilities
    
    Args:
        symbol (str): Stock ticker symbol
    """
    print(f"🗞️ MAXIMUM NEWS COVERAGE DEMONSTRATION FOR {symbol}")
    print("=" * 80)
    
    analyzer = StockAnalyzer(symbol)
    
    # Method 1: Extended news coverage
    print("\n1. 📰 EXTENDED NEWS COVERAGE (Up to 25 articles)")
    print("-" * 60)
    extended_data = analyzer.print_extended_news(limit=25)
    
    # Method 2: Get even more news programmatically
    print(f"\n2. 📊 MAXIMUM NEWS DATA ANALYSIS")
    print("-" * 60)
    max_news = analyzer.get_extended_news(limit=50)
    
    if max_news and not max_news.get('error'):
        print(f"✅ Total news articles available: {max_news['total_available']}")
        print(f"✅ Articles with substantial content: {max_news['content_stats']['articles_with_content']}")
        print(f"✅ Longest article: {max_news['content_stats']['longest_article']} characters")
        print(f"✅ Unique publishers: {len(max_news['content_stats']['publishers'])}")
        
        # Show top 5 longest articles
        articles_with_content = [a for a in max_news['articles'] if a.get('content_length', 0) > 0]
        articles_with_content.sort(key=lambda x: x.get('content_length', 0), reverse=True)
        
        print(f"\n📈 TOP 5 LONGEST NEWS ARTICLES:")
        for i, article in enumerate(articles_with_content[:5], 1):
            print(f"   {i}. {article['title'][:60]}...")
            print(f"      📝 {article['content_length']} characters")
            print(f"      🏢 {article['publisher']}")
            print(f"      📅 {article['published_date']}")
            print()
    
    # Method 3: Regular news for comparison
    print(f"\n3. 📋 REGULAR NEWS (Standard method)")
    print("-" * 60)
    regular_news = analyzer.get_news(limit=20)
    if regular_news:
        print(f"✅ Regular news method returned: {len(regular_news)} articles")
        total_chars = sum(len(article.get('summary', '')) for article in regular_news)
        print(f"✅ Total content: {total_chars} characters")
        
        # Show sample of longest regular news
        longest_regular = max(regular_news, key=lambda x: len(x.get('summary', '')))
        print(f"✅ Longest regular article: {len(longest_regular.get('summary', ''))} characters")
        print(f"   Title: {longest_regular.get('title', 'No title')[:60]}...")

def compare_news_methods(symbol):
    """
    Compare different news retrieval methods
    
    Args:
        symbol (str): Stock ticker symbol
    """
    print(f"\n🔍 NEWS METHOD COMPARISON FOR {symbol}")
    print("=" * 60)
    
    analyzer = StockAnalyzer(symbol)
    
    # Method comparison
    methods = [
        ("Standard get_news(10)", lambda: analyzer.get_news(10)),
        ("Increased get_news(20)", lambda: analyzer.get_news(20)),
        ("Maximum get_news(50)", lambda: analyzer.get_news(50)),
        ("Extended get_extended_news(25)", lambda: analyzer.get_extended_news(25)),
        ("Maximum extended(50)", lambda: analyzer.get_extended_news(50)),
    ]
    
    results = []
    
    for method_name, method_func in methods:
        try:
            data = method_func()
            
            if method_name.startswith("Extended") or method_name.startswith("Maximum extended"):
                # Extended news format
                article_count = data.get('total_processed', 0) if data else 0
                content_chars = sum(a.get('content_length', 0) for a in data.get('articles', []))
                has_content = data.get('content_stats', {}).get('articles_with_content', 0) if data else 0
            else:
                # Regular news format
                article_count = len(data) if data else 0
                content_chars = sum(len(a.get('summary', '')) for a in data) if data else 0
                has_content = len([a for a in data if a.get('summary', '')]) if data else 0
            
            results.append({
                'method': method_name,
                'articles': article_count,
                'total_chars': content_chars,
                'with_content': has_content,
                'avg_chars': content_chars / article_count if article_count > 0 else 0
            })
            
        except Exception as e:
            results.append({
                'method': method_name,
                'error': str(e)
            })
    
    # Display comparison
    print(f"\n📊 METHOD COMPARISON RESULTS:")
    print("-" * 60)
    print(f"{'Method':<25} {'Articles':<10} {'With Content':<12} {'Total Chars':<12} {'Avg/Article':<12}")
    print("-" * 75)
    
    for result in results:
        if 'error' in result:
            print(f"{result['method']:<25} {'ERROR':<10} {result['error'][:30]}")
        else:
            print(f"{result['method']:<25} {result['articles']:<10} {result['with_content']:<12} {result['total_chars']:<12} {result['avg_chars']:.0f}")
    
    # Find best method
    valid_results = [r for r in results if 'error' not in r]
    if valid_results:
        best_method = max(valid_results, key=lambda x: x['total_chars'])
        print(f"\n🏆 BEST METHOD: {best_method['method']}")
        print(f"   📰 Articles: {best_method['articles']}")
        print(f"   📝 Total Content: {best_method['total_chars']} characters")
        print(f"   📊 Average per Article: {best_method['avg_chars']:.0f} characters")

def main():
    """Main function for maximum news demonstration"""
    print("🗞️ MAXIMUM NEWS COVERAGE DEMONSTRATION")
    print("=" * 50)
    
    # Get user input
    symbol = input("Enter a stock symbol for maximum news coverage (e.g., AAPL, TSLA, GOOGL): ").strip().upper()
    
    if not symbol:
        symbol = "TSLA"  # Default to Tesla (usually has lots of news)
        print(f"Using default symbol: {symbol}")
    
    # Demonstrate maximum news coverage
    demonstrate_maximum_news(symbol)
    
    # Compare different methods
    compare_news_methods(symbol)
    
    print(f"\n🎉 MAXIMUM NEWS DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("Your analyzer now supports:")
    print("✅ Extended news coverage (up to 50+ articles)")
    print("✅ Comprehensive content extraction")
    print("✅ Multiple news retrieval methods")
    print("✅ Full content without truncation")
    print("✅ Detailed news statistics and metadata")

if __name__ == "__main__":
    main()
