"""Client for the official Meta Ad Library API (Graph API `ads_archive` endpoint).

For commercial (non-political) ads the API only returns ads delivered in the EU,
and it does not return spend or impressions. It does return `eu_total_reach`,
delivery dates, countries and creative text, which `analyze.py` turns into
estimates.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta

DEFAULT_API_VERSION = os.environ.get("META_GRAPH_VERSION", "v23.0")

EU_COUNTRIES = [
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE",
    "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
]

FIELDS = [
    "id",
    "page_id",
    "page_name",
    "ad_creation_time",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "ad_creative_bodies",
    "ad_creative_link_captions",
    "ad_creative_link_titles",
    "ad_snapshot_url",
    "publisher_platforms",
    "languages",
    "eu_total_reach",
    "target_locations",
    "age_country_gender_reach_breakdown",
]

RETRYABLE_CODES = {4, 17, 32, 613}  # Graph API rate-limit error codes


class AdLibraryError(Exception):
    pass


def build_url(search_terms, countries, token, days=30, active_only=True, page_size=200,
              api_version=DEFAULT_API_VERSION, today=None):
    today = today or date.today()
    params = {
        "search_terms": search_terms,
        "search_type": "KEYWORD_UNORDERED",
        "ad_type": "ALL",
        "ad_reached_countries": json.dumps(list(countries)),
        "ad_active_status": "ACTIVE" if active_only else "ALL",
        "ad_delivery_date_min": (today - timedelta(days=days)).isoformat(),
        "fields": ",".join(FIELDS),
        "limit": str(page_size),
        "access_token": token,
    }
    return f"https://graph.facebook.com/{api_version}/ads_archive?" + urllib.parse.urlencode(params)


def _get_json(url, opener, sleep, retries=3):
    for attempt in range(retries + 1):
        try:
            with opener(url, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                err = json.loads(e.read().decode("utf-8")).get("error", {})
            except (ValueError, AttributeError):
                err = {}
            if err.get("code") in RETRYABLE_CODES and attempt < retries:
                sleep(30 * (attempt + 1))
                continue
            # Never echo the URL: it contains the access token.
            raise AdLibraryError(
                f"Ad Library API error {e.code}: {err.get('message', e.reason)} "
                f"(code {err.get('code')}, subcode {err.get('error_subcode')})"
            ) from None
    raise AdLibraryError("Ad Library API: too many retries")


def fetch_ads(search_terms, countries, token, days=30, active_only=True, max_ads=2000,
              page_size=200, api_version=DEFAULT_API_VERSION,
              opener=urllib.request.urlopen, sleep=time.sleep, today=None):
    """Return up to `max_ads` ads (dicts) matching the search, following pagination."""
    if not token:
        raise AdLibraryError("Missing access token: set META_ACCESS_TOKEN.")
    url = build_url(search_terms, countries, token, days, active_only, page_size, api_version, today)
    ads = []
    while url and len(ads) < max_ads:
        data = _get_json(url, opener, sleep)
        ads.extend(data.get("data", []))
        url = (data.get("paging") or {}).get("next")
    for ad in ads:
        ad.setdefault("_search_terms", search_terms)
    return ads[:max_ads]
