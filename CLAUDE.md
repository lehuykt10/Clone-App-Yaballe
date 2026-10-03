# DropShip Pro — Claude Code Instructions

## FIRST READ THIS
This project builds a Yaballe-clone SaaS for Amazon+AliExpress→eBay dropshipping automation.
Full specs, skills, and patterns are in `SKILL.md`. Read it before doing anything.

## Quick Start Commands

```bash
# Install dependencies
cd frontend && npm install
cd backend && pip install -r requirements.txt

# Run dev
cd frontend && npm run dev          # http://localhost:3000
cd backend && uvicorn main:app --reload  # http://localhost:8000

# Database
supabase db push                    # Apply migrations
supabase db reset                   # Reset to clean state

# Jobs
redis-server &                      # Start Redis
python -m jobs.worker               # Start job worker
```

## Environment Setup
Copy `.env.example` to `.env.local` (frontend) and `.env` (backend).
See SKILL.md → "Required Environment Variables" for all keys needed.

## Current Build Status
Update this section as features are completed:

### ✅ Done
- (nothing yet — starting fresh)

### 🚧 In Progress
- Phase 1: Auth + Dashboard + eBay Connection

### 📋 Todo
- All phases listed in SKILL.md

## Key Files to Know
- `SKILL.md` — Master spec, all skills, database schema, API reference
- `backend/api/amazon/scraper.py` — Amazon data extraction
- `backend/api/ebay/client.py` — eBay API wrapper
- `backend/jobs/monitor.py` — Inventory monitor job
- `frontend/app/dashboard/` — Main dashboard
- `.claude/skills/winning-product-research/` — Skill research sản phẩm winning (viral video, biến thể, case study)

## If You Get Stuck
1. Check SKILL.md for the relevant skill/pattern
2. Read existing similar code in the project
3. For eBay API issues: check https://developer.ebay.com/devzone/rest/api-docs
4. For Amazon scraping issues: check if HTML structure changed, update selectors
5. List what you need (credentials, decisions) clearly in Vietnamese for owner
