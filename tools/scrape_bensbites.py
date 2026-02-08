#!/usr/bin/env python3
"""
Ben's Bites Scraper: Extracts articles from bensbites.com/archive
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import time
import sys
import os
import hashlib

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))
from storage_manager import generate_article_id


def fetch_with_retry(url: str, headers: dict = None, retries: int = 1) -> requests.Response:
    """Fetch URL with retry logic."""
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < retries:
                print(f"⚠️  Retry {attempt + 1}/{retries} for {url}")
                time.sleep(5)
            else:
                raise e


def extract_article_metadata(article_url: str) -> dict:
    """
    Fetch individual article page to extract metadata.
    Returns dict with published_at and summary.
    """
    try:
        response = fetch_with_retry(article_url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Try to find published date (Substack uses <time> tag)
        time_tag = soup.find('time')
        if time_tag and time_tag.get('datetime'):
            published_at = time_tag['datetime']
        else:
            # Fallback to current time
            published_at = datetime.now(timezone.utc).isoformat()
        
        # Try to find summary/description (meta tag)
        meta_desc = soup.find('meta', {'property': 'og:description'}) or \
                    soup.find('meta', {'name': 'description'})
        summary = meta_desc['content'] if meta_desc else ""
        
        # Truncate summary to 200 chars
        if len(summary) > 200:
            summary = summary[:197] + "..."
        
        # Try to find author
        author_tag = soup.find('meta', {'property': 'article:author'}) or \
                     soup.find('a', {'class': 'author'})
        author = author_tag.get('content', 'Ben Tossell') if author_tag else 'Ben Tossell'
        
        return {
            'published_at': published_at,
            'summary': summary,
            'author': author
        }
        
    except Exception as e:
        print(f"⚠️  Could not fetch metadata for {article_url}: {e}")
        return {
            'published_at': datetime.now(timezone.utc).isoformat(),
            'summary': "",
            'author': 'Ben Tossell'
        }


def scrape_bensbites() -> list:
    """
    Scrape Ben's Bites archive.
    Returns list of Article objects.
    """
    archive_url = "https://bensbites.com/archive"
    articles = []
    
    try:
        print("🔍 Fetching Ben's Bites archive...")
        response = fetch_with_retry(archive_url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all article links (they use /p/ pattern)
        article_links = soup.find_all('a', href=lambda x: x and '/p/' in x)
        
        print(f"📰 Found {len(article_links)} potential articles")
        
        # Deduplicate by href
        seen_urls = set()
        unique_links = []
        for link in article_links:
            href = link.get('href')
            if href not in seen_urls:
                seen_urls.add(href)
                unique_links.append(link)
        
        print(f"📰 Processing {len(unique_links)} unique articles (limit: 10)")
        
        # Process first 10 articles (most recent)
        for i, link in enumerate(unique_links[:10]):
            href = link.get('href')
            title = link.get_text(strip=True)
            
            # Make absolute URL
            if href.startswith('/'):
                article_url = f"https://bensbites.com{href}"
            else:
                article_url = href
            
            print(f"  [{i+1}/10] {title[:50]}...")
            
            # Fetch metadata from individual article page
            metadata = extract_article_metadata(article_url)
            
            # Create article object
            article = {
                'id': generate_article_id(article_url),
                'title': title,
                'source': "Ben's Bites",
                'url': article_url,
                'summary': metadata['summary'],
                'published_at': metadata['published_at'],
                'category': 'AI News',
                'saved': False,
                'metadata': {
                    'author': metadata['author'],
                    'newsletter_issue': ''
                }
            }
            
            articles.append(article)
            
            # Rate limiting
            time.sleep(1)
        
        print(f"✅ Scraped {len(articles)} articles from Ben's Bites")
        return articles
        
    except Exception as e:
        print(f"❌ Error scraping Ben's Bites: {e}")
        return []


if __name__ == "__main__":
    articles = scrape_bensbites()
    print(f"\n📊 Total articles: {len(articles)}")
    
    if articles:
        print("\nSample article:")
        print(f"  Title: {articles[0]['title']}")
        print(f"  URL: {articles[0]['url']}")
        print(f"  Published: {articles[0]['published_at']}")
