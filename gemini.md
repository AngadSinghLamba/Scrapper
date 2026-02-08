# The Constitution (gemini.md)

## The Law
- Protocol: B.L.A.S.T.
- Architecture: A.N.T. (Architecture, Navigation, Tools)

## Data Schemas

### Article Schema
```json
{
  "id": "string (hash of URL or title)",
  "title": "string",
  "source": "string (Ben's Bites | The AI Rundown | Reddit)",
  "url": "string (canonical link)",
  "summary": "string (truncated content or meta description)",
  "published_at": "string (ISO 8601 timestamp)",
  "category": "string (AI | Tools | Research | etc)",
  "saved": "boolean (default: false)",
  "metadata": {
    "author": "string",
    "upvotes": "number (for Reddit)",
    "newsletter_issue": "string"
  }
}
```

### Storage Schema (`.tmp/articles.json`)
```json
{
  "last_updated": "ISO timestamp",
  "articles": [
    "ArticleObject"
  ]
}
```

## Behavioral Rules
- **Aesthetics First**: Dashboard must be "Gorgeous" and "Interactive". Use glassmorphism or high-end modern UI.
- **Recency**: Only display articles from the last 24 hours by default, unless they are marked as `saved: true`.
- **Fault Tolerance**: If one scraper fails due to a layout change, the system must continue to function and log the error to `progress.md` without crashing the dashboard.
- **Persistence**: "Saved" status must be preserved in `articles.json`.

## Invariants
- No `from module import *`.
- Atomic scripts in tools/.

## Maintenance Log
- (Pending Trigger Phase)
