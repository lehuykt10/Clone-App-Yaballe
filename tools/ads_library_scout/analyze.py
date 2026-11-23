"""Group Ad Library ads by advertiser/store, score how "winning" each one looks,
and estimate spend and orders.

All money and order numbers are ESTIMATES built from assumptions (CPM, frequency,
ROAS, AOV, daily budget per ad). Treat them as an order-of-magnitude range for
comparing advertisers, not as real figures.
"""
import csv
import math
import re
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Assumptions:
    cpm_low: float = 6.0          # USD per 1,000 impressions (EU, low)
    cpm_high: float = 12.0        # USD per 1,000 impressions (EU, high)
    frequency: float = 1.4        # impressions per reached person
    daily_per_ad_low: float = 10.0   # fallback when reach is unknown
    daily_per_ad_high: float = 50.0
    roas_low: float = 1.2         # revenue / ad spend
    roas_high: float = 2.5
    aov: float = 40.0             # average order value, USD


@dataclass
class Group:
    key: str
    page_name: str
    domain: str
    ads: list = field(default_factory=list)
    # filled by compute()
    active_ads: int = 0
    total_ads: int = 0
    days_running: int = 0
    new_last_7d: int = 0
    eu_reach: int = 0
    countries: list = field(default_factory=list)
    platforms: list = field(default_factory=list)
    sample_texts: list = field(default_factory=list)
    snapshot_urls: list = field(default_factory=list)
    spend_low: float = 0.0
    spend_high: float = 0.0
    spend_method: str = ""
    daily_spend_low: float = 0.0
    daily_spend_high: float = 0.0
    orders_low: int = 0
    orders_high: int = 0
    score: int = 0


DOMAIN_RE = re.compile(r"^(?:https?://)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)+)(?:/.*)?$")


def parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def domain_of(ad):
    for cap in ad.get("ad_creative_link_captions") or []:
        m = DOMAIN_RE.match(str(cap).strip().lower())
        if m:
            return m.group(1)
    return ""


def _countries(ad):
    out = set()
    for row in ad.get("age_country_gender_reach_breakdown") or []:
        if row.get("country"):
            out.add(row["country"])
    if not out:
        for loc in ad.get("target_locations") or []:
            if not loc.get("excluded") and loc.get("name"):
                out.add(loc["name"])
    return out


def _is_active(ad, today):
    stop = parse_date(ad.get("ad_delivery_stop_time"))
    return stop is None or stop >= today


def group_ads(ads):
    groups = {}
    for ad in ads:
        dom = domain_of(ad)
        page = ad.get("page_name") or "(unknown page)"
        key = dom or f"page:{ad.get('page_id') or page}"
        g = groups.get(key)
        if g is None:
            g = groups[key] = Group(key=key, page_name=page, domain=dom)
        g.ads.append(ad)
    return list(groups.values())


def compute(group, assumptions, today):
    a = assumptions
    ads = group.ads
    active = [ad for ad in ads if _is_active(ad, today)]
    group.total_ads = len(ads)
    group.active_ads = len(active)
    starts = [parse_date(ad.get("ad_delivery_start_time")) for ad in (active or ads)]
    starts = [s for s in starts if s]
    group.days_running = (today - min(starts)).days if starts else 0
    group.new_last_7d = sum(1 for s in starts if (today - s).days <= 7)
    group.eu_reach = sum(int(ad.get("eu_total_reach") or 0) for ad in ads)

    countries, platforms, texts, snaps = set(), set(), [], []
    for ad in ads:
        countries |= _countries(ad)
        platforms |= set(ad.get("publisher_platforms") or [])
        for body in ad.get("ad_creative_bodies") or []:
            t = " ".join(str(body).split())[:160]
            if t and t not in texts and len(texts) < 3:
                texts.append(t)
        if ad.get("ad_snapshot_url") and len(snaps) < 5:
            snaps.append(ad["ad_snapshot_url"])
    group.countries = sorted(countries)
    group.platforms = sorted(platforms)
    group.sample_texts = texts
    group.snapshot_urls = snaps

    # --- spend estimate (lifetime of the ads found) ---
    if group.eu_reach > 0:
        impressions = group.eu_reach * a.frequency
        group.spend_low = impressions / 1000 * a.cpm_low
        group.spend_high = impressions / 1000 * a.cpm_high
        group.spend_method = "reach"
    else:
        ad_days = 0
        for ad in ads:
            s = parse_date(ad.get("ad_delivery_start_time"))
            if not s:
                continue
            e = parse_date(ad.get("ad_delivery_stop_time")) or today
            ad_days += max(1, (min(e, today) - s).days)
        group.spend_low = ad_days * a.daily_per_ad_low
        group.spend_high = ad_days * a.daily_per_ad_high
        group.spend_method = "ads x days"
    days = max(1, group.days_running)
    group.daily_spend_low = group.spend_low / days
    group.daily_spend_high = group.spend_high / days
    group.orders_low = int(group.spend_low * a.roas_low / a.aov)
    group.orders_high = int(group.spend_high * a.roas_high / a.aov)

    # --- winning score, 0-100 ---
    s_active = min(group.active_ads, 30) / 30 * 30            # many live creatives
    s_age = min(group.days_running, 30) / 30 * 25             # survived 30+ days = profitable
    s_fresh = min(group.new_last_7d, 5) / 5 * 20               # still adding creatives = scaling
    s_reach = min(math.log10(group.eu_reach + 1) / 6, 1) * 15  # 1M reach = full marks
    s_geo = min(len(group.countries), 5) / 5 * 10              # expanding to several countries
    group.score = round(s_active + s_age + s_fresh + s_reach + s_geo)
    return group


def analyze(ads, assumptions=None, today=None, min_active=1):
    assumptions = assumptions or Assumptions()
    today = today or date.today()
    groups = [compute(g, assumptions, today) for g in group_ads(ads)]
    groups = [g for g in groups if g.active_ads >= min_active]
    groups.sort(key=lambda g: (g.score, g.active_ads, g.eu_reach), reverse=True)
    return groups


# ---------------------------------------------------------------- manual CSV input

MANUAL_COLUMNS = ["page_name", "domain", "start_date", "end_date", "ad_url", "text", "countries"]


def ads_from_manual_csv(path):
    """Ads copied by hand from the Ad Library website (e.g. US ads the API does not return).

    Columns: page_name, domain, start_date (YYYY-MM-DD), end_date (empty = still active),
    ad_url, text, countries (comma separated).
    """
    ads = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for i, row in enumerate(csv.DictReader(f)):
            row = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
            ads.append({
                "id": f"manual-{i + 1}",
                "page_name": row.get("page_name", ""),
                "ad_creative_link_captions": [row["domain"]] if row.get("domain") else [],
                "ad_delivery_start_time": row.get("start_date") or None,
                "ad_delivery_stop_time": row.get("end_date") or None,
                "ad_snapshot_url": row.get("ad_url", ""),
                "ad_creative_bodies": [row["text"]] if row.get("text") else [],
                "target_locations": [{"name": c.strip()} for c in row.get("countries", "").split(",") if c.strip()],
            })
    return ads


# ---------------------------------------------------------------- output

def write_csv(groups, path):
    cols = ["rank", "score", "advertiser", "domain", "active_ads", "total_ads", "days_running",
            "new_last_7d", "eu_reach", "countries", "spend_method", "spend_low_usd", "spend_high_usd",
            "daily_spend_low_usd", "daily_spend_high_usd", "orders_low", "orders_high",
            "sample_text", "ad_links"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for i, g in enumerate(groups, 1):
            w.writerow([i, g.score, g.page_name, g.domain, g.active_ads, g.total_ads, g.days_running,
                        g.new_last_7d, g.eu_reach, " ".join(g.countries), g.spend_method,
                        round(g.spend_low), round(g.spend_high), round(g.daily_spend_low),
                        round(g.daily_spend_high), g.orders_low, g.orders_high,
                        " | ".join(g.sample_texts), " ".join(g.snapshot_urls)])


def _money(x):
    return f"${x:,.0f}"


def write_markdown(groups, path, assumptions, title="Ad Library Scout report", today=None, top=25):
    a = assumptions
    today = today or date.today()
    lines = [
        f"# {title}",
        "",
        f"Ngày: {today.isoformat()} · Số nhà quảng cáo: {len(groups)}",
        "",
        "> **Ước tính, không phải số thật.** Meta không công bố chi tiêu của quảng cáo thương mại. "
        f"Chi tiêu tính từ reach EU × tần suất {a.frequency} × CPM ${a.cpm_low:g}–${a.cpm_high:g} "
        f"(hoặc số ads × số ngày × ${a.daily_per_ad_low:g}–${a.daily_per_ad_high:g}/ngày khi không có reach). "
        f"Đơn hàng = chi tiêu × ROAS {a.roas_low:g}–{a.roas_high:g} ÷ AOV ${a.aov:g}.",
        "",
        "| # | Điểm | Nhà quảng cáo | Domain | Ads đang chạy | Ngày chạy | Ads mới 7 ngày | Reach EU | Chi tiêu ước tính | /ngày | Đơn ước tính |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, g in enumerate(groups[:top], 1):
        lines.append(
            f"| {i} | **{g.score}** | {g.page_name} | {g.domain or '-'} | {g.active_ads} | {g.days_running} | "
            f"{g.new_last_7d} | {g.eu_reach:,} | {_money(g.spend_low)}–{_money(g.spend_high)} | "
            f"{_money(g.daily_spend_low)}–{_money(g.daily_spend_high)} | {g.orders_low:,}–{g.orders_high:,} |"
        )
    lines += ["", "## Chi tiết top 10", ""]
    for i, g in enumerate(groups[:10], 1):
        lines.append(f"### {i}. {g.page_name} ({g.domain or 'không rõ domain'}) · điểm {g.score}")
        lines.append(f"- Quốc gia: {', '.join(g.countries) or '-'} · Nền tảng: {', '.join(g.platforms) or '-'}")
        for t in g.sample_texts:
            lines.append(f"- “{t}”")
        for u in g.snapshot_urls[:3]:
            lines.append(f"- Xem ad: {u}")
        lines.append("")
    lines += [
        "## Cách đọc điểm (0–100)",
        "- 30đ: số ads đang chạy (đủ 30 ads = tối đa)",
        "- 25đ: đã chạy ≥ 30 ngày (ads sống lâu thường là ads có lãi)",
        "- 20đ: ads mới trong 7 ngày (đang scale, thêm creative)",
        "- 15đ: reach EU (1 triệu = tối đa)",
        "- 10đ: số quốc gia (≥ 5 = tối đa)",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
