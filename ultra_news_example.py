"""
Ultra-Comprehensive News Analysis Example
Demonstrates the most advanced news retrieval capabilities
"""

from stock_data_analyzer import StockAnalyzer
from comprehensive_news_analyzer import ComprehensiveNewsAnalyzer
import json
from datetime import datetime

def demonstrate_ultra_news_analysis():
    """
    Demonstrate ultra-comprehensive news analysis capabilities
    """
    print("🚀 ULTRA-COMPREHENSIVE NEWS ANALYSIS DEMONSTRATION")
    print("=" * 80)
    
    # Test symbols with typically high news volume
    test_symbols = ["AAPL", "TSLA", "NVDA", "GOOGL", "MSFT"]
    
    for symbol in test_symbols:
        print(f"\n{'='*100}")
        print(f"🔍 ULTRA-COMPREHENSIVE ANALYSIS FOR {symbol}")
        print(f"{'='*100}")
        
        # Initialize analyzer
        analyzer = StockAnalyzer(symbol)
        
        # Method 1: Ultra-comprehensive news analysis
        print(f"\n🎯 Method 1: Ultra-Comprehensive News Analysis")
        print("-" * 80)
        
        ultra_data = analyzer.print_ultra_comprehensive_news(limit=75)
        
        # Method 2: Compare all news methods
        print(f"\n📊 Method 2: News Methods Comparison")
        print("-" * 80)
        
        comparison = analyzer.compare_news_methods([symbol])
        
        # Method 3: Use the comprehensive news analyzer
        print(f"\n🌐 Method 3: Multi-Source Comprehensive Analysis")
        print("-" * 80)
        
        comprehensive_analyzer = ComprehensiveNewsAnalyzer(symbol)
        multi_source_data = comprehensive_analyzer.print_comprehensive_analysis(yahoo_limit=50)
        
        # Summary for this symbol
        if ultra_data.get('status') == 'success':
            coverage = ultra_data['coverage_summary']
            print(f"\n📈 SUMMARY FOR {symbol}")
            print("-" * 50)
            print(f"✅ Total articles processed: {coverage['articles_with_content']}")
            print(f"✅ Total content: {coverage['total_characters']:,} characters")
            print(f"✅ Unique news sources: {coverage['unique_publishers']}")
            print(f"✅ Substantial articles: {coverage['substantial_articles']}")
            
            # Export detailed data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_ultra_news_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(ultra_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Detailed data exported to: {filename}")
        
        print(f"\n{'='*100}")
        print(f"✅ Ultra-comprehensive analysis complete for {symbol}")
        print(f"{'='*100}")
        
        # Pause between symbols
        input("\nPress Enter to continue to next symbol (or Ctrl+C to exit)...")

def analyze_news_coverage_comparison():
    """
    Compare news coverage across multiple stocks and methods
    """
    print("\n🔬 NEWS COVERAGE COMPARISON ANALYSIS")
    print("=" * 80)
    
    # Compare different stock categories
    stock_categories = {
        "Tech Giants": ["AAPL", "GOOGL", "MSFT"],
        "Growth Stocks": ["TSLA", "NVDA", "AMD"],
        "Traditional": ["JNJ", "PG", "KO"]
    }
    
    all_results = {}
    
    for category, symbols in stock_categories.items():
        print(f"\n📊 Analyzing {category} Stocks")
        print("-" * 60)
        
        category_results = {}
        
        for symbol in symbols:
            print(f"\n🔍 Processing {symbol}...")
            
            analyzer = StockAnalyzer(symbol)
            
            # Get ultra-comprehensive data
            ultra_data = analyzer.get_ultra_comprehensive_news(limit=50)
            
            if ultra_data.get('status') == 'success':
                coverage = ultra_data['coverage_summary']
                quality = ultra_data['quality_metrics']
                
                category_results[symbol] = {
                    'articles_processed': ultra_data['total_processed_articles'],
                    'articles_with_content': coverage['articles_with_content'],
                    'total_characters': coverage['total_characters'],
                    'total_words': coverage['total_words'],
                    'unique_publishers': coverage['unique_publishers'],
                    'coverage_quality': quality['coverage_ratio'],
                    'avg_article_length': quality['avg_content_length'],
                    'substantial_content_ratio': quality['substantial_content_ratio']
                }
                
                print(f"   ✅ {symbol}: {coverage['articles_with_content']} articles, {coverage['total_characters']:,} chars")
            else:
                category_results[symbol] = {'error': ultra_data.get('error', 'Unknown error')}
                print(f"   ❌ {symbol}: Error retrieving data")
        
        all_results[category] = category_results
    
    # Print comparison summary
    print(f"\n📋 COVERAGE COMPARISON SUMMARY")
    print("=" * 80)
    
    for category, results in all_results.items():
        print(f"\n🏷️  {category}:")
        print("-" * 40)
        
        # Calculate category averages
        valid_results = [r for r in results.values() if 'error' not in r]
        
        if valid_results:
            avg_articles = sum(r['articles_with_content'] for r in valid_results) / len(valid_results)
            avg_chars = sum(r['total_characters'] for r in valid_results) / len(valid_results)
            avg_publishers = sum(r['unique_publishers'] for r in valid_results) / len(valid_results)
            avg_quality = sum(r['coverage_quality'] for r in valid_results) / len(valid_results)
            
            print(f"   📊 Average articles per symbol: {avg_articles:.1f}")
            print(f"   📊 Average content per symbol: {avg_chars:,.0f} characters")
            print(f"   📊 Average publishers per symbol: {avg_publishers:.1f}")
            print(f"   📊 Average coverage quality: {avg_quality:.1%}")
            
            # Show best performer in category
            best_symbol = max(valid_results, key=lambda x: results[x]['total_characters'])
            best_symbol_name = [k for k, v in results.items() if v == best_symbol][0]
            print(f"   🏆 Best coverage: {best_symbol_name} ({best_symbol['total_characters']:,} chars)")
    
    # Export comparison results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_filename = f"news_coverage_comparison_{timestamp}.json"
    
    with open(comparison_filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Comparison results exported to: {comparison_filename}")
    
    return all_results

def test_maximum_news_limits():
    """
    Test maximum news retrieval limits
    """
    print("\n🧪 TESTING MAXIMUM NEWS LIMITS")
    print("=" * 80)
    
    test_symbol = "AAPL"  # Use a symbol known to have lots of news
    analyzer = StockAnalyzer(test_symbol)
    
    # Test different limits
    test_limits = [10, 25, 50, 75, 100, 150, 200]
    
    print(f"Testing news retrieval limits for {test_symbol}...")
    
    results = {}
    
    for limit in test_limits:
        print(f"\n🔍 Testing limit: {limit}")
        
        ultra_data = analyzer.get_ultra_comprehensive_news(limit=limit)
        
        if ultra_data.get('status') == 'success':
            processed = ultra_data['total_processed_articles']
            available = ultra_data['total_available_articles']
            chars = ultra_data['coverage_summary']['total_characters']
            
            results[limit] = {
                'articles_processed': processed,
                'total_available': available,
                'total_characters': chars,
                'hit_limit': processed >= limit
            }
            
            print(f"   📊 Processed: {processed}, Available: {available}, Chars: {chars:,}")
            
            if processed < limit:
                print(f"   ✅ Retrieved all available articles (less than limit)")
                break
        else:
            results[limit] = {'error': ultra_data.get('error')}
            print(f"   ❌ Error at limit {limit}")
    
    # Find optimal limit
    successful_results = {k: v for k, v in results.items() if 'error' not in v}
    
    if successful_results:
        max_articles = max(r['articles_processed'] for r in successful_results.values())
        max_chars = max(r['total_characters'] for r in successful_results.values())
        
        optimal_limit = min(k for k, v in successful_results.items() 
                           if v['articles_processed'] == max_articles)
        
        print(f"\n🎯 OPTIMAL CONFIGURATION FOUND")
        print("-" * 50)
        print(f"✅ Optimal limit: {optimal_limit}")
        print(f"✅ Maximum articles retrievable: {max_articles}")
        print(f"✅ Maximum content: {max_chars:,} characters")
        
        # Test the optimal configuration
        print(f"\n🚀 TESTING OPTIMAL CONFIGURATION")
        print("-" * 50)
        
        final_test = analyzer.print_ultra_comprehensive_news(limit=optimal_limit)
        
        return {
            'test_results': results,
            'optimal_limit': optimal_limit,
            'max_articles': max_articles,
            'max_content': max_chars,
            'final_test': final_test
        }
    
    return {'error': 'No successful results', 'test_results': results}

# Main execution
if __name__ == "__main__":
    print("🌟 ULTRA-COMPREHENSIVE NEWS ANALYSIS SUITE")
    print("=" * 80)
    
    print("\nSelect an analysis mode:")
    print("1. Full ultra-comprehensive demonstration")
    print("2. News coverage comparison across stock categories") 
    print("3. Maximum news limits testing")
    print("4. Quick single-stock analysis")
    print("5. Run all analyses")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        demonstrate_ultra_news_analysis()
    
    elif choice == "2":
        analyze_news_coverage_comparison()
    
    elif choice == "3":
        test_maximum_news_limits()
    
    elif choice == "4":
        symbol = input("Enter stock symbol: ").strip().upper()
        if symbol:
            print(f"\n🔍 Quick ultra-comprehensive analysis for {symbol}")
            analyzer = StockAnalyzer(symbol)
            ultra_data = analyzer.print_ultra_comprehensive_news(limit=50)
    
    elif choice == "5":
        print("\n🚀 Running all analyses...")
        
        print("\n" + "="*100)
        print("ANALYSIS 1: Ultra-Comprehensive Demonstration")
        print("="*100)
        demonstrate_ultra_news_analysis()
        
        print("\n" + "="*100)
        print("ANALYSIS 2: Coverage Comparison")
        print("="*100)
        analyze_news_coverage_comparison()
        
        print("\n" + "="*100)
        print("ANALYSIS 3: Maximum Limits Testing")
        print("="*100)
        test_maximum_news_limits()
        
        print("\n🎉 All analyses complete!")
    
    else:
        print("Invalid choice. Please run the script again.")
    
    print(f"\n{'='*80}")
    print("✅ Analysis complete! Check the exported JSON files for detailed data.")
    print(f"{'='*80}")
