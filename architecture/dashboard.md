# Dashboard Architecture SOP

## Purpose
Provide a beautiful, interactive web interface for viewing and managing AI news articles.

## Goals
- Display articles in a visually stunning card-based layout
- Enable filtering by source and saved status
- Implement "Save" functionality with persistence
- Auto-refresh every 60 seconds
- Achieve "Gorgeous" aesthetic with glassmorphism

## Input
- `articles.json` from storage (via API endpoint)

## Logic

### Rendering
1. Fetch articles from `/api/articles`
2. Apply active filters (All, Saved, by Source)
3. Sort by published date (newest first)
4. Render article cards with:
   - Title
   - Source badge
   - Summary
   - Published time (relative, e.g., "2 hours ago")
   - Save button (heart icon)
   - External link button

### Save Functionality
1. User clicks heart icon
2. Send POST to `/api/articles/:id/save`
3. Update local state
4. Re-render card with updated saved status

### Filters
- **All**: Show all articles from last 24h + saved
- **Saved**: Show only saved articles
- **By Source**: Show only articles from specific source

### Auto-Refresh
- Every 60 seconds, re-fetch articles
- Preserve scroll position
- Show subtle notification if new articles available

## UI/UX Requirements
- **Glassmorphism**: Frosted glass effect on cards
- **Gradients**: Vibrant background gradients
- **Animations**: Smooth transitions on hover, save button pulse
- **Typography**: Modern font (Inter or Outfit from Google Fonts)
- **Responsive**: Grid layout that adapts to screen size
- **Dark Mode**: Optimized for dark backgrounds

## Edge Cases
- **No Articles**: Show empty state with illustration
- **API Error**: Show error message but don't crash
- **Slow Network**: Show loading skeleton
