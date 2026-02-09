#!/usr/bin/env python3
"""
Manager: Orchestrates all scrapers with fault tolerance and 24h filtering
"""

import sys
import os
from datetime import datetime, timezone, timedelta

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from storage_manager import load_articles, save_articles, merge_articles
from scrape_bensbites import scrape_bensbites
from scrape_rundown import scrape_rundown
from scrape_reddit import scrape_reddit


def filter_last_24h(articles: list) -> list:
    """
    Filter articles to only include those from the last 24 hours.
    Exception: Always keep articles with saved=True.
    """
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
    filtered = []
    
    for article in articles:
        # Always keep saved articles
        if article.get('saved', False):
            filtered.append(article)
            continue
        
        # Parse published_at
        try:
            # Handle both ISO format with and without 'Z'
            pub_str = article['published_at']
            if pub_str.endswith('Z'):
                pub_str = pub_str[:-1] + '+00:00'
            
            published_at = datetime.fromisoformat(pub_str)
            
            # Ensure timezone aware
            if published_at.tzinfo is None:
                published_at = published_at.replace(tzinfo=timezone.utc)
            
            # Check if within 24h
            if published_at >= cutoff_time:
                filtered.append(article)
                
        except Exception as e:
            print(f"⚠️  Could not parse date for {article.get('title', 'Unknown')}: {e}")
            # Include article if we can't parse date (fail safe)
            filtered.append(article)
    
    return filtered


def run_scrapers():
    """
    Run all scrapers with fault tolerance.
    Logs errors but continues if one scraper fails.
    """
    print("=" * 60)
    print("🚀 AI News Dashboard - Scraper Manager")
    print("=" * 60)
    print()
    
    all_articles = []
    errors = []
    
    # Run Ben's Bites scraper
    print("1️⃣  Ben's Bites")
    print("-" * 60)
    try:
        bb_articles = scrape_bensbites()
        all_articles.extend(bb_articles)
        print()
    except Exception as e:
        error_msg = f"Ben's Bites scraper failed: {e}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        print()
    
    # Run The AI Rundown scraper
    print("2️⃣  The AI Rundown")
    print("-" * 60)
    try:
        rd_articles = scrape_rundown()
        all_articles.extend(rd_articles)
        print()
    except Exception as e:
        error_msg = f"The AI Rundown scraper failed: {e}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        print()
    
    # Run Reddit scraper
    print("3️⃣  Reddit")
    print("-" * 60)
    try:
        reddit_articles = scrape_reddit()
        all_articles.extend(reddit_articles)
        print()
    except Exception as e:
        error_msg = f"Reddit scraper failed: {e}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Scraping Summary")
    print("=" * 60)
    print(f"Total articles fetched: {len(all_articles)}")
    
    if errors:
        print(f"⚠️  Errors encountered: {len(errors)}")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ All scrapers completed successfully")
    
    print()
    
    # Filter to last 24h
    print("🔍 Filtering to last 24 hours...")
    filtered_articles = filter_last_24h(all_articles)
    print(f"   Kept {len(filtered_articles)} articles (within 24h or saved)")
    print()
    
    # Load existing articles and merge
    print("💾 Merging with existing articles...")
    existing_data = load_articles()
    existing_articles = existing_data.get('articles', [])
    
    merged_articles = merge_articles(existing_articles, filtered_articles)
    print(f"   Total articles after merge: {len(merged_articles)}")
    print()
    
    # Save to storage
    print("💾 Saving to storage...")
    success = save_articles(merged_articles)
    
    if success:
        print("✅ Articles saved successfully")
    else:
        print("❌ Failed to save articles")
    
    print()
    print("=" * 60)
    print("🎉 Scraping complete!")
    print("=" * 60)
    
    # Log to progress.md
    log_to_progress(len(all_articles), len(filtered_articles), len(merged_articles), errors)


def log_to_progress(fetched: int, filtered: int, total: int, errors: list):
    """Log execution to progress.md"""
    progress_path = os.path.join(os.path.dirname(__file__), '..', 'progress.md')
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    log_entry = f"\n## [{timestamp}] Scraper Run\n"
    log_entry += f"- Fetched: {fetched} articles\n"
    log_entry += f"- Filtered (24h): {filtered} articles\n"
    log_entry += f"- Total in storage: {total} articles\n"
    
    if errors:
        log_entry += f"- Errors: {len(errors)}\n"
        for error in errors:
            log_entry += f"  - {error}\n"
    else:
        log_entry += "- Status: ✅ All scrapers successful\n"
    
    try:
        with open(progress_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"⚠️  Could not log to progress.md: {e}")


if __name__ == "__main__":
    run_scrapers()
