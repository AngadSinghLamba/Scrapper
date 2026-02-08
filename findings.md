# Findings

## Research
- Environment: Scratch/Empty project directory detected.
- System: Mac.
- **Ben's Bites**: Archive at `https://bensbites.com/archive`. Uses Substack. Posts under `/p/`.
- **The AI Rundown**: Archive at `https://therundown.ai/archive`. Posts under `/p/`.
- **Reddit**: Targeted subreddits: `r/artificial`, `r/MachineLearning`, `r/Singularity`. Use `.json` endpoints for cleaner data.

## Constraints
- Forbidden from installing new packages unless explicitly requested (for populated environments). Since this is a scratch environment, I will propose a `requirements.txt` in Phase 2.
- Dashboard must be local (no Supabase in Phase 1).

## Discoveries
- Both newsletters use a `/p/slug` structure for individual articles.
- Archives are publicly accessible without login for the last few posts.
- Reddit offers `top` for last 24h via `reddit.com/r/SUBREDDIT/top.json?t=day`.
