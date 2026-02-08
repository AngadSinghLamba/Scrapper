#!/usr/bin/env python3
"""
Handshake Tool: Verify Reddit JSON Endpoint Accessibility
Tests if we can fetch top posts from AI subreddits.
"""

import requests
import sys

def verify_reddit():
    """Verify Reddit JSON endpoint is accessible."""
    subreddits = ['artificial', 'MachineLearning', 'Singularity']
    
    for subreddit in subreddits:
        url = f"https://reddit.com/r/{subreddit}/top.json?t=day&limit=5"
        
        try:
            headers = {'User-Agent': 'AI-News-Dashboard/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            if posts:
                print(f"✅ SUCCESS: r/{subreddit} - Found {len(posts)} posts")
            else:
                print(f"⚠️  WARNING: r/{subreddit} - No posts found")
                
        except requests.RequestException as e:
            print(f"❌ ERROR: r/{subreddit} - {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = verify_reddit()
    sys.exit(0 if success else 1)
