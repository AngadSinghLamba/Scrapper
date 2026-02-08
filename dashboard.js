// Dashboard JavaScript - Handles article rendering, filtering, and save functionality

let allArticles = [];
let currentFilter = 'all';
const AUTO_REFRESH_INTERVAL = 60000; // 60 seconds

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    setupFilters();
    loadArticles();

    // Auto-refresh every 60 seconds
    setInterval(() => {
        loadArticles(true); // Silent refresh
    }, AUTO_REFRESH_INTERVAL);
});

// Setup filter buttons
function setupFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update current filter
            currentFilter = btn.dataset.filter;

            // Re-render articles
            renderArticles();
        });
    });
}

// Load articles from API
async function loadArticles(silent = false) {
    if (!silent) {
        showLoading();
    }

    try {
        const response = await fetch('/api/articles');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        allArticles = data.articles || [];

        // Update stats
        updateStats(data.last_updated);

        // Render articles
        renderArticles();

        if (silent) {
            showNotification('Dashboard refreshed');
        }

    } catch (error) {
        console.error('Error loading articles:', error);
        showError(error.message);
    }
}

// Render articles based on current filter
function renderArticles() {
    const grid = document.getElementById('articles-grid');
    const loading = document.getElementById('loading');
    const emptyState = document.getElementById('empty-state');
    const errorState = document.getElementById('error-state');

    // Hide all states
    loading.style.display = 'none';
    emptyState.style.display = 'none';
    errorState.style.display = 'none';

    // Filter articles
    let filtered = filterArticles(allArticles, currentFilter);

    // Sort by published date (newest first)
    filtered.sort((a, b) => {
        return new Date(b.published_at) - new Date(a.published_at);
    });

    // Show empty state if no articles
    if (filtered.length === 0) {
        grid.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    // Render article cards
    grid.innerHTML = filtered.map(article => createArticleCard(article)).join('');

    // Attach save button listeners
    attachSaveListeners();
}

// Filter articles based on filter type
function filterArticles(articles, filter) {
    if (filter === 'all') {
        return articles;
    }

    if (filter === 'saved') {
        return articles.filter(a => a.saved);
    }

    // Filter by source
    return articles.filter(a => a.source === filter);
}

// Create article card HTML
function createArticleCard(article) {
    const sourceClass = article.source.toLowerCase().replace(/[^a-z]/g, '');
    const savedClass = article.saved ? 'saved' : '';
    const savedIcon = article.saved ? '❤️' : '🤍';

    const timeAgo = getTimeAgo(article.published_at);

    return `
        <div class="article-card" data-id="${article.id}">
            <div class="article-header">
                <span class="source-badge ${sourceClass}">${article.source}</span>
                <button class="save-btn ${savedClass}" data-id="${article.id}">
                    ${savedIcon}
                </button>
            </div>
            
            <h3 class="article-title">${escapeHtml(article.title)}</h3>
            
            ${article.summary ? `<p class="article-summary">${escapeHtml(article.summary)}</p>` : ''}
            
            <div class="article-footer">
                <span class="article-meta">${timeAgo}</span>
                <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="read-more">
                    Read More →
                </a>
            </div>
        </div>
    `;
}

// Attach save button listeners
function attachSaveListeners() {
    const saveButtons = document.querySelectorAll('.save-btn');

    saveButtons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const articleId = btn.dataset.id;
            await toggleSave(articleId);
        });
    });
}

// Toggle save status
async function toggleSave(articleId) {
    try {
        const article = allArticles.find(a => a.id === articleId);
        if (!article) return;

        const newSavedStatus = !article.saved;

        const response = await fetch(`/api/articles/${articleId}/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ saved: newSavedStatus })
        });

        if (!response.ok) {
            if (response.status === 405 || response.status === 404) {
                throw new Error('Save functionality is not available in the static preview. Use the local server for full features.');
            }
            throw new Error('Failed to update save status');
        }

        // Update local state
        article.saved = newSavedStatus;

        // Update stats
        updateStats();

        // Re-render to update UI
        renderArticles();

        showNotification(newSavedStatus ? 'Article saved!' : 'Article unsaved');

    } catch (error) {
        console.error('Error toggling save:', error);
        showNotification('Failed to save article', true);
    }
}

// Update stats bar
function updateStats(lastUpdated = null) {
    const totalCount = allArticles.length;
    const savedCount = allArticles.filter(a => a.saved).length;

    document.getElementById('total-count').textContent = totalCount;
    document.getElementById('saved-count').textContent = savedCount;

    if (lastUpdated) {
        document.getElementById('last-updated').textContent = getTimeAgo(lastUpdated);
    }
}

// Show loading state
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('articles-grid').innerHTML = '';
    document.getElementById('empty-state').style.display = 'none';
    document.getElementById('error-state').style.display = 'none';
}

// Show error state
function showError(message) {
    document.getElementById('error-state').style.display = 'block';
    document.getElementById('error-message').textContent = message;
    document.getElementById('loading').style.display = 'none';
    document.getElementById('articles-grid').innerHTML = '';
    document.getElementById('empty-state').style.display = 'none';
}

// Show notification
function showNotification(text, isError = false) {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notification-text');

    notificationText.textContent = text;
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Get relative time (e.g., "2 hours ago")
function getTimeAgo(timestamp) {
    const now = new Date();
    const past = new Date(timestamp);
    const diffMs = now - past;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return past.toLocaleDateString();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
