#!/usr/bin/env python3
"""
Storage Manager: Handles all read/write operations for articles.json
Implements atomic writes and schema validation.
"""

import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

# Path to storage file
STORAGE_PATH = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'articles.json')
BACKUP_PATH = STORAGE_PATH + '.backup'


def generate_article_id(url: str) -> str:
    """Generate unique ID from URL."""
    return hashlib.md5(url.encode()).hexdigest()[:16]


def validate_article(article: Dict) -> bool:
    """Validate article against schema."""
    required_fields = ['id', 'title', 'source', 'url', 'published_at', 'saved']
    
    for field in required_fields:
        if field not in article:
            print(f"⚠️  Missing required field: {field}")
            return False
    
    return True


def load_articles() -> Dict:
    """Load articles from JSON storage."""
    # Fallback to root articles.json if .tmp version is missing (e.g. in fresh CI environment)
    if not os.path.exists(STORAGE_PATH):
        root_path = os.path.join(os.path.dirname(__file__), '..', 'articles.json')
        if os.path.exists(root_path):
            print(f"🔄 Initializing .tmp storage from {root_path}")
            try:
                os.makedirs(os.path.dirname(STORAGE_PATH), exist_ok=True)
                shutil.copy(root_path, STORAGE_PATH)
            except Exception as e:
                print(f"⚠️  Could not copy root articles to .tmp: {e}")

    if not os.path.exists(STORAGE_PATH):
        return {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "articles": []
        }
    
    try:
        with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        # Try to restore from backup
        if os.path.exists(BACKUP_PATH):
            print("🔄 Restoring from backup...")
            shutil.copy(BACKUP_PATH, STORAGE_PATH)
            with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("⚠️  No backup available, returning empty structure")
            return {
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "articles": []
            }


def save_articles(articles: List[Dict]) -> bool:
    """Save articles to JSON storage with atomic write."""
    # Validate all articles
    for article in articles:
        if not validate_article(article):
            print(f"❌ Invalid article: {article.get('title', 'Unknown')}")
            return False
    
    # Create backup of existing file
    if os.path.exists(STORAGE_PATH):
        shutil.copy(STORAGE_PATH, BACKUP_PATH)
    
    # Prepare data structure
    data = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "articles": articles
    }
    
    # Write to temporary file first
    temp_path = STORAGE_PATH + '.tmp'
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        shutil.move(temp_path, STORAGE_PATH)
        print(f"✅ Saved {len(articles)} articles")
        return True
        
    except Exception as e:
        print(f"❌ Save error: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False


def update_saved_status(article_id: str, saved: bool) -> bool:
    """Update the saved status of a specific article."""
    data = load_articles()
    
    for article in data['articles']:
        if article['id'] == article_id:
            article['saved'] = saved
            return save_articles(data['articles'])
    
    print(f"⚠️  Article not found: {article_id}")
    return False


def merge_articles(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """
    Merge new articles with existing ones.
    Preserves 'saved' status from existing articles.
    """
    # Create lookup by ID
    existing_map = {article['id']: article for article in existing}
    
    merged = []
    seen_ids = set()
    
    # Add new articles (preserving saved status if they exist)
    for article in new:
        article_id = article['id']
        if article_id in existing_map:
            # Preserve saved status
            article['saved'] = existing_map[article_id]['saved']
        
        if article_id not in seen_ids:
            merged.append(article)
            seen_ids.add(article_id)
    
    # Add existing saved articles that aren't in new batch
    for article in existing:
        if article['saved'] and article['id'] not in seen_ids:
            merged.append(article)
            seen_ids.add(article['id'])
    
    return merged


if __name__ == "__main__":
    # Test the storage manager
    print("Testing Storage Manager...")
    
    # Test load
    data = load_articles()
    print(f"Loaded {len(data['articles'])} articles")
    
    # Test save
    test_article = {
        "id": generate_article_id("https://test.com/article"),
        "title": "Test Article",
        "source": "Test Source",
        "url": "https://test.com/article",
        "summary": "This is a test",
        "published_at": datetime.utcnow().isoformat() + "Z",
        "category": "Test",
        "saved": False,
        "metadata": {}
    }
    
    save_articles([test_article])
    print("✅ Storage manager test complete")
