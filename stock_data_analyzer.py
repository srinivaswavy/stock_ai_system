"""
Yahoo Finance Stock Data Analyzer
A comprehensive Python script to fetch and analyze stock data using Yahoo Finance API
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from urllib.parse import urlparse
import os

class StockAnalyzer:
    def __init__(self, symbol):
        """
        Initialize the Stock Analyzer with a stock symbol
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
        """
        self.symbol = symbol.upper()
        self.stock = yf.Ticker(self.symbol)
        
    def get_stock_info(self):
        """
        Get basic information about the stock
        
        Returns:
            dict: Stock information
        """
        try:
            info = self.stock.info
            return {
                'Symbol': self.symbol,
                'Company Name': info.get('longName', 'N/A'),
                'Current Price': info.get('currentPrice', 'N/A'),
                'Market Cap': info.get('marketCap', 'N/A'),
                'PE Ratio': info.get('trailingPE', 'N/A'),
                'Dividend Yield': info.get('dividendYield', 'N/A'),
                '52 Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52 Week Low': info.get('fiftyTwoWeekLow', 'N/A'),
                'Sector': info.get('sector', 'N/A'),
                'Industry': info.get('industry', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return None
    
    def get_historical_data(self, period="1y", interval="1d"):
        """
        Get historical stock data
        
        Args:
            period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval (str): Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            pandas.DataFrame: Historical stock data
        """
        try:
            data = self.stock.history(period=period, interval=interval)
            return data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None
    
    def get_custom_date_range(self, start_date, end_date):
        """
        Get historical data for a custom date range
        
        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
        
        Returns:
            pandas.DataFrame: Historical stock data
        """
        try:
            data = self.stock.history(start=start_date, end=end_date)
            return data
        except Exception as e:
            print(f"Error fetching custom date range data: {e}")
            return None
    
    def plot_price_chart(self, period="1y", save_chart=False):
        """
        Plot stock price chart
        
        Args:
            period (str): Time period for the chart
            save_chart (bool): Whether to save the chart as an image
        """
        data = self.get_historical_data(period=period)
        
        if data is None or data.empty:
            print("No data available for plotting")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label=f'{self.symbol} Close Price', linewidth=2)
        plt.title(f'{self.symbol} Stock Price - {period.upper()}')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_chart:
            filename = f"{self.symbol}_price_chart_{period}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Chart saved as {filename}")
        
        plt.show()
    
    def calculate_moving_averages(self, period="1y", windows=[20, 50, 200]):
        """
        Calculate moving averages for the stock
        
        Args:
            period (str): Time period for data
            windows (list): List of window sizes for moving averages
        
        Returns:
            pandas.DataFrame: Data with moving averages
        """
        data = self.get_historical_data(period=period)
        
        if data is None or data.empty:
            print("No data available for moving averages")
            return None
        
        for window in windows:
            data[f'MA_{window}'] = data['Close'].rolling(window=window).mean()
        
        return data
    
    def plot_with_moving_averages(self, period="1y", windows=[20, 50, 200], save_chart=False):
        """
        Plot stock price with moving averages
        
        Args:
            period (str): Time period for the chart
            windows (list): List of window sizes for moving averages
            save_chart (bool): Whether to save the chart as an image
        """
        data = self.calculate_moving_averages(period=period, windows=windows)
        
        if data is None:
            return
        
        plt.figure(figsize=(14, 8))
        plt.plot(data.index, data['Close'], label=f'{self.symbol} Close Price', linewidth=2)
        
        colors = ['orange', 'red', 'purple']
        for i, window in enumerate(windows):
            color = colors[i] if i < len(colors) else 'gray'
            plt.plot(data.index, data[f'MA_{window}'], 
                    label=f'{window}-day MA', linewidth=1.5, color=color)
        
        plt.title(f'{self.symbol} Stock Price with Moving Averages - {period.upper()}')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_chart:
            filename = f"{self.symbol}_ma_chart_{period}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Chart saved as {filename}")
        
        plt.show()
    
    def get_financial_data(self):
        """
        Get financial statements data
        
        Returns:
            dict: Dictionary containing financial data
        """
        try:
            return {
                'income_statement': self.stock.financials,
                'balance_sheet': self.stock.balance_sheet,
                'cash_flow': self.stock.cashflow
            }
        except Exception as e:
            print(f"Error fetching financial data: {e}")
            return None
    
    def get_dividend_data(self):
        """
        Get dividend data
        
        Returns:
            pandas.Series: Dividend data
        """
        try:
            return self.stock.dividends
        except Exception as e:
            print(f"Error fetching dividend data: {e}")
            return None
    
    def get_news(self, limit=20):
        """
        Get latest news for the stock
        
        Args:
            limit (int): Number of news articles to retrieve (default: 20, increased from 10)
        
        Returns:
            list: List of news articles with title, summary, link, and publication date
        """
        try:
            # Get news from Yahoo Finance
            news_data = self.stock.news
            
            if not news_data:
                return None
            
            # Don't limit too strictly - get all available news up to the limit
            news_data = news_data[:limit] if len(news_data) > limit else news_data
            
            formatted_news = []
            for article in news_data:
                try:
                    # Extract content from the nested structure
                    content = article.get('content', {})
                    
                    # Extract relevant fields
                    title = content.get('title', 'No title available')
                    summary = content.get('summary', content.get('description', ''))
                    
                    # If summary is empty, try to get from other fields
                    if not summary:
                        summary = content.get('intro', content.get('excerpt', ''))
                    
                    # Handle link extraction - it might be nested in different ways
                    link = content.get('canonicalUrl', content.get('clickThroughUrl', ''))
                    if isinstance(link, dict):
                        link = link.get('url', str(link))
                    
                    provider = content.get('provider', {})
                    publisher = provider.get('displayName', 'Unknown') if isinstance(provider, dict) else str(provider)
                    
                    # Handle timestamp
                    pub_date = content.get('pubDate', 0)
                    if isinstance(pub_date, str):
                        # If it's already a string, keep it
                        published_date = pub_date
                    else:
                        # If it's a timestamp, convert it
                        published_date = self._format_timestamp(pub_date)
                    
                    formatted_article = {
                        'title': title,
                        'summary': summary,  # Keep full summary without any truncation
                        'link': link,
                        'publisher': publisher,
                        'published_date': published_date
                    }
                    formatted_news.append(formatted_article)
                    
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
            
            return formatted_news if formatted_news else None
            
        except Exception as e:
            print(f"Error fetching news for {self.symbol}: {e}")
            return None
    
    def _format_timestamp(self, timestamp):
        """
        Convert Unix timestamp to readable date format
        
        Args:
            timestamp (int): Unix timestamp
        
        Returns:
            str: Formatted date string
        """
        try:
            if timestamp:
                return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return 'N/A'
        except:
            return 'N/A'
    
    def print_news(self, limit=5):
        """
        Print latest news for the stock in a formatted way
        
        Args:
            limit (int): Number of news articles to display (default: 5)
        
        Returns:
            list: List of formatted news articles (same as get_news)
        """
        print(f"\n{'='*60}")
        print(f"LATEST NEWS FOR {self.symbol}")
        print(f"{'='*60}")
        
        news = self.get_news(limit=limit)
        
        if not news:
            print("No news available for this stock.")
            return []
        
        for i, article in enumerate(news, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Publisher: {article['publisher']}")
            print(f"   Date: {article['published_date']}")
            
            # Print full summary if available
            summary = article['summary']
            if summary and summary != 'N/A':
                print(f"   Summary: {summary}")
            
            print(f"   Link: {article['link']}")
            print("-" * 60)
        
        print(f"\nShowing {len(news)} latest news articles for {self.symbol}")
        print(f"{'='*60}")
        
        # Return the news data for programmatic use
        return news
    
    def get_stock_recommendations(self):
        """
        Get analyst recommendations for the stock
        
        Returns:
            pandas.DataFrame: Analyst recommendations
        """
        try:
            recommendations = self.stock.recommendations
            return recommendations
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return None
    
    def get_calendar_events(self):
        """
        Get upcoming calendar events (earnings, etc.)
        
        Returns:
            dict or pandas.DataFrame: Calendar events
        """
        try:
            calendar = self.stock.calendar
            return calendar
        except Exception as e:
            print(f"Error fetching calendar events: {e}")
            return None
    
    def print_summary(self, include_news=True):
        """
        Print a summary of the stock
        
        Args:
            include_news (bool): Whether to include latest news (default: True)
        
        Returns:
            dict: Dictionary containing stock info, news, and analysis data
        """
        print(f"\n{'='*50}")
        print(f"STOCK ANALYSIS SUMMARY FOR {self.symbol}")
        print(f"{'='*50}")
        
        info = self.get_stock_info()
        if info:
            for key, value in info.items():
                print(f"{key:15}: {value}")
        
        print(f"\n{'='*50}")
        
        # Get news data
        news_data = []
        if include_news:
            news_data = self.print_news(limit=5)  # Increased from 3 to 5 for summary
        
        # Return structured data for programmatic use
        return {
            'symbol': self.symbol,
            'stock_info': info,
            'news': news_data,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_comprehensive_analysis(self, period="3mo", include_news=True, news_limit=10):
        """
        Get comprehensive stock analysis data without printing
        
        Args:
            period (str): Time period for historical data analysis
            include_news (bool): Whether to include news data
            news_limit (int): Number of news articles to include
        
        Returns:
            dict: Comprehensive analysis data structure
        """
        try:
            # Get basic stock info
            stock_info = self.get_stock_info()
            
            # Get historical data
            historical_data = self.get_historical_data(period=period)
            
            # Calculate statistics
            analysis_stats = {}
            if historical_data is not None and not historical_data.empty:
                current_price = historical_data['Close'].iloc[-1]
                prev_close = historical_data['Close'].iloc[-2] if len(historical_data) > 1 else current_price
                
                analysis_stats = {
                    'current_price': current_price,
                    'previous_close': prev_close,
                    'daily_change': current_price - prev_close,
                    'daily_change_pct': ((current_price - prev_close) / prev_close * 100) if prev_close != 0 else 0,
                    'period_high': historical_data['High'].max(),
                    'period_low': historical_data['Low'].min(),
                    'average_volume': historical_data['Volume'].mean(),
                    'period_start_price': historical_data['Close'].iloc[0],
                    'period_change': current_price - historical_data['Close'].iloc[0],
                    'period_change_pct': ((current_price - historical_data['Close'].iloc[0]) / historical_data['Close'].iloc[0] * 100) if historical_data['Close'].iloc[0] != 0 else 0,
                    'total_days': len(historical_data)
                }
            
            # Get moving averages
            ma_data = self.calculate_moving_averages(period=period, windows=[20, 50, 200])
            ma_analysis = {}
            if ma_data is not None and not ma_data.empty:
                latest_price = ma_data['Close'].iloc[-1]
                ma_analysis = {
                    'ma_20': ma_data['MA_20'].iloc[-1] if not pd.isna(ma_data['MA_20'].iloc[-1]) else None,
                    'ma_50': ma_data['MA_50'].iloc[-1] if not pd.isna(ma_data['MA_50'].iloc[-1]) else None,
                    'ma_200': ma_data['MA_200'].iloc[-1] if not pd.isna(ma_data['MA_200'].iloc[-1]) else None,
                    'price_above_ma_20': latest_price > ma_data['MA_20'].iloc[-1] if not pd.isna(ma_data['MA_20'].iloc[-1]) else None,
                    'price_above_ma_50': latest_price > ma_data['MA_50'].iloc[-1] if not pd.isna(ma_data['MA_50'].iloc[-1]) else None,
                    'price_above_ma_200': latest_price > ma_data['MA_200'].iloc[-1] if not pd.isna(ma_data['MA_200'].iloc[-1]) else None
                }
                
                # Determine trend signal
                if (ma_analysis['price_above_ma_20'] and ma_analysis['price_above_ma_50'] and ma_analysis['price_above_ma_200']):
                    ma_analysis['trend_signal'] = 'BULLISH'
                elif (not ma_analysis['price_above_ma_20'] and not ma_analysis['price_above_ma_50'] and not ma_analysis['price_above_ma_200']):
                    ma_analysis['trend_signal'] = 'BEARISH'
                else:
                    ma_analysis['trend_signal'] = 'MIXED'
            
            # Get analyst recommendations
            recommendations = self.get_stock_recommendations()
            rec_analysis = {}
            if recommendations is not None and not recommendations.empty:
                latest_rec = recommendations.iloc[0]
                total_analysts = sum([
                    latest_rec.get('strongBuy', 0), 
                    latest_rec.get('buy', 0),
                    latest_rec.get('hold', 0), 
                    latest_rec.get('sell', 0), 
                    latest_rec.get('strongSell', 0)
                ])
                
                if total_analysts > 0:
                    rec_analysis = {
                        'total_analysts': total_analysts,
                        'strong_buy': latest_rec.get('strongBuy', 0),
                        'buy': latest_rec.get('buy', 0),
                        'hold': latest_rec.get('hold', 0),
                        'sell': latest_rec.get('sell', 0),
                        'strong_sell': latest_rec.get('strongSell', 0),
                        'buy_ratio': (latest_rec.get('strongBuy', 0) + latest_rec.get('buy', 0)) / total_analysts * 100
                    }
            
            # Get news if requested
            news_data = []
            if include_news:
                news_data = self.get_news(limit=news_limit) or []
            
            # Get calendar events
            calendar_events = self.get_calendar_events()
            
            # Compile comprehensive analysis
            comprehensive_analysis = {
                'symbol': self.symbol,
                'timestamp': datetime.now().isoformat(),
                'analysis_period': period,
                'stock_info': stock_info,
                'price_analysis': analysis_stats,
                'technical_analysis': ma_analysis,
                'analyst_recommendations': rec_analysis,
                'news': news_data,
                'calendar_events': calendar_events,
                'raw_data': {
                    'historical_data_shape': historical_data.shape if historical_data is not None else None,
                    'has_recommendations': recommendations is not None and not recommendations.empty,
                    'news_count': len(news_data),
                    'has_calendar': calendar_events is not None
                }
            }
            
            return comprehensive_analysis
            
        except Exception as e:
            return {
                'symbol': self.symbol,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'success': False
            }
    
    def get_price_statistics(self, period="1mo"):
        """
        Get price statistics for a given period
        
        Args:
            period (str): Time period for analysis
        
        Returns:
            dict: Price statistics
        """
        data = self.get_historical_data(period=period)
        
        if data is None or data.empty:
            return None
        
        current_price = data['Close'].iloc[-1]
        start_price = data['Close'].iloc[0]
        
        return {
            'symbol': self.symbol,
            'period': period,
            'current_price': current_price,
            'start_price': start_price,
            'high': data['High'].max(),
            'low': data['Low'].min(),
            'change': current_price - start_price,
            'change_pct': ((current_price - start_price) / start_price * 100) if start_price != 0 else 0,
            'average_volume': data['Volume'].mean(),
            'total_volume': data['Volume'].sum(),
            'trading_days': len(data),
            'volatility': data['Close'].pct_change().std() * 100,  # Daily volatility as percentage
            'last_5_days': data.tail(5)[['Open', 'High', 'Low', 'Close', 'Volume']].to_dict('records')
        }
    
    def get_extended_news(self, limit=50):
        """
        Get extended news coverage with maximum available articles
        
        Args:
            limit (int): Maximum number of news articles to retrieve (default: 50)
        
        Returns:
            dict: Extended news data with metadata
        """
        try:
            # Get all available news
            all_news = self.stock.news
            
            if not all_news:
                return {
                    'symbol': self.symbol,
                    'total_articles': 0,
                    'articles': [],
                    'error': 'No news available'
                }
            
            # Take up to the limit, but don't restrict if we have less
            news_subset = all_news[:limit] if len(all_news) > limit else all_news
            
            formatted_articles = []
            for i, article in enumerate(news_subset):
                try:
                    content = article.get('content', {})
                    
                    # Extract all possible text content
                    title = content.get('title', f'Article {i+1}')
                    summary = content.get('summary', '')
                    description = content.get('description', '')
                    intro = content.get('intro', '')
                    excerpt = content.get('excerpt', '')
                    
                    # Combine all available text for maximum content
                    full_content = summary
                    if not full_content and description:
                        full_content = description
                    if not full_content and intro:
                        full_content = intro
                    if not full_content and excerpt:
                        full_content = excerpt
                    
                    # Extract metadata
                    provider = content.get('provider', {})
                    publisher = provider.get('displayName', 'Unknown Source') if isinstance(provider, dict) else str(provider)
                    
                    link = content.get('canonicalUrl', content.get('clickThroughUrl', ''))
                    if isinstance(link, dict):
                        link = link.get('url', str(link))
                    
                    pub_date = content.get('pubDate', 0)
                    published_date = pub_date if isinstance(pub_date, str) else self._format_timestamp(pub_date)
                    
                    # Additional metadata if available
                    content_type = content.get('contentType', 'STORY')
                    thumbnail = content.get('thumbnail', {})
                    
                    formatted_article = {
                        'article_number': i + 1,
                        'title': title,
                        'full_content': full_content,
                        'content_length': len(full_content),
                        'publisher': publisher,
                        'published_date': published_date,
                        'link': link,
                        'content_type': content_type,
                        'has_thumbnail': bool(thumbnail),
                        'raw_fields': list(content.keys())  # Show what fields are available
                    }
                    
                    formatted_articles.append(formatted_article)
                    
                except Exception as e:
                    formatted_articles.append({
                        'article_number': i + 1,
                        'error': f'Error processing article: {str(e)}',
                        'raw_content': str(article)[:200] + '...'
                    })
            
            return {
                'symbol': self.symbol,
                'timestamp': datetime.now().isoformat(),
                'total_available': len(all_news),
                'total_processed': len(formatted_articles),
                'articles': formatted_articles,
                'content_stats': {
                    'articles_with_content': len([a for a in formatted_articles if a.get('content_length', 0) > 0]),
                    'average_content_length': sum(a.get('content_length', 0) for a in formatted_articles) / len(formatted_articles) if formatted_articles else 0,
                    'longest_article': max((a.get('content_length', 0) for a in formatted_articles), default=0),
                    'publishers': list(set(a.get('publisher', 'Unknown') for a in formatted_articles))
                }
            }
            
        except Exception as e:
            return {
                'symbol': self.symbol,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'total_articles': 0,
                'articles': []
            }
    
    def print_extended_news(self, limit=25):
        """
        Print extended news with comprehensive coverage
        
        Args:
            limit (int): Number of articles to display (default: 25)
        
        Returns:
            dict: Extended news data
        """
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE NEWS COVERAGE FOR {self.symbol}")
        print(f"{'='*80}")
        
        extended_news = self.get_extended_news(limit=limit)
        
        if extended_news.get('error'):
            print(f"Error: {extended_news['error']}")
            return extended_news
        
        # Print statistics
        stats = extended_news['content_stats']
        print(f"\n📊 NEWS COVERAGE STATISTICS:")
        print(f"   Total Available Articles: {extended_news['total_available']}")
        print(f"   Articles Processed: {extended_news['total_processed']}")
        print(f"   Articles with Content: {stats['articles_with_content']}")
        print(f"   Average Content Length: {stats['average_content_length']:.0f} characters")
        print(f"   Longest Article: {stats['longest_article']} characters")
        print(f"   Publishers: {', '.join(stats['publishers'][:5])}{'...' if len(stats['publishers']) > 5 else ''}")
        
        # Print articles
        articles = extended_news['articles']
        for article in articles:
            if 'error' in article:
                print(f"\n❌ Article {article['article_number']}: {article['error']}")
                continue
                
            print(f"\n📰 Article {article['article_number']}: {article['title']}")
            print(f"   📅 Date: {article['published_date']}")
            print(f"   🏢 Publisher: {article['publisher']}")
            print(f"   📝 Content Length: {article['content_length']} characters")
            
            if article['full_content']:
                # Show full content without truncation
                print(f"   📖 Content: {article['full_content']}")
            else:
                print(f"   📖 Content: [No summary available]")
                
            print(f"   🔗 Link: {article['link']}")
            print(f"   🔧 Available Fields: {', '.join(article['raw_fields'])}")
            print("-" * 80)
        
        print(f"\n✅ Comprehensive news coverage complete for {self.symbol}")
        print(f"{'='*80}")
        
        return extended_news
    
    def get_ultra_comprehensive_news(self, limit=500):
        """
        Get ultra-comprehensive news with maximum possible coverage
        
        Args:
            limit (int): Maximum number of news articles to retrieve (default: 100)
        
        Returns:
            dict: Ultra-comprehensive news data with enhanced analysis
        """
        try:
            # Get all available news without initial filtering
            all_news = self.stock.news
            
            if not all_news:
                return {
                    'symbol': self.symbol,
                    'status': 'no_news',
                    'total_articles': 0,
                    'articles': [],
                    'error': 'No news available from Yahoo Finance'
                }
            
            print(f"🔍 Processing {len(all_news)} available news articles for {self.symbol}...")
            
            # Process all available articles (up to limit)
            news_to_process = all_news[:limit] if len(all_news) > limit else all_news
            
            processed_articles = []
            content_analysis = {
                'total_characters': 0,
                'total_words': 0,
                'articles_with_substantial_content': 0,
                'unique_publishers': set(),
                'date_range': {'earliest': None, 'latest': None},
                'content_types': {},
                'link_domains': set()
            }
            
            for i, article in enumerate(news_to_process):
                try:
                    content = article.get('content', {})
                    
                    # Extract comprehensive text content
                    text_fields = ['summary', 'description', 'intro', 'excerpt', 'body', 'text']
                    combined_text = ''
                    content_sources = []
                    
                    for field in text_fields:
                        field_content = content.get(field, '')
                        if field_content and isinstance(field_content, str):
                            if field_content not in combined_text:
                                combined_text += f" {field_content}"
                                content_sources.append(field)
                    
                    combined_text = combined_text.strip()
                    
                    # Enhanced metadata extraction
                    title = content.get('title', f'Article {i+1}')
                    
                    # Publisher information
                    provider = content.get('provider', {})
                    if isinstance(provider, dict):
                        publisher = provider.get('displayName', 'Unknown Source')
                        publisher_domain = provider.get('url', '')
                    else:
                        publisher = str(provider) if provider else 'Unknown Source'
                        publisher_domain = ''
                    
                    # Link extraction and analysis
                    link = content.get('canonicalUrl', content.get('clickThroughUrl', ''))
                    if isinstance(link, dict):
                        link = link.get('url', str(link))
                    
                    # Extract domain from link
                    link_domain = ''
                    if link:
                        try:
                            from urllib.parse import urlparse
                            parsed_url = urlparse(link)
                            link_domain = parsed_url.netloc
                            content_analysis['link_domains'].add(link_domain)
                        except:
                            pass
                    
                    # Date processing
                    pub_date = content.get('pubDate', 0)
                    if isinstance(pub_date, str):
                        published_date = pub_date
                        try:
                            # Try to parse the date for range analysis
                            from dateutil import parser
                            parsed_date = parser.parse(pub_date)
                            if content_analysis['date_range']['earliest'] is None or parsed_date < content_analysis['date_range']['earliest']:
                                content_analysis['date_range']['earliest'] = parsed_date
                            if content_analysis['date_range']['latest'] is None or parsed_date > content_analysis['date_range']['latest']:
                                content_analysis['date_range']['latest'] = parsed_date
                        except:
                            pass
                    else:
                        published_date = self._format_timestamp(pub_date)
                        if pub_date:
                            try:
                                parsed_date = datetime.fromtimestamp(pub_date)
                                if content_analysis['date_range']['earliest'] is None or parsed_date < content_analysis['date_range']['earliest']:
                                    content_analysis['date_range']['earliest'] = parsed_date
                                if content_analysis['date_range']['latest'] is None or parsed_date > content_analysis['date_range']['latest']:
                                    content_analysis['date_range']['latest'] = parsed_date
                            except:
                                pass
                    
                    # Content analysis
                    char_count = len(combined_text)
                    word_count = len(combined_text.split()) if combined_text else 0
                    
                    # Determine if article has substantial content
                    substantial_content = char_count > 100  # Threshold for substantial content
                    if substantial_content:
                        content_analysis['articles_with_substantial_content'] += 1
                    
                    content_analysis['total_characters'] += char_count
                    content_analysis['total_words'] += word_count
                    content_analysis['unique_publishers'].add(publisher)
                    
                    # Content type analysis
                    content_type = content.get('contentType', 'STORY')
                    content_analysis['content_types'][content_type] = content_analysis['content_types'].get(content_type, 0) + 1
                    
                    # Additional metadata
                    thumbnail = content.get('thumbnail', {})
                    category = content.get('category', '')
                    tags = content.get('tags', [])
                    
                    # Sentiment indicators (basic)
                    sentiment_keywords = {
                        'positive': ['rise', 'gain', 'profit', 'growth', 'buy', 'bullish', 'upgrade', 'strong'],
                        'negative': ['fall', 'loss', 'decline', 'drop', 'sell', 'bearish', 'downgrade', 'weak'],
                        'neutral': ['stable', 'holds', 'maintains', 'expects', 'analyst', 'report']
                    }
                    
                    sentiment_score = {'positive': 0, 'negative': 0, 'neutral': 0}
                    text_for_sentiment = (title + ' ' + combined_text).lower()
                    
                    for sentiment, keywords in sentiment_keywords.items():
                        sentiment_score[sentiment] = sum(1 for keyword in keywords if keyword in text_for_sentiment)
                    
                    # Create comprehensive article record
                    article_data = {
                        'id': i + 1,
                        'title': title,
                        'full_content': combined_text,
                        'content_sources': content_sources,
                        'char_count': char_count,
                        'word_count': word_count,
                        'substantial_content': substantial_content,
                        'publisher': publisher,
                        'publisher_domain': publisher_domain,
                        'published_date': published_date,
                        'link': link,
                        'link_domain': link_domain,
                        'content_type': content_type,
                        'category': category,
                        'tags': tags,
                        'has_thumbnail': bool(thumbnail),
                        'thumbnail_url': thumbnail.get('url', '') if isinstance(thumbnail, dict) else '',
                        'sentiment_indicators': sentiment_score,
                        'raw_fields_available': list(content.keys()),
                        'processing_timestamp': datetime.now().isoformat()
                    }
                    
                    processed_articles.append(article_data)
                    
                except Exception as e:
                    # Include error articles for debugging
                    processed_articles.append({
                        'id': i + 1,
                        'error': f'Processing error: {str(e)}',
                        'raw_preview': str(article)[:300] + '...',
                        'processing_timestamp': datetime.now().isoformat()
                    })
            
            # Finalize content analysis
            content_analysis['unique_publishers'] = list(content_analysis['unique_publishers'])
            content_analysis['link_domains'] = list(content_analysis['link_domains'])
            content_analysis['date_range']['earliest'] = content_analysis['date_range']['earliest'].isoformat() if content_analysis['date_range']['earliest'] else None
            content_analysis['date_range']['latest'] = content_analysis['date_range']['latest'].isoformat() if content_analysis['date_range']['latest'] else None
            
            # Calculate additional statistics
            articles_with_content = [a for a in processed_articles if not a.get('error') and a.get('char_count', 0) > 0]
            
            quality_metrics = {
                'coverage_ratio': len(articles_with_content) / len(processed_articles) if processed_articles else 0,
                'avg_content_length': content_analysis['total_characters'] / len(articles_with_content) if articles_with_content else 0,
                'avg_word_count': content_analysis['total_words'] / len(articles_with_content) if articles_with_content else 0,
                'publisher_diversity': len(content_analysis['unique_publishers']),
                'content_type_diversity': len(content_analysis['content_types']),
                'substantial_content_ratio': content_analysis['articles_with_substantial_content'] / len(processed_articles) if processed_articles else 0
            }
            
            return {
                'symbol': self.symbol,
                'status': 'success',
                'retrieval_timestamp': datetime.now().isoformat(),
                'total_available_articles': len(all_news),
                'total_processed_articles': len(processed_articles),
                'articles': processed_articles,
                'content_analysis': content_analysis,
                'quality_metrics': quality_metrics,
                'coverage_summary': {
                    'total_characters': content_analysis['total_characters'],
                    'total_words': content_analysis['total_words'],
                    'unique_publishers': len(content_analysis['unique_publishers']),
                    'articles_with_content': len(articles_with_content),
                    'substantial_articles': content_analysis['articles_with_substantial_content']
                }
            }
            
        except Exception as e:
            return {
                'symbol': self.symbol,
                'status': 'error',
                'error': str(e),
                'retrieval_timestamp': datetime.now().isoformat()
            }
    
    def print_ultra_comprehensive_news(self, limit=50):
        """
        Print ultra-comprehensive news analysis with detailed statistics
        
        Args:
            limit (int): Maximum number of articles to process
            
        Returns:
            dict: The comprehensive news data
        """
        print(f"\n{'='*80}")
        print(f"🔍 ULTRA-COMPREHENSIVE NEWS ANALYSIS FOR {self.symbol}")
        print(f"{'='*80}")
        
        news_data = self.get_ultra_comprehensive_news(limit=limit)
        
        if news_data['status'] == 'error':
            print(f"❌ Error retrieving news: {news_data['error']}")
            return news_data
        
        if news_data['status'] == 'no_news':
            print("📰 No news articles available for this symbol")
            return news_data
        
        # Display comprehensive statistics
        print(f"\n📊 COVERAGE STATISTICS")
        print("-" * 60)
        coverage = news_data['coverage_summary']
        quality = news_data['quality_metrics']
        
        print(f"✅ Total articles available: {news_data['total_available_articles']}")
        print(f"✅ Articles processed: {news_data['total_processed_articles']}")
        print(f"✅ Articles with content: {coverage['articles_with_content']}")
        print(f"✅ Substantial articles: {coverage['substantial_articles']}")
        print(f"✅ Total content characters: {coverage['total_characters']:,}")
        print(f"✅ Total words: {coverage['total_words']:,}")
        print(f"✅ Unique publishers: {coverage['unique_publishers']}")
        print(f"✅ Coverage quality: {quality['coverage_ratio']:.1%}")
        print(f"✅ Average article length: {quality['avg_content_length']:.0f} characters")
        
        # Date range
        analysis = news_data['content_analysis']
        if analysis['date_range']['earliest'] and analysis['date_range']['latest']:
            print(f"✅ Date range: {analysis['date_range']['earliest'][:10]} to {analysis['date_range']['latest'][:10]}")
        
        # Publisher breakdown
        if analysis['unique_publishers']:
            print(f"\n📰 PUBLISHERS ({len(analysis['unique_publishers'])} total)")
            print("-" * 60)
            for i, publisher in enumerate(analysis['unique_publishers'][:10], 1):
                print(f"{i:2d}. {publisher}")
            if len(analysis['unique_publishers']) > 10:
                print(f"    ... and {len(analysis['unique_publishers']) - 10} more")
        
        # Content type breakdown
        if analysis['content_types']:
            print(f"\n📝 CONTENT TYPES")
            print("-" * 60)
            for content_type, count in analysis['content_types'].items():
                print(f"• {content_type}: {count} articles")
        
        # Top articles by content length
        articles_with_content = [a for a in news_data['articles'] if not a.get('error') and a.get('char_count', 0) > 0]
        articles_with_content.sort(key=lambda x: x.get('char_count', 0), reverse=True)
        
        print(f"\n🏆 TOP 10 MOST COMPREHENSIVE ARTICLES")
        print("-" * 60)
        
        for i, article in enumerate(articles_with_content[:10], 1):
            print(f"\n{i:2d}. {article['title']}")
            print(f"    📊 {article['char_count']:,} chars | {article['word_count']:,} words")
            print(f"    🏢 {article['publisher']}")
            print(f"    📅 {article['published_date']}")
            print(f"    🔗 {article['link']}")
            
            # Show content preview
            if article.get('full_content'):
                preview = article['full_content'][:200].replace('\n', ' ').strip()
                if len(article['full_content']) > 200:
                    preview += "..."
                print(f"    📝 {preview}")
            
            # Show sentiment indicators if significant
            sentiment = article.get('sentiment_indicators', {})
            if sum(sentiment.values()) > 0:
                sentiment_str = " | ".join([f"{k}: {v}" for k, v in sentiment.items() if v > 0])
                print(f"    💭 Sentiment indicators: {sentiment_str}")
        
        print(f"\n{'='*80}")
        print(f"✅ Ultra-comprehensive analysis complete for {self.symbol}")
        print(f"📊 Processed {coverage['articles_with_content']} articles with {coverage['total_characters']:,} total characters")
        print(f"{'='*80}")
        
        return news_data
    
    def compare_news_methods(self, symbol_list=None):
        """
        Compare different news retrieval methods for analysis
        
        Args:
            symbol_list (list): List of symbols to compare (optional)
            
        Returns:
            dict: Comparison results
        """
        if symbol_list is None:
            symbol_list = [self.symbol]
        
        print(f"\n{'='*80}")
        print("📊 NEWS RETRIEVAL METHODS COMPARISON")
        print(f"{'='*80}")
        
        comparison_results = {}
        
        for symbol in symbol_list:
            print(f"\n🔍 Analyzing {symbol}...")
            
            temp_analyzer = StockAnalyzer(symbol) if symbol != self.symbol else self
            
            # Method 1: Standard news
            standard_news = temp_analyzer.get_news(limit=20)
            standard_count = len(standard_news) if standard_news else 0
            standard_chars = sum(len(a.get('summary', '')) for a in (standard_news or []))
            
            # Method 2: Extended news
            extended_news = temp_analyzer.get_extended_news(limit=30)
            extended_count = len(extended_news.get('articles', []))
            extended_chars = sum(a.get('content_length', 0) for a in extended_news.get('articles', []))
            
            # Method 3: Ultra-comprehensive news
            ultra_news = temp_analyzer.get_ultra_comprehensive_news(limit=50)
            ultra_count = ultra_news.get('total_processed_articles', 0)
            ultra_chars = ultra_news.get('coverage_summary', {}).get('total_characters', 0)
            
            comparison_results[symbol] = {
                'standard_method': {
                    'articles': standard_count,
                    'total_characters': standard_chars,
                    'avg_chars_per_article': standard_chars / standard_count if standard_count > 0 else 0
                },
                'extended_method': {
                    'articles': extended_count,
                    'total_characters': extended_chars,
                    'avg_chars_per_article': extended_chars / extended_count if extended_count > 0 else 0
                },
                'ultra_comprehensive_method': {
                    'articles': ultra_count,
                    'total_characters': ultra_chars,
                    'avg_chars_per_article': ultra_chars / ultra_count if ultra_count > 0 else 0,
                    'unique_publishers': len(ultra_news.get('content_analysis', {}).get('unique_publishers', [])),
                    'coverage_quality': ultra_news.get('quality_metrics', {}).get('coverage_ratio', 0)
                }
            }
            
            # Display results for this symbol
            print(f"\n📊 Results for {symbol}:")
            print(f"   Standard method:        {standard_count:2d} articles, {standard_chars:,} chars")
            print(f"   Extended method:        {extended_count:2d} articles, {extended_chars:,} chars")
            print(f"   Ultra-comprehensive:    {ultra_count:2d} articles, {ultra_chars:,} chars")
            print(f"   Coverage improvement:   {((ultra_chars / standard_chars - 1) * 100) if standard_chars > 0 else 0:.1f}%")
        
        print(f"\n{'='*80}")
        print("✅ News methods comparison complete")
        print(f"{'='*80}")
        
        return comparison_results

    # ...existing code...
    

def analyze_multiple_stocks(symbols, period="1y", show_chart=True, save_chart=False):
    """
    Analyze multiple stocks and compare their performance
    
    Args:
        symbols (list): List of stock symbols
        period (str): Time period for analysis
        show_chart (bool): Whether to display the chart
        save_chart (bool): Whether to save the chart
    
    Returns:
        dict: Analysis results for all stocks with performance data
    """
    results = {
        'symbols': symbols,
        'period': period,
        'timestamp': datetime.now().isoformat(),
        'stock_data': {},
        'comparison_data': []
    }
    
    if show_chart:
        plt.figure(figsize=(14, 8))
    
    for symbol in symbols:
        try:
            analyzer = StockAnalyzer(symbol)
            data = analyzer.get_historical_data(period=period)
            
            if data is not None and not data.empty:
                # Calculate normalized prices
                start_price = data['Close'].iloc[0]
                end_price = data['Close'].iloc[-1]
                normalized_prices = (data['Close'] / start_price - 1) * 100
                
                # Store individual stock data
                results['stock_data'][symbol] = {
                    'start_price': start_price,
                    'end_price': end_price,
                    'total_return_pct': ((end_price - start_price) / start_price * 100),
                    'data_points': len(data),
                    'period_high': data['High'].max(),
                    'period_low': data['Low'].min(),
                    'avg_volume': data['Volume'].mean(),
                    'volatility': data['Close'].pct_change().std() * 100
                }
                
                # Add to comparison data
                results['comparison_data'].append({
                    'symbol': symbol,
                    'return_pct': results['stock_data'][symbol]['total_return_pct'],
                    'volatility': results['stock_data'][symbol]['volatility'],
                    'final_price': end_price
                })
                
                # Add to chart if requested
                if show_chart:
                    plt.plot(data.index, normalized_prices, label=f'{symbol}', linewidth=2)
            
            else:
                results['stock_data'][symbol] = {'error': 'No data available'}
                
        except Exception as e:
            results['stock_data'][symbol] = {'error': str(e)}
    
    # Sort comparison data by return
    results['comparison_data'].sort(key=lambda x: x.get('return_pct', -float('inf')), reverse=True)
    
    # Add summary statistics
    if results['comparison_data']:
        returns = [item['return_pct'] for item in results['comparison_data'] if 'return_pct' in item]
        if returns:
            results['summary'] = {
                'best_performer': results['comparison_data'][0]['symbol'] if results['comparison_data'] else None,
                'worst_performer': results['comparison_data'][-1]['symbol'] if results['comparison_data'] else None,
                'average_return': sum(returns) / len(returns),
                'best_return': max(returns),
                'worst_return': min(returns),
                'stocks_analyzed': len(returns)
            }
    
    # Show and save chart if requested
    if show_chart:
        plt.title(f'Stock Performance Comparison - {period.upper()}')
        plt.xlabel('Date')
        plt.ylabel('Percentage Change (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_chart:
            filename = f"stock_comparison_{period}_{datetime.now().strftime('%Y%m%d')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            results['chart_saved'] = filename
        
        plt.show()
    
    return results


# Example usage and demonstration
if __name__ == "__main__":
    print("Yahoo Finance Stock Data Analyzer")
    print("=" * 40)
    
    # Example 1: Analyze a single stock
    print("\n1. Single Stock Analysis Example (Apple)")
    apple = StockAnalyzer("AAPL")
    summary_data = apple.print_summary(include_news=True)
    
    print(f"\nSummary data returned: {summary_data['symbol']}")
    print(f"News articles included: {len(summary_data['news'])}")
    
    # Get recent data
    print("\nRecent 5 days of data:")
    recent_data = apple.get_historical_data(period="5d")
    if recent_data is not None:
        print(recent_data[['Open', 'High', 'Low', 'Close', 'Volume']].round(2))
    
    # Example of getting structured data
    print("\n2. Getting Structured Data Example")
    comprehensive_data = apple.get_comprehensive_analysis(period="1mo", include_news=False)
    print(f"Comprehensive analysis returned for: {comprehensive_data['symbol']}")
    
    price_stats = apple.get_price_statistics(period="1mo")
    if price_stats:
        print(f"Monthly return: {price_stats['change_pct']:.2f}%")
        print(f"Volatility: {price_stats['volatility']:.2f}%")
    
    # Show additional news if needed
    print("\n" + "="*50)
    print("For more examples, see 'programmatic_usage_example.py'")
    print("All functions now return structured data!")
    print("="*50)
    
    # Example 2: Compare multiple stocks (returns data)
    print("\n3. Multiple Stock Comparison Example")
    tech_stocks = ["AAPL", "GOOGL", "MSFT"]
    comparison_results = analyze_multiple_stocks(tech_stocks, period="1mo", show_chart=False)
    
    if 'summary' in comparison_results:
        print(f"Best performer: {comparison_results['summary']['best_performer']}")
        print(f"Average return: {comparison_results['summary']['average_return']:.2f}%")
    
    print("\n" + "="*50)
    print("Example usage completed!")
    print("All functions now return data structures for programmatic use.")
    print("="*50)
