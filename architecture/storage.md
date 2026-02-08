# Storage Architecture SOP

## Purpose
Manage all read/write operations for the local JSON database (`/.tmp/articles.json`) that stores article data and saved status.

## Goals
- Provide atomic write operations to prevent data corruption
- Validate data against the Article Schema defined in `gemini.md`
- Enable easy migration to Supabase in Phase 2

## Input
- Article objects conforming to schema
- Article ID and saved status for updates

## Logic

### Load Articles
1. Check if `articles.json` exists
2. If not, return empty structure: `{"last_updated": ISO_timestamp, "articles": []}`
3. If exists, read and parse JSON
4. Return parsed data

### Save Articles
1. Validate each article against schema
2. Create backup of existing file (if exists)
3. Write to temporary file first
4. Atomic rename to `articles.json`
5. Update `last_updated` timestamp

### Update Saved Status
1. Load current articles
2. Find article by ID
3. Toggle `saved` field
4. Save updated articles

## Edge Cases
- **File Corruption**: If JSON parse fails, restore from backup
- **Missing Fields**: Reject articles missing required schema fields
- **Concurrent Writes**: Use file locking (not implemented in Phase 1, single-threaded)

## Migration Path to Supabase
- Replace `load_articles()` with Supabase query
- Replace `save_articles()` with Supabase upsert
- Keep same function signatures for backward compatibility
