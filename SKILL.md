# 🚀 DROPSHIP PRO — AI Agent Skill Kit
## Amazon + AliExpress → eBay Automation Platform
### Build by: Nguyễn Lê Huy | Version 1.0 | 2026

---

## 🎯 MISSION STATEMENT

You are an expert full-stack AI Agent building **DropShip Pro** — a SaaS web application that clones and improves upon Yaballe (app.yaballe.com). Your job is to autonomously research, code, debug, and deploy every feature of this platform.

**Core value proposition:** Automate 100% of Amazon→eBay and AliExpress→eBay dropshipping operations — listing, repricing, inventory monitoring, order fulfillment — in both API and Non-API modes.

---

## 🏗️ PROJECT ARCHITECTURE

### Tech Stack
```
Frontend:  Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
Backend:   FastAPI (Python) — primary | Node.js Express — secondary
Database:  PostgreSQL (Supabase)
Queue:     BullMQ + Redis (Upstash)
Auth:      NextAuth.js + JWT
Deploy:    Vercel (frontend) + Railway (backend)
AI:        Claude API (claude-haiku-4-5-20251001 for bulk, claude-sonnet-4-6 for analysis)
```

### Repository Structure
```
dropship-pro/
├── frontend/                  # Next.js app
│   ├── app/
│   │   ├── (auth)/           # login, register
│   │   ├── dashboard/        # main dashboard
│   │   ├── listings/         # listing management
│   │   ├── monitor/          # inventory monitor
│   │   ├── orders/           # order management
│   │   └── settings/         # account settings
│   ├── components/
│   └── lib/
├── backend/                   # FastAPI
│   ├── api/
│   │   ├── amazon/           # Amazon scraper + PA API
│   │   ├── aliexpress/       # AliExpress scraper
│   │   ├── ebay/             # eBay API + MIP bot
│   │   ├── monitor/          # Inventory monitor jobs
│   │   ├── orders/           # Auto-order engine
│   │   └── ai/               # Claude AI integration
│   ├── models/               # SQLAlchemy models
│   ├── jobs/                 # BullMQ job definitions
│   └── utils/
├── mip-bot/                   # Non-API browser bot
│   ├── playwright/
│   └── stealth/
└── shared/                    # Types, constants
```

---

## 📦 ALL FEATURES TO BUILD (Priority Order)

### PHASE 1 — Core Infrastructure (Week 1-2)
- [ ] User auth (register, login, JWT, refresh token)
- [ ] eBay OAuth 2.0 connection (API mode)
- [ ] eBay Non-API (MIP) connection via Playwright
- [ ] Dashboard skeleton with sidebar navigation
- [ ] Database schema (see DATABASE section)
- [ ] Multi-account support (multiple eBay accounts per user)

### PHASE 2 — Listing Engine (Week 3-4)
- [ ] Single ASIN lister: Amazon ASIN → eBay listing (1 click)
- [ ] AliExpress URL → eBay listing (1 click)
- [ ] AI title rewriter (Claude API)
- [ ] AI description generator
- [ ] Image fetcher + collage maker
- [ ] VeRO scanner (check banned brands/ASINs before listing)
- [ ] Price calculator (cost + markup + eBay fee = sell price)
- [ ] Category mapper (Amazon/AliExpress category → eBay category)
- [ ] Bulk CSV lister (upload CSV of ASINs/URLs → batch list)
- [ ] Listing templates (save/reuse listing configurations)

### PHASE 3 — Inventory Monitor (Week 5-6) ⭐ CRITICAL
- [ ] Stock checker job: check Amazon/AliExpress stock every 15-30 min
- [ ] Auto set quantity=0 on eBay when source is out of stock
- [ ] Auto restore quantity=1 when back in stock
- [ ] Price change detection → trigger repricer
- [ ] Monitor dashboard (status, last checked, history)
- [ ] Email/Telegram alerts for stock events
- [ ] Monitor 10,000+ ASINs efficiently (batch processing)

### PHASE 4 — Auto-Repricer (Week 7)
- [ ] Price rules engine (min margin, max markup, floor price)
- [ ] Amazon price change → auto update eBay price
- [ ] AliExpress price change → auto update eBay price
- [ ] Competitor repricer (watch eBay competitor prices)
- [ ] Repricing history log

### PHASE 5 — Auto-Order (Week 8-9) ⭐ COMPLEX
- [ ] eBay order webhook/polling (detect new sales)
- [ ] Amazon auto-order via Zinc API
- [ ] AliExpress auto-order via Playwright bot
- [ ] Buyer address routing (eBay buyer → Amazon/AliExpress ship-to)
- [ ] Gift mode (no price invoice)
- [ ] Tracking number extraction from Amazon confirmation email
- [ ] Auto-update tracking on eBay order
- [ ] Order status dashboard

### PHASE 6 — Analytics & Polish (Week 10-11)
- [ ] Sales dashboard (revenue, profit, orders over time)
- [ ] STR (Sell-Through Rate) per listing
- [ ] PPL (Profit Per Listing) analytics
- [ ] Top performing products report
- [ ] Account health monitor (eBay metrics)

### PHASE 7 — SaaS & Monetization (Week 12)
- [ ] Stripe subscription billing (4 pricing tiers)
- [ ] Usage limits enforcement per plan
- [ ] Admin panel
- [ ] Onboarding wizard

---

## 🗄️ DATABASE SCHEMA

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR NOT NULL,
  plan VARCHAR DEFAULT 'starter', -- starter|pro|scale|enterprise
  stripe_customer_id VARCHAR,
  stripe_subscription_id VARCHAR,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- eBay Accounts
CREATE TABLE ebay_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  username VARCHAR NOT NULL,
  mode VARCHAR NOT NULL, -- 'api' | 'mip'
  -- API mode
  oauth_token TEXT,
  oauth_refresh TEXT,
  token_expires_at TIMESTAMPTZ,
  -- MIP mode
  mip_session TEXT, -- encrypted browser session/cookies
  -- Meta
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Listings (products being monitored)
CREATE TABLE listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  ebay_account_id UUID REFERENCES ebay_accounts(id),
  -- Source
  source VARCHAR NOT NULL, -- 'amazon' | 'aliexpress'
  source_id VARCHAR NOT NULL, -- ASIN or AliExpress item ID
  source_url TEXT,
  -- eBay listing
  ebay_item_id VARCHAR,
  ebay_title TEXT,
  -- Pricing
  source_price DECIMAL(10,2),
  ebay_price DECIMAL(10,2),
  markup_percent DECIMAL(5,2),
  -- Status
  status VARCHAR DEFAULT 'active', -- active|out_of_stock|delisted|error
  quantity INTEGER DEFAULT 1,
  -- Monitor
  last_checked_at TIMESTAMPTZ,
  check_interval_minutes INTEGER DEFAULT 30,
  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Price History
CREATE TABLE price_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id),
  old_source_price DECIMAL(10,2),
  new_source_price DECIMAL(10,2),
  old_ebay_price DECIMAL(10,2),
  new_ebay_price DECIMAL(10,2),
  reason VARCHAR, -- 'source_price_change'|'manual'|'repricer'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Stock History
CREATE TABLE stock_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id),
  in_stock BOOLEAN NOT NULL,
  action_taken VARCHAR, -- 'set_zero'|'restored'|'none'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Orders
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  listing_id UUID REFERENCES listings(id),
  -- eBay order
  ebay_order_id VARCHAR UNIQUE NOT NULL,
  ebay_sale_price DECIMAL(10,2),
  -- Buyer
  buyer_name VARCHAR,
  buyer_address TEXT, -- JSON
  -- Source order
  source VARCHAR, -- 'amazon'|'aliexpress'
  source_order_id VARCHAR,
  source_cost DECIMAL(10,2),
  -- Tracking
  tracking_number VARCHAR,
  tracking_carrier VARCHAR,
  -- Profit
  profit DECIMAL(10,2),
  -- Status
  status VARCHAR DEFAULT 'pending', -- pending|ordered|shipped|delivered|error
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- VeRO Database (banned brands/ASINs)
CREATE TABLE vero_list (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand VARCHAR,
  asin VARCHAR,
  reason TEXT,
  added_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🔌 EXTERNAL APIs & CREDENTIALS

### Required Environment Variables
```env
# Supabase
DATABASE_URL=postgresql://...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=...

# Redis (Upstash)
REDIS_URL=redis://...
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...

# eBay API
EBAY_APP_ID=...          # Client ID
EBAY_CERT_ID=...         # Client Secret
EBAY_DEV_ID=...
EBAY_REDIRECT_URI=...    # OAuth callback
EBAY_SANDBOX=false       # true for testing

# Amazon
RAINFOREST_API_KEY=...   # rainforestapi.com — $15/mo, best option
# OR
AMAZON_PA_ACCESS_KEY=... # PA API (requires Associates account)
AMAZON_PA_SECRET_KEY=...
AMAZON_PA_PARTNER_TAG=...

# AliExpress
ALIEXPRESS_APP_KEY=...   # AliExpress Open Platform
ALIEXPRESS_APP_SECRET=...

# Zinc (Amazon auto-order)
ZINC_API_KEY=...         # zinc.io — $0.05/order

# AI
ANTHROPIC_API_KEY=...

# Auth
NEXTAUTH_SECRET=...
NEXTAUTH_URL=https://app.dropshippro.com

# Stripe
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
STRIPE_PRICE_STARTER=price_...
STRIPE_PRICE_PRO=price_...
STRIPE_PRICE_SCALE=price_...
```

### API Reference Quick Guide

#### eBay REST API (API Mode)
```
Base URL: https://api.ebay.com
Auth: OAuth 2.0 Bearer token
Key endpoints:
- POST /sell/inventory/v1/inventory_item/{sku}  → create/update listing
- POST /sell/inventory/v1/offer                → create offer (listing on eBay)
- PUT  /sell/inventory/v1/offer/{offerId}/publish → publish listing
- GET  /sell/fulfillment/v1/order              → get orders
- POST /sell/fulfillment/v1/order/{orderId}/shipping_fulfillment → add tracking
- POST /sell/inventory/v1/inventory_item/{sku} → update quantity/price
```

#### eBay Finding API (Search — no OAuth needed)
```
URL: https://svcs.ebay.com/services/search/FindingService/v1
Auth: SECURITY-APPNAME query param (App ID)
Key operation: findItemsByKeywords
```

#### Amazon via Rainforest API
```
Base URL: https://api.rainforestapi.com/request
Key params:
- api_key, type=product, asin=XXXXX
- Returns: title, price, rating, reviews, bsr, images, stock_status, buybox_winner
```

#### AliExpress Open Platform
```
Base URL: https://api.taobao.com/router/rest
Key methods:
- aliexpress.ds.product.get → product detail by item ID
- aliexpress.solution.product.list.get → search products
Auth: HMAC-MD5 signed requests
```

#### Zinc API (Amazon auto-order)
```
POST https://api.zinc.io/v1/orders
Auth: Basic {ZINC_API_KEY}:
Body: { retailer: "amazon", products: [{product_id, quantity}], shipping_address: {...}, gift_message: "..." }
```

---

## 🤖 AI AGENT BEHAVIORS & SKILLS

### Skill 1: Amazon Data Extraction
When given an ASIN, extract real product data using this priority:
1. **Rainforest API** (if key available) → 100% accurate
2. **Playwright scrape** amazon.com/dp/{ASIN} → parse HTML
3. **Claude estimate** → fallback only, label as "AI ESTIMATE ⚠️"

Key fields to extract:
- title, brand, category, amazonPrice, rating, reviewCount
- bsr (Best Sellers Rank), monthlySales ("X bought in past month")
- imageUrl (high-res), isPrime, isHazmat, weight, dimensions
- stockStatus: "In Stock" / "Out of Stock" / "Usually ships in X days"

Stock check optimization (for monitor jobs):
```python
# Fast stock check — only fetch essential data, not full page
url = f"https://www.amazon.com/dp/{asin}"
# Parse only: "In Stock", "Out of Stock", "Currently unavailable"
# Use lightweight headers, skip images
```

### Skill 2: AliExpress Data Extraction
When given an AliExpress URL or Item ID:
1. **AliExpress Open Platform API** (if credentials available)
2. **Playwright scrape** — navigate to item page, extract JSON from `window.__INIT_DATA__`
3. Parse: title, price (USD after conversion), images, shipping time, seller rating, stock quantity

### Skill 3: eBay Listing Creation (API Mode)
```python
# Full flow to create an eBay listing via REST API:
# Step 1: Create/Update Inventory Item
PUT /sell/inventory/v1/inventory_item/{sku}
{
  "availability": {"shipToLocationAvailability": {"quantity": 1}},
  "condition": "NEW",
  "product": {
    "title": "{rewritten_title}",
    "description": "{html_description}",
    "imageUrls": ["{image_url}"],
    "aspects": {}  # category-specific attributes
  }
}

# Step 2: Create Offer
POST /sell/inventory/v1/offer
{
  "sku": "{sku}",
  "marketplaceId": "EBAY_US",
  "format": "FIXED_PRICE",
  "pricingSummary": {"price": {"value": "{price}", "currency": "USD"}},
  "listingDescription": "{description}",
  "categoryId": "{ebay_category_id}",
  "merchantLocationKey": "default"
}

# Step 3: Publish
POST /sell/inventory/v1/offer/{offerId}/publish
```

### Skill 4: eBay MIP (Non-API) Mode
MIP = **M**anual **I**nventory **P**rocess — uses Playwright to control browser like a human.

```python
# MIP Bot architecture
from playwright.async_api import async_playwright

async def mip_list_item(session_cookies, item_data):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        # Restore saved session
        await context.add_cookies(session_cookies)
        page = await context.new_page()
        # Navigate to eBay sell form
        await page.goto("https://www.ebay.com/sl/add")
        # Fill form fields...
```

**IMPORTANT:** Always use `playwright-stealth` or equivalent to avoid bot detection.

### Skill 5: Inventory Monitor Job
```python
# BullMQ job — runs every 30 minutes per user
async def check_inventory_batch(user_id: str, batch_size: int = 50):
    listings = await get_active_listings(user_id, limit=batch_size)
    
    # Parallel check all listings
    tasks = [check_single_listing(listing) for listing in listings]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for listing, result in zip(listings, results):
        if isinstance(result, Exception):
            await log_error(listing.id, str(result))
            continue
            
        was_in_stock = listing.status == 'active'
        is_in_stock = result['in_stock']
        price_changed = result['price'] != listing.source_price
        
        if was_in_stock and not is_in_stock:
            # Out of stock → set eBay quantity to 0
            await update_ebay_quantity(listing, quantity=0)
            await update_listing_status(listing.id, 'out_of_stock')
            await log_stock_event(listing.id, in_stock=False, action='set_zero')
            await send_alert(listing.user_id, f"OUT OF STOCK: {listing.ebay_title}")
            
        elif not was_in_stock and is_in_stock:
            # Back in stock → restore quantity
            await update_ebay_quantity(listing, quantity=1)
            await update_ebay_price(listing, result['price'])
            await update_listing_status(listing.id, 'active')
            await log_stock_event(listing.id, in_stock=True, action='restored')
            
        elif price_changed:
            # Price changed → repricer handles it
            await trigger_repricer(listing.id, new_source_price=result['price'])
```

### Skill 6: AI Title Rewriter
```python
async def rewrite_title_for_ebay(amazon_title: str, category: str = "") -> str:
    prompt = f"""Rewrite this Amazon product title for eBay listing optimization.

Original Amazon title: {amazon_title}
Category: {category}

Rules:
1. Maximum 80 characters (STRICT — count carefully)
2. Start with the most important searchable keyword first
3. REMOVE: brand name, "Amazon", "Prime", registered trademarks (™ ®)
4. REMOVE: special characters: | / \\ # @ & * ( )
5. INCLUDE: main product type + key feature + size/color/quantity if relevant
6. Make it sound natural and searchable
7. Do NOT start with articles (the, a, an)

Output: ONLY the rewritten title, nothing else. No explanation."""

    response = await claude_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()[:80]
```

### Skill 7: Profit Calculator
```python
def calculate_profit(source_price: float, markup_percent: float = 30) -> dict:
    """
    eBay fee structure:
    - Final value fee: 13.25% of sale price (most categories)
    - Payment processing: 2.9% + $0.30
    - Optional: Promoted listings ~2-5% (skip for now)
    """
    sell_price = source_price * (1 + markup_percent / 100)
    ebay_final_value_fee = sell_price * 0.1325
    payment_fee = sell_price * 0.029 + 0.30
    total_fees = ebay_final_value_fee + payment_fee
    profit = sell_price - source_price - total_fees
    margin = (profit / sell_price) * 100 if sell_price > 0 else 0
    roi = (profit / source_price) * 100 if source_price > 0 else 0
    
    return {
        "source_price": round(source_price, 2),
        "sell_price": round(sell_price, 2),
        "ebay_fee": round(ebay_final_value_fee, 2),
        "payment_fee": round(payment_fee, 2),
        "profit": round(profit, 2),
        "margin_percent": round(margin, 1),
        "roi_percent": round(roi, 1)
    }

# Minimum viable margin for dropshipping: 10%
# Target margin: 15-25%
```

### Skill 8: Auto-Order (Amazon via Zinc)
```python
async def place_amazon_order(
    asin: str,
    buyer_address: dict,
    zinc_api_key: str
) -> dict:
    """Place Amazon order to ship directly to eBay buyer"""
    
    order_payload = {
        "retailer": "amazon",
        "products": [{"product_id": asin, "quantity": 1}],
        "shipping_address": {
            "first_name": buyer_address["first_name"],
            "last_name": buyer_address["last_name"],
            "address_line1": buyer_address["street"],
            "city": buyer_address["city"],
            "state": buyer_address["state"],
            "zip_code": buyer_address["zip"],
            "country": "US",
            "phone_number": buyer_address.get("phone", "5555555555")
        },
        "billing_address": {...},  # Use your own billing
        "payment_method": {...},   # Your virtual card
        "shipping_method": "cheapest",
        "gift_message": "Thank you for your purchase!",
        "is_gift": True,           # No price invoice
        "max_price": 999           # Safety limit in cents
    }
    
    response = await httpx.post(
        "https://api.zinc.io/v1/orders",
        auth=(zinc_api_key, ""),
        json=order_payload
    )
    return response.json()
```

### Skill 9: VeRO Scanner
```python
VERO_BRANDS = [
    "Nike", "Adidas", "Apple", "Samsung", "Sony", "Louis Vuitton",
    "Gucci", "Chanel", "Rolex", "Disney", "Marvel", "Nintendo",
    "Lego", "Pokemon", "Harry Potter", # ... expand this list
]

VERO_KEYWORDS = [
    "replica", "counterfeit", "fake", "knockoff", "inspired by",
    "looks like", "similar to brand"
]

async def scan_vero(title: str, asin: str, brand: str) -> dict:
    """Check if product violates eBay VeRO policy"""
    risks = []
    
    # Check brand
    for vero_brand in VERO_BRANDS:
        if vero_brand.lower() in title.lower() or vero_brand.lower() == brand.lower():
            risks.append(f"Brand '{vero_brand}' is VeRO protected")
    
    # Check ASIN in custom VeRO database
    db_result = await db.fetch_one(
        "SELECT reason FROM vero_list WHERE asin = :asin OR brand = :brand",
        {"asin": asin, "brand": brand}
    )
    if db_result:
        risks.append(f"Database flag: {db_result['reason']}")
    
    return {
        "is_safe": len(risks) == 0,
        "risks": risks,
        "recommendation": "SKIP" if risks else "OK"
    }
```

### Skill 10: Debug & Self-Fix Protocol
When encountering errors, follow this systematic approach:

```
STEP 1: Parse the error
- What type? (ImportError, HTTP 4xx/5xx, TimeoutError, ParseError, etc.)
- Which module? (amazon scraper, ebay api, monitor job, etc.)
- Is it intermittent or consistent?

STEP 2: Identify root cause category
A) API error → check credentials, rate limits, endpoint URL
B) Scraper blocked → rotate User-Agent, add delay, use proxy
C) Parse error → Amazon/eBay changed HTML structure
D) Logic error → trace the data flow, check edge cases
E) Dependency error → check imports, versions, env vars

STEP 3: Apply fix
- Never break working code to fix one thing
- Apply minimal change
- Add error handling for the specific case

STEP 4: Verify
- Test the specific failing case
- Test adjacent functionality
- Check logs for related errors

STEP 5: Document
- Add comment explaining why fix was needed
- Update error handling to be more informative
```

---

## 📋 CODING STANDARDS

### Python Backend
```python
# Always use async/await for I/O
# Type hints required
# Error handling: specific exceptions, not bare except
# Logging: use structlog for structured logs

from typing import Optional, List, Dict, Any
import structlog

logger = structlog.get_logger()

async def example_function(asin: str) -> Optional[Dict[str, Any]]:
    try:
        result = await fetch_data(asin)
        logger.info("data_fetched", asin=asin, status="ok")
        return result
    except httpx.TimeoutException:
        logger.error("fetch_timeout", asin=asin)
        return None
    except httpx.HTTPStatusError as e:
        logger.error("http_error", asin=asin, status_code=e.response.status_code)
        raise
```

### TypeScript Frontend
```typescript
// Use Server Components where possible (Next.js 14)
// Client Components only when needed (useState, useEffect, browser APIs)
// All API calls through /lib/api.ts
// Loading states and error states always handled
// Mobile-first responsive design
```

### API Response Format
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "meta": {
    "timestamp": "2026-03-11T14:00:00Z",
    "source": "amazon_scrape"
  }
}
```

---

## ⚡ PERFORMANCE TARGETS

| Operation | Target | Method |
|-----------|--------|--------|
| Single listing creation | < 10 seconds | Parallel: scrape + AI simultaneously |
| Bulk 1000 listings | < 30 minutes | BullMQ workers, 10 concurrent |
| Stock check per ASIN | < 3 seconds | Lightweight HTML parse |
| Monitor 10K listings | < 60 min/cycle | 100 concurrent workers |
| eBay API call | < 2 seconds | Connection pooling |
| Page load | < 2 seconds | Next.js SSR + CDN |

---

## 🚨 CRITICAL RULES (Never Break These)

1. **Never store raw passwords** — always bcrypt hash
2. **Never log API keys or tokens** in any log file
3. **Never expose .env values** to frontend
4. **Always rate limit** Amazon requests: max 1 request/second per IP
5. **Always add delays** between eBay MIP bot actions: 1-3 seconds random
6. **Always check VeRO** before listing any product
7. **Always validate** eBay buyer address before placing Amazon order
8. **Never hardcode** credentials, always use environment variables
9. **Always handle** eBay API rate limits (429 → exponential backoff)
10. **Always encrypt** stored session cookies/tokens at rest

---

## 💰 PRICING & PLAN LIMITS

```python
PLAN_LIMITS = {
    "starter": {
        "max_listings": 200,
        "max_ebay_accounts": 1,
        "monitor_interval_minutes": 60,
        "bulk_upload_limit": 100,
        "auto_order": False,
        "mip_mode": False,
        "price_usd": 19
    },
    "pro": {
        "max_listings": 1000,
        "max_ebay_accounts": 3,
        "monitor_interval_minutes": 30,
        "bulk_upload_limit": 500,
        "auto_order": True,
        "mip_mode": False,
        "price_usd": 49
    },
    "scale": {
        "max_listings": 5000,
        "max_ebay_accounts": 10,
        "monitor_interval_minutes": 15,
        "bulk_upload_limit": 2000,
        "auto_order": True,
        "mip_mode": True,
        "price_usd": 99
    },
    "enterprise": {
        "max_listings": -1,  # unlimited
        "max_ebay_accounts": -1,
        "monitor_interval_minutes": 10,
        "bulk_upload_limit": -1,
        "auto_order": True,
        "mip_mode": True,
        "price_usd": 199
    }
}
```

---

## 🔄 DEVELOPMENT WORKFLOW

When working on a new feature:
1. **Read** the feature spec from this SKILL.md
2. **Check** existing code for related patterns to reuse
3. **Plan** the implementation (list files to create/modify)
4. **Code** the backend API endpoint first, then frontend
5. **Test** with real ASINs and eBay sandbox credentials
6. **Fix** any errors using the Debug Protocol (Skill 10)
7. **Deploy** to Vercel/Railway
8. **Verify** deployment works end-to-end

When asked to "continue building", always:
- Check git status for what's been done
- Read relevant existing files before writing new ones
- Never duplicate code — check utils/ and shared/ first
- Update this SKILL.md if you discover new patterns

---

## 📞 OWNER CONTEXT

**Owner:** Nguyễn Lê Huy (lehuykt10@gmail.com)
**Business:** eBay Dropshipping seller since 2014, Amazon→eBay specialist
**Goal:** Build and monetize DropShip Pro as SaaS product for Vietnamese + global dropshippers
**Current tools:** Yaballe subscription (knows the product deeply as a user)
**Tech level:** Business/marketing focused — relies on AI for all technical implementation
**Language preference:** Vietnamese for explanations, English for code comments
**Deployed infra:**
- Vercel team: "Le Huy's projects" (team_Xb6CZw32iKf8TyhgBwKKs4lo)
- Existing Vercel projects: dropspy, project-exi18, ebay-mastery-vn
**API Keys available:** Anthropic API key, eBay Sandbox App ID

**Communication style:**
- Explain decisions in Vietnamese
- Show code directly without asking permission
- Proactively fix issues without waiting to be asked
- When stuck, list what's needed (credentials, decisions) clearly

---

*Last updated: March 2026 | DropShip Pro AI Agent Kit v1.0*
