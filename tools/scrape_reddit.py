#!/usr/bin/env python3
"""
Reddit Scraper: Extracts top AI posts from Reddit
"""

import requests
from datetime import datetime, timezone
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))
from storage_manager import generate_article_id


def scrape_reddit() -> list:
    """
    Scrape top posts from AI-related subreddits.
    Returns list of Article objects.
    """
    subreddits = ['artificial', 'MachineLearning', 'Singularity']
    headers = {'User-Agent': 'AI-News-Dashboard/1.0'}
    articles = []
    
    for subreddit in subreddits:
        url = f"https://reddit.com/r/{subreddit}/top.json?t=day&limit=10"
        
        try:
            print(f"🔍 Fetching r/{subreddit}...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            print(f"📰 Found {len(posts)} posts from r/{subreddit}")
            
            for post_data in posts:
                post = post_data.get('data', {})
                
                # Extract data
                title = post.get('title', '')
                post_url = post.get('url', '')
                upvotes = post.get('ups', 0)
                author = post.get('author', 'Unknown')
                created_utc = post.get('created_utc', time.time())
                
                # Convert timestamp to ISO format
                published_at = datetime.fromtimestamp(created_utc, tz=timezone.utc).isoformat()
                
                # Use selftext as summary if available, otherwise empty
                summary = post.get('selftext', '')[:200]
                if len(post.get('selftext', '')) > 200:
                    summary += "..."
                
                # Create article object
                article = {
                    'id': generate_article_id(post_url),
                    'title': title,
                    'source': 'Reddit',
                    'url': post_url,
                    'summary': summary,
                    'published_at': published_at,
                    'category': f'r/{subreddit}',
                    'saved': False,
                    'metadata': {
                        'author': author,
                        'upvotes': upvotes,
                        'subreddit': subreddit
                    }
                }
                
                articles.append(article)
            
            # Rate limiting between subreddits
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error scraping r/{subreddit}: {e}")
            continue
    
    print(f"✅ Scraped {len(articles)} total posts from Reddit")
    return articles


if __name__ == "__main__":
    articles = scrape_reddit()
    print(f"\n📊 Total articles: {len(articles)}")
    
    if articles:
        print("\nSample article:")
        print(f"  Title: {articles[0]['title']}")
        print(f"  URL: {articles[0]['url']}")
        print(f"  Upvotes: {articles[0]['metadata']['upvotes']}")
        print(f"  Published: {articles[0]['published_at']}")
