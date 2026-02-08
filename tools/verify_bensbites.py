#!/usr/bin/env python3
"""
Handshake Tool: Verify Ben's Bites Archive Accessibility
Tests if we can fetch and parse the archive page.
"""

import requests
from bs4 import BeautifulSoup
import sys

def verify_bensbites():
    """Verify Ben's Bites archive is accessible."""
    url = "https://bensbites.com/archive"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Look for article links (they use /p/ pattern)
        article_links = soup.find_all('a', href=lambda x: x and '/p/' in x)
        
        if article_links:
            print(f"✅ SUCCESS: Found {len(article_links)} article links")
            print(f"Sample: {article_links[0].get('href')}")
            return True
        else:
            print("⚠️  WARNING: No article links found")
            return False
            
    except requests.RequestException as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = verify_bensbites()
    sys.exit(0 if success else 1)
