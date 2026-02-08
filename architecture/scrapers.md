# Scrapers Architecture SOP

## Purpose
Extract article data from Ben's Bites, The AI Rundown, and Reddit, conforming to the Article Schema.

## Goals
- Fetch latest articles from each source
- Parse HTML/JSON to extract structured data
- Handle layout changes gracefully
- Return standardized Article objects

## Input
- Source URLs (archive pages or API endpoints)

## Logic

### Ben's Bites Scraper
1. Fetch `https://bensbites.com/archive`
2. Parse HTML with BeautifulSoup
3. Find all links matching `/p/` pattern
4. For each link:
   - Extract title from link text
   - Extract URL (make absolute if relative)
   - Fetch individual article page to get published date and summary
   - Generate ID from URL hash
5. Return list of Article objects

### The AI Rundown Scraper
1. Fetch `https://therundown.ai/archive` with User-Agent header
2. Parse HTML with BeautifulSoup
3. Find all links matching `/p/` pattern
4. For each link:
   - Extract title from link text
   - Extract URL
   - Fetch individual article page to get metadata
   - Generate ID from URL hash
5. Return list of Article objects

### Reddit Scraper
1. For each subreddit (`r/artificial`, `r/MachineLearning`, `r/Singularity`):
   - Fetch `https://reddit.com/r/{subreddit}/top.json?t=day&limit=10`
   - Parse JSON response
   - Extract: title, URL, upvotes, author, timestamp
   - Generate ID from URL hash
2. Return combined list of Article objects

## Edge Cases
- **Layout Changes**: If selectors fail, log error and return empty list (don't crash)
- **Network Errors**: Retry once with 5-second delay, then fail gracefully
- **Missing Metadata**: Use defaults (e.g., "Unknown" for author)
- **Rate Limiting**: Add 1-second delay between individual article fetches

## Retry Strategy
- Timeout: 10 seconds per request
- Retries: 1 retry with 5-second backoff
- User-Agent: Always use for The AI Rundown and Reddit

## Known Selectors
- **Ben's Bites**: `<a href="/p/...">` for article links
- **The AI Rundown**: `<a href="/p/...">` for article links
- **Reddit**: JSON API with `data.children[].data` structure
