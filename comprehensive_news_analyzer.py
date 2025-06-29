"""
Comprehensive News Analyzer for Stocks
Advanced news retrieval with multiple sources and enhanced coverage
"""

import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re
from urllib.parse import urljoin, urlparse
import time

class ComprehensiveNewsAnalyzer:
    """
    Advanced news analyzer that combines multiple sources for maximum coverage
    """
    
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.stock = yf.Ticker(self.symbol)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_yahoo_finance_news(self, limit=50):
        """
        Enhanced Yahoo Finance news retrieval with maximum data extraction
        
        Args:
            limit (int): Maximum articles to retrieve
            
        Returns:
            dict: Comprehensive news data
        """
        try:
            # Get raw news data
            news_data = self.stock.news
            
            if not news_data:
                return {'source': 'yahoo_finance', 'articles': [], 'total': 0}
            
            articles = []
            for i, article in enumerate(news_data[:limit]):
                try:
                    # Extract all possible data fields
                    raw_content = article.get('content', {})
                    
                    # Main content fields
                    title = raw_content.get('title', f'Article {i+1}')
                    
                    # Try multiple summary fields in order of preference
                    summary_fields = ['summary', 'description', 'intro', 'excerpt', 'body']
                    full_text = ''
                    content_sources = []
                    
                    for field in summary_fields:
                        field_content = raw_content.get(field, '')
                        if field_content and field_content not in full_text:
                            full_text += f" {field_content}"
                            content_sources.append(field)
                    
                    full_text = full_text.strip()
                    
                    # Publisher information
                    provider = raw_content.get('provider', {})
                    if isinstance(provider, dict):
                        publisher = provider.get('displayName', 'Unknown')
                        publisher_url = provider.get('url', '')
                    else:
                        publisher = str(provider)
                        publisher_url = ''
                    
                    # Links and URLs
                    link = raw_content.get('canonicalUrl', raw_content.get('clickThroughUrl', ''))
                    if isinstance(link, dict):
                        link = link.get('url', str(link))
                    
                    # Timestamp handling
                    pub_date = raw_content.get('pubDate', 0)
                    if isinstance(pub_date, str):
                        published_date = pub_date
                    else:
                        published_date = self._format_timestamp(pub_date)
                    
                    # Additional metadata
                    thumbnail = raw_content.get('thumbnail', {})
                    category = raw_content.get('category', '')
                    tags = raw_content.get('tags', [])
                    
                    # Content analysis
                    word_count = len(full_text.split()) if full_text else 0
                    char_count = len(full_text)
                    
                    processed_article = {
                        'id': i + 1,
                        'title': title,
                        'full_content': full_text,
                        'content_sources': content_sources,
                        'word_count': word_count,
                        'char_count': char_count,
                        'publisher': publisher,
                        'publisher_url': publisher_url,
                        'published_date': published_date,
                        'link': link,
                        'category': category,
                        'tags': tags,
                        'has_thumbnail': bool(thumbnail),
                        'thumbnail_url': thumbnail.get('url', '') if isinstance(thumbnail, dict) else '',
                        'content_type': raw_content.get('contentType', 'STORY'),
                        'all_fields': list(raw_content.keys()),
                        'source': 'yahoo_finance'
                    }
                    
                    articles.append(processed_article)
                    
                except Exception as e:
                    articles.append({
                        'id': i + 1,
                        'error': str(e),
                        'raw_data_preview': str(article)[:200] + '...',
                        'source': 'yahoo_finance'
                    })
            
            return {
                'source': 'yahoo_finance',
                'symbol': self.symbol,
                'timestamp': datetime.now().isoformat(),
                'total_available': len(news_data),
                'total_processed': len(articles),
                'articles': articles,
                'content_statistics': self._calculate_content_stats(articles)
            }
            
        except Exception as e:
            return {
                'source': 'yahoo_finance',
                'symbol': self.symbol,
                'error': str(e),
                'articles': []
            }
    
    def get_google_news_search(self, limit=20):
        """
        Search Google News for stock-related articles
        Note: This is a simplified implementation for demonstration
        
        Args:
            limit (int): Maximum articles to retrieve
            
        Returns:
            dict: Google News search results
        """
        try:
            # Get company name for better search
            info = self.stock.info
            company_name = info.get('longName', info.get('shortName', self.symbol))
            
            # Construct search terms
            search_terms = [
                f"{self.symbol} stock news",
                f"{company_name} earnings",
                f"{company_name} financial news",
                f"{self.symbol} price target",
                f"{company_name} analyst"
            ]
            
            all_results = []
            
            for term in search_terms[:2]:  # Limit to avoid rate limiting
                try:
                    # This is a placeholder - in practice, you'd use Google News API or RSS
                    print(f"Searching Google News for: {term}")
                    
                    # Simulated result structure
                    simulated_results = {
                        'search_term': term,
                        'articles_found': f"Would search for '{term}' in Google News",
                        'note': 'This is a placeholder - implement with Google News API or RSS feeds'
                    }
                    
                    all_results.append(simulated_results)
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    all_results.append({
                        'search_term': term,
                        'error': str(e)
                    })
            
            return {
                'source': 'google_news',
                'symbol': self.symbol,
                'search_results': all_results,
                'note': 'Google News integration requires API setup'
            }
            
        except Exception as e:
            return {
                'source': 'google_news',
                'error': str(e)
            }
    
    def get_reddit_discussions(self, limit=10):
        """
        Get Reddit discussions about the stock
        Note: Requires Reddit API setup for full implementation
        
        Args:
            limit (int): Maximum discussions to retrieve
            
        Returns:
            dict: Reddit discussion data
        """
        try:
            # Popular finance subreddits
            subreddits = ['stocks', 'investing', 'SecurityAnalysis', 'financialindependence']
            
            results = {
                'source': 'reddit',
                'symbol': self.symbol,
                'subreddits_searched': subreddits,
                'note': 'Reddit integration requires PRAW (Python Reddit API Wrapper) setup',
                'discussions': []
            }
            
            # Placeholder for Reddit API integration
            for subreddit in subreddits:
                results['discussions'].append({
                    'subreddit': subreddit,
                    'search_query': f"{self.symbol} OR {self.symbol.lower()}",
                    'status': 'Would search Reddit API here'
                })
            
            return results
            
        except Exception as e:
            return {
                'source': 'reddit',
                'error': str(e)
            }
    
    def get_comprehensive_news_analysis(self, yahoo_limit=50, google_limit=20, reddit_limit=10):
        """
        Get comprehensive news analysis from all sources
        
        Args:
            yahoo_limit (int): Yahoo Finance news limit
            google_limit (int): Google News limit
            reddit_limit (int): Reddit discussions limit
            
        Returns:
            dict: Complete news analysis
        """
        print(f"🔍 Gathering comprehensive news for {self.symbol}...")
        
        # Collect from all sources
        yahoo_news = self.get_yahoo_finance_news(yahoo_limit)
        google_news = self.get_google_news_search(google_limit)
        reddit_data = self.get_reddit_discussions(reddit_limit)
        
        # Combine and analyze
        all_sources = [yahoo_news, google_news, reddit_data]
        
        comprehensive_analysis = {
            'symbol': self.symbol,
            'analysis_timestamp': datetime.now().isoformat(),
            'sources': {
                'yahoo_finance': yahoo_news,
                'google_news': google_news,
                'reddit': reddit_data
            },
            'summary': {
                'total_yahoo_articles': len(yahoo_news.get('articles', [])),
                'total_sources_attempted': len(all_sources),
                'data_quality_score': self._calculate_data_quality(yahoo_news),
                'content_diversity': self._analyze_content_diversity(yahoo_news)
            }
        }
        
        return comprehensive_analysis
    
    def print_comprehensive_analysis(self, yahoo_limit=50):
        """
        Print comprehensive news analysis in a formatted way
        
        Args:
            yahoo_limit (int): Yahoo Finance news limit
        """
        print(f"\n{'='*80}")
        print(f"🔍 COMPREHENSIVE NEWS ANALYSIS FOR {self.symbol}")
        print(f"{'='*80}")
        
        analysis = self.get_comprehensive_news_analysis(yahoo_limit=yahoo_limit)
        
        # Yahoo Finance Analysis
        yahoo_data = analysis['sources']['yahoo_finance']
        if yahoo_data.get('articles'):
            print(f"\n📰 YAHOO FINANCE NEWS ({len(yahoo_data['articles'])} articles)")
            print("-" * 60)
            
            stats = yahoo_data.get('content_statistics', {})
            print(f"✅ Articles with content: {stats.get('articles_with_content', 0)}")
            print(f"✅ Average content length: {stats.get('avg_content_length', 0):.0f} characters")
            print(f"✅ Longest article: {stats.get('max_content_length', 0)} characters")
            print(f"✅ Unique publishers: {stats.get('unique_publishers', 0)}")
            
            # Show top articles
            articles = yahoo_data['articles']
            content_articles = [a for a in articles if a.get('char_count', 0) > 0]
            content_articles.sort(key=lambda x: x.get('char_count', 0), reverse=True)
            
            print(f"\n🏆 TOP 5 MOST COMPREHENSIVE ARTICLES:")
            for i, article in enumerate(content_articles[:5], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   📊 {article['char_count']} chars, {article['word_count']} words")
                print(f"   🏢 {article['publisher']}")
                print(f"   📅 {article['published_date']}")
                print(f"   🔗 {article['link']}")
                
                if article.get('full_content'):
                    preview = article['full_content'][:150] + "..." if len(article['full_content']) > 150 else article['full_content']
                    print(f"   📝 {preview}")
        
        # Additional sources info
        print(f"\n🌐 ADDITIONAL SOURCES AVAILABLE")
        print("-" * 60)
        print("• Google News integration (requires API setup)")
        print("• Reddit discussions (requires PRAW setup)")
        print("• Financial news websites (requires web scraping)")
        print("• SEC filings integration")
        
        return analysis
    
    def export_news_data(self, filename=None, yahoo_limit=50):
        """
        Export comprehensive news data to JSON file
        
        Args:
            filename (str): Output filename (optional)
            yahoo_limit (int): Yahoo Finance news limit
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.symbol}_comprehensive_news_{timestamp}.json"
        
        analysis = self.get_comprehensive_news_analysis(yahoo_limit=yahoo_limit)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Comprehensive news data exported to: {filename}")
        return filename
    
    def _format_timestamp(self, timestamp):
        """Convert Unix timestamp to readable date format"""
        try:
            if timestamp:
                return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return 'N/A'
        except:
            return 'N/A'
    
    def _calculate_content_stats(self, articles):
        """Calculate content statistics for articles"""
        if not articles:
            return {}
        
        content_articles = [a for a in articles if not a.get('error') and a.get('char_count', 0) > 0]
        
        if not content_articles:
            return {'articles_with_content': 0}
        
        char_counts = [a['char_count'] for a in content_articles]
        word_counts = [a['word_count'] for a in content_articles]
        publishers = list(set(a['publisher'] for a in content_articles))
        
        return {
            'articles_with_content': len(content_articles),
            'avg_content_length': sum(char_counts) / len(char_counts),
            'max_content_length': max(char_counts),
            'min_content_length': min(char_counts),
            'avg_word_count': sum(word_counts) / len(word_counts),
            'max_word_count': max(word_counts),
            'unique_publishers': len(publishers),
            'publisher_list': publishers
        }
    
    def _calculate_data_quality(self, yahoo_data):
        """Calculate data quality score"""
        if not yahoo_data.get('articles'):
            return 0
        
        total_articles = len(yahoo_data['articles'])
        articles_with_content = len([a for a in yahoo_data['articles'] if a.get('char_count', 0) > 0])
        
        if total_articles == 0:
            return 0
        
        return (articles_with_content / total_articles) * 100
    
    def _analyze_content_diversity(self, yahoo_data):
        """Analyze content diversity"""
        if not yahoo_data.get('articles'):
            return {}
        
        articles = [a for a in yahoo_data['articles'] if not a.get('error')]
        
        publishers = [a.get('publisher', 'Unknown') for a in articles]
        categories = [a.get('category', 'General') for a in articles]
        
        return {
            'unique_publishers': len(set(publishers)),
            'unique_categories': len(set(categories)),
            'publisher_distribution': {pub: publishers.count(pub) for pub in set(publishers)},
            'category_distribution': {cat: categories.count(cat) for cat in set(categories)}
        }


# Example usage and demonstrations
if __name__ == "__main__":
    print("🚀 Comprehensive News Analyzer")
    print("=" * 50)
    
    # Example stocks to analyze
    test_symbols = ["AAPL", "TSLA", "GOOGL"]
    
    for symbol in test_symbols:
        print(f"\n{'='*80}")
        print(f"ANALYZING {symbol}")
        print(f"{'='*80}")
        
        analyzer = ComprehensiveNewsAnalyzer(symbol)
        
        # Get comprehensive analysis
        analysis = analyzer.print_comprehensive_analysis(yahoo_limit=30)
        
        # Export data
        filename = analyzer.export_news_data(yahoo_limit=30)
        
        print(f"\n✅ Analysis complete for {symbol}")
        print(f"📁 Data exported to: {filename}")
        
        print("\n" + "-"*80)
        input("Press Enter to continue to next stock...")
