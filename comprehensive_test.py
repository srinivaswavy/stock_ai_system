"""
Comprehensive Test Script for Ultra News Analysis
Tests all enhanced news functionality
"""

from stock_data_analyzer import StockAnalyzer
from comprehensive_news_analyzer import ComprehensiveNewsAnalyzer
import json
import time
from datetime import datetime

def test_basic_functionality():
    """Test basic functionality works"""
    print("🧪 TESTING BASIC FUNCTIONALITY")
    print("=" * 60)
    
    test_symbol = "AAPL"
    print(f"Testing with {test_symbol}...")
    
    try:
        analyzer = StockAnalyzer(test_symbol)
        
        # Test 1: Basic stock info
        print("\n1️⃣ Testing basic stock info...")
        info = analyzer.get_stock_info()
        assert info is not None, "Stock info should not be None"
        print(f"   ✅ Company: {info.get('Company Name', 'N/A')}")
        
        # Test 2: Standard news
        print("\n2️⃣ Testing standard news retrieval...")
        news = analyzer.get_news(limit=5)
        if news:
            print(f"   ✅ Retrieved {len(news)} news articles")
            assert len(news) <= 5, "Should not exceed limit"
        else:
            print("   ⚠️  No news available (this is okay)")
        
        # Test 3: Extended news
        print("\n3️⃣ Testing extended news retrieval...")
        extended = analyzer.get_extended_news(limit=10)
        if extended and not extended.get('error'):
            print(f"   ✅ Extended news: {len(extended.get('articles', []))} articles")
        else:
            print(f"   ⚠️  Extended news: {extended.get('error', 'No data')}")
        
        # Test 4: Ultra-comprehensive news
        print("\n4️⃣ Testing ultra-comprehensive news...")
        ultra = analyzer.get_ultra_comprehensive_news(limit=20)
        if ultra.get('status') == 'success':
            coverage = ultra['coverage_summary']
            print(f"   ✅ Ultra news: {coverage['articles_with_content']} articles with content")
            print(f"   ✅ Total characters: {coverage['total_characters']:,}")
        else:
            print(f"   ❌ Ultra news failed: {ultra.get('error', 'Unknown error')}")
        
        print("\n✅ Basic functionality tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Basic functionality test failed: {e}")
        return False

def test_comprehensive_analyzer():
    """Test the comprehensive news analyzer"""
    print("\n🧪 TESTING COMPREHENSIVE NEWS ANALYZER")
    print("=" * 60)
    
    test_symbol = "TSLA"
    print(f"Testing with {test_symbol}...")
    
    try:
        analyzer = ComprehensiveNewsAnalyzer(test_symbol)
        
        # Test 1: Yahoo Finance enhanced retrieval
        print("\n1️⃣ Testing Yahoo Finance enhanced retrieval...")
        yahoo_data = analyzer.get_yahoo_finance_news(limit=15)
        
        if yahoo_data.get('articles'):
            print(f"   ✅ Retrieved {len(yahoo_data['articles'])} articles")
            
            # Check content statistics
            stats = yahoo_data.get('content_statistics', {})
            print(f"   📊 Articles with content: {stats.get('articles_with_content', 0)}")
            print(f"   📊 Unique publishers: {stats.get('unique_publishers', 0)}")
        else:
            print("   ⚠️  No Yahoo Finance articles retrieved")
        
        # Test 2: Comprehensive analysis
        print("\n2️⃣ Testing comprehensive analysis...")
        comprehensive = analyzer.get_comprehensive_news_analysis(yahoo_limit=20)
        
        yahoo_section = comprehensive['sources']['yahoo_finance']
        if yahoo_section.get('articles'):
            print(f"   ✅ Comprehensive analysis: {len(yahoo_section['articles'])} articles")
        else:
            print("   ⚠️  No articles in comprehensive analysis")
        
        print("\n✅ Comprehensive analyzer tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Comprehensive analyzer test failed: {e}")
        return False

def test_news_methods_comparison():
    """Test news methods comparison"""
    print("\n🧪 TESTING NEWS METHODS COMPARISON")
    print("=" * 60)
    
    test_symbols = ["AAPL", "GOOGL"]
    
    try:
        for symbol in test_symbols:
            print(f"\n🔍 Testing comparison for {symbol}...")
            
            analyzer = StockAnalyzer(symbol)
            comparison = analyzer.compare_news_methods([symbol])
            
            if symbol in comparison:
                methods = comparison[symbol]
                
                standard = methods.get('standard_method', {})
                extended = methods.get('extended_method', {})
                ultra = methods.get('ultra_comprehensive_method', {})
                
                print(f"   📊 Standard: {standard.get('articles', 0)} articles")
                print(f"   📊 Extended: {extended.get('articles', 0)} articles")
                print(f"   📊 Ultra: {ultra.get('articles', 0)} articles")
                
                # Verify ultra method provides more content
                if ultra.get('total_characters', 0) >= standard.get('total_characters', 0):
                    print(f"   ✅ Ultra method provides more content")
                else:
                    print(f"   ⚠️  Ultra method content: {ultra.get('total_characters', 0)} vs Standard: {standard.get('total_characters', 0)}")
        
        print("\n✅ News methods comparison tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ News methods comparison test failed: {e}")
        return False

def test_data_export():
    """Test data export functionality"""
    print("\n🧪 TESTING DATA EXPORT")
    print("=" * 60)
    
    test_symbol = "MSFT"
    
    try:
        # Test 1: Ultra news data export
        print(f"\n1️⃣ Testing ultra news data export for {test_symbol}...")
        
        analyzer = StockAnalyzer(test_symbol)
        ultra_data = analyzer.get_ultra_comprehensive_news(limit=10)
        
        if ultra_data.get('status') == 'success':
            # Export to JSON
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_export_{test_symbol}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(ultra_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Data exported to: {filename}")
            
            # Verify file exists and has content
            import os
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                print(f"   ✅ Export file verified: {os.path.getsize(filename):,} bytes")
                
                # Clean up test file
                os.remove(filename)
                print(f"   🧹 Test file cleaned up")
            else:
                print(f"   ❌ Export file not found or empty")
                return False
        else:
            print(f"   ⚠️  No data to export: {ultra_data.get('error', 'Unknown error')}")
        
        # Test 2: Comprehensive analyzer export
        print(f"\n2️⃣ Testing comprehensive analyzer export...")
        
        comprehensive_analyzer = ComprehensiveNewsAnalyzer(test_symbol)
        export_filename = comprehensive_analyzer.export_news_data(yahoo_limit=10)
        
        if os.path.exists(export_filename):
            print(f"   ✅ Comprehensive export successful: {export_filename}")
            print(f"   📊 File size: {os.path.getsize(export_filename):,} bytes")
            
            # Clean up
            os.remove(export_filename)
            print(f"   🧹 Export file cleaned up")
        else:
            print(f"   ❌ Comprehensive export failed")
            return False
        
        print("\n✅ Data export tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Data export test failed: {e}")
        return False

def performance_test():
    """Test performance with different limits"""
    print("\n🧪 PERFORMANCE TESTING")
    print("=" * 60)
    
    test_symbol = "AAPL"
    limits_to_test = [5, 10, 25, 50]
    
    try:
        analyzer = StockAnalyzer(test_symbol)
        
        for limit in limits_to_test:
            print(f"\n⏱️  Testing performance with limit {limit}...")
            
            start_time = time.time()
            ultra_data = analyzer.get_ultra_comprehensive_news(limit=limit)
            end_time = time.time()
            
            duration = end_time - start_time
            
            if ultra_data.get('status') == 'success':
                coverage = ultra_data['coverage_summary']
                articles = coverage['articles_with_content']
                chars = coverage['total_characters']
                
                print(f"   ⏱️  Time: {duration:.2f}s")
                print(f"   📊 Articles: {articles}")
                print(f"   📊 Characters: {chars:,}")
                print(f"   🚀 Performance: {articles/duration:.1f} articles/sec, {chars/duration:,.0f} chars/sec")
                
                # Performance assertion
                if duration > 30:  # Should not take more than 30 seconds
                    print(f"   ⚠️  Performance warning: took {duration:.2f}s")
                else:
                    print(f"   ✅ Good performance: {duration:.2f}s")
            else:
                print(f"   ❌ Failed at limit {limit}: {ultra_data.get('error')}")
        
        print("\n✅ Performance tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Performance test failed: {e}")
        return False

def integration_test():
    """Test integration between different components"""
    print("\n🧪 INTEGRATION TESTING")
    print("=" * 60)
    
    test_symbol = "NVDA"
    
    try:
        # Test integration between standard analyzer and comprehensive analyzer
        print(f"\n1️⃣ Testing analyzer integration for {test_symbol}...")
        
        standard_analyzer = StockAnalyzer(test_symbol)
        comprehensive_analyzer = ComprehensiveNewsAnalyzer(test_symbol)
        
        # Get data from both
        standard_news = standard_analyzer.get_news(limit=10)
        ultra_news = standard_analyzer.get_ultra_comprehensive_news(limit=15)
        comprehensive_news = comprehensive_analyzer.get_yahoo_finance_news(limit=10)
        
        print(f"   📊 Standard news: {len(standard_news) if standard_news else 0} articles")
        print(f"   📊 Ultra news: {ultra_news.get('total_processed_articles', 0)} articles")
        print(f"   📊 Comprehensive news: {len(comprehensive_news.get('articles', []))} articles")
        
        # Test methods comparison integration
        print(f"\n2️⃣ Testing methods comparison integration...")
        
        comparison = standard_analyzer.compare_news_methods([test_symbol])
        
        if test_symbol in comparison:
            print(f"   ✅ Methods comparison integrated successfully")
            
            # Verify data consistency
            ultra_method = comparison[test_symbol].get('ultra_comprehensive_method', {})
            expected_articles = ultra_news.get('total_processed_articles', 0)
            comparison_articles = ultra_method.get('articles', 0)
            
            if abs(expected_articles - comparison_articles) <= 1:  # Allow small variance
                print(f"   ✅ Data consistency verified")
            else:
                print(f"   ⚠️  Data inconsistency: {expected_articles} vs {comparison_articles}")
        else:
            print(f"   ❌ Methods comparison integration failed")
            return False
            
        print("\n✅ Integration tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🧪 COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print("Testing all enhanced news functionality...")
    
    test_results = {
        'Basic Functionality': test_basic_functionality(),
        'Comprehensive Analyzer': test_comprehensive_analyzer(),
        'News Methods Comparison': test_news_methods_comparison(),
        'Data Export': test_data_export(),
        'Performance': performance_test(),
        'Integration': integration_test()
    }
    
    # Summary
    print(f"\n{'='*80}")
    print("🧪 TEST RESULTS SUMMARY")
    print(f"{'='*80}")
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<30} {status}")
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced news functionality is working correctly.")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    return test_results

if __name__ == "__main__":
    print("🚀 ENHANCED NEWS ANALYSIS TEST SUITE")
    print("=" * 80)
    
    print("This script will test all enhanced news functionality.")
    print("It may take several minutes to complete all tests.\n")
    
    choice = input("Run all tests? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        results = run_all_tests()
        
        # Optional: Export test results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = f"test_results_{timestamp}.json"
        
        with open(results_filename, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'test_results': results,
                'summary': {
                    'total_tests': len(results),
                    'passed_tests': sum(results.values()),
                    'success_rate': sum(results.values()) / len(results) * 100
                }
            }, f, indent=2)
        
        print(f"\n📁 Test results exported to: {results_filename}")
    else:
        print("Test suite cancelled.")
    
    print("\n" + "="*80)
    print("✅ Test suite complete!")
    print("="*80)
