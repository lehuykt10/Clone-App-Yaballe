import io
import json
import sys
import tempfile
import unittest
import urllib.parse
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ads_library import AdLibraryError, build_url, fetch_ads  # noqa: E402
from analyze import (Assumptions, ads_from_library_text, ads_from_manual_csv, analyze,  # noqa: E402
                     domain_of, us_library_url, write_csv, write_markdown)

TODAY = date(2026, 11, 23)


def d(days_ago):
    return (TODAY - timedelta(days=days_ago)).isoformat()


def ad(i, page, caption, start, stop=None, reach=0, countries=("DE",), body="Cool cap"):
    return {
        "id": str(i), "page_id": page, "page_name": page,
        "ad_creative_link_captions": [caption] if caption else [],
        "ad_delivery_start_time": start, "ad_delivery_stop_time": stop,
        "eu_total_reach": reach, "ad_creative_bodies": [body],
        "ad_snapshot_url": f"https://www.facebook.com/ads/library/?id={i}",
        "publisher_platforms": ["facebook", "instagram"],
        "age_country_gender_reach_breakdown": [{"country": c} for c in countries],
    }


# Winner: 12 active ads, oldest 45 days, 4 new this week, big reach, 3 countries
WINNER = [ad(i, "CoolCap Co", "COOLCAP.COM", d(45 if i == 0 else (3 if i < 4 else 20)),
             reach=80000, countries=("DE", "FR", "NL")) for i in range(12)]
# Tester: 2 ads, 5 days old, small reach
TESTER = [ad(100 + i, "New Shop", "www.newshop.store", d(5), reach=1500) for i in range(2)]
# Stopped advertiser: ads ended last week
STOPPED = [ad(200 + i, "Old Shop", "oldshop.com", d(60), stop=d(8), reach=50000) for i in range(5)]


class AnalyzeTests(unittest.TestCase):
    def setUp(self):
        self.groups = analyze(WINNER + TESTER + STOPPED, Assumptions(aov=40), today=TODAY, min_active=1)

    def test_domain_parsing(self):
        self.assertEqual(domain_of({"ad_creative_link_captions": ["WWW.Shop.CO.UK"]}), "shop.co.uk")
        self.assertEqual(domain_of({"ad_creative_link_captions": ["Shop now", "https://x.com/p/1"]}), "x.com")
        self.assertEqual(domain_of({"ad_creative_link_captions": ["Free shipping"]}), "")

    def test_stopped_advertiser_is_dropped_and_winner_ranks_first(self):
        keys = [g.key for g in self.groups]
        self.assertEqual(keys, ["coolcap.com", "newshop.store"])
        self.assertGreater(self.groups[0].score, self.groups[1].score)

    def test_winner_metrics(self):
        g = self.groups[0]
        self.assertEqual(g.active_ads, 12)
        self.assertEqual(g.days_running, 45)
        self.assertEqual(g.new_last_7d, 3)
        self.assertEqual(g.eu_reach, 12 * 80000)
        self.assertEqual(g.countries, ["DE", "FR", "NL"])
        self.assertEqual(g.spend_method, "reach")

    def test_reach_based_estimates(self):
        g = self.groups[0]
        impressions = 960000 * 1.4
        self.assertAlmostEqual(g.spend_low, impressions / 1000 * 6)
        self.assertAlmostEqual(g.spend_high, impressions / 1000 * 12)
        self.assertEqual(g.orders_low, int(g.spend_low * 1.2 / 40))
        self.assertEqual(g.orders_high, int(g.spend_high * 2.5 / 40))
        self.assertAlmostEqual(g.daily_spend_low, g.spend_low / 45)

    def test_score_bounds(self):
        for g in self.groups:
            self.assertTrue(0 <= g.score <= 100)

    def test_fallback_estimate_without_reach(self):
        ads = [ad(1, "P", "p.com", d(10)), ad(2, "P", "p.com", d(4))]
        g = analyze(ads, Assumptions(), today=TODAY)[0]
        self.assertEqual(g.spend_method, "ads x days")
        self.assertEqual(g.spend_low, (10 + 4) * 10)
        self.assertEqual(g.spend_high, (10 + 4) * 50)

    def test_manual_csv_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "manual.csv"
            csv_path.write_text(
                "page_name,domain,start_date,end_date,ad_url,text,countries\n"
                f"US Shop,usshop.com,{d(40)},,https://fb.com/ads/1,Cool cap,US\n"
                f"US Shop,usshop.com,{d(2)},,https://fb.com/ads/2,Cool cap 2,\"US,CA\"\n",
                encoding="utf-8")
            ads = ads_from_manual_csv(csv_path)
            self.assertEqual(len(ads), 2)
            g = analyze(ads, Assumptions(), today=TODAY)[0]
            self.assertEqual((g.domain, g.active_ads, g.days_running), ("usshop.com", 2, 40))
            self.assertEqual(g.countries, ["CA", "US"])
            write_csv([g], Path(tmp) / "r.csv")
            write_markdown([g], Path(tmp) / "r.md", Assumptions(), today=TODAY)
            self.assertIn("usshop.com", (Path(tmp) / "r.md").read_text(encoding="utf-8"))


LIBRARY_TEXT = """Filters
Active
Library ID: 1234567890123
Started running on Oct 5, 2026
Platforms
This ad has multiple versions
See summary details
Cool Head Co
Sponsored
My heavy-head days are quieter now
COOLHEAD.COM
Cool comfort cap
Shop now
3 ads use this creative and text
Active
Library ID: 2234567890123
Started running on Nov 20, 2026
Platforms
See ad details
Cool Head Co
Sponsored
Flip it up and keep working
coolhead.com
Shop now
Inactive
Library ID: 3234567890123
Sep 1, 2026 - Oct 10, 2026
Platforms
See ad details
Old Brand
Sponsored
Last season's offer
oldbrand.store
Shop now
"""


class LibraryTextTests(unittest.TestCase):
    def test_parse_cards(self):
        ads = ads_from_library_text(LIBRARY_TEXT)
        self.assertEqual(len(ads), 3 + 1 + 1)
        first = ads[0]
        self.assertEqual(first["page_name"], "Cool Head Co")
        self.assertEqual(first["ad_creative_link_captions"], ["coolhead.com"])
        self.assertEqual(first["ad_delivery_start_time"], "2026-10-05")
        self.assertIsNone(first["ad_delivery_stop_time"])
        self.assertEqual(first["ad_creative_bodies"], ["My heavy-head days are quieter now"])
        self.assertEqual(first["ad_snapshot_url"], "https://www.facebook.com/ads/library/?id=1234567890123")
        self.assertEqual(first["target_locations"], [{"name": "US"}])
        old = ads[-1]
        self.assertEqual((old["ad_delivery_start_time"], old["ad_delivery_stop_time"]), ("2026-09-01", "2026-10-10"))

    def test_analysis_of_library_text(self):
        groups = analyze(ads_from_library_text(LIBRARY_TEXT), Assumptions(), today=TODAY)
        self.assertEqual([g.key for g in groups], ["coolhead.com"])
        g = groups[0]
        self.assertEqual((g.active_ads, g.days_running, g.new_last_7d), (4, 49, 1))
        self.assertEqual(g.spend_method, "ads x days")

    def test_vietnamese_dates(self):
        text = "Đang hoạt động\nID thư viện: 9234567890123\nBắt đầu chạy vào 5 thg 10, 2026\nShop VN\nĐược tài trợ\nXin chào\nshopvn.com\n"
        ad = ads_from_library_text(text)[0]
        self.assertEqual((ad["page_name"], ad["ad_delivery_start_time"]), ("Shop VN", "2026-10-05"))

    def test_us_link(self):
        url = us_library_url("migraine cap", days=30, today=TODAY)
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertEqual((q["country"], q["q"], q["active_status"]), (["US"], ["migraine cap"], ["active"]))
        self.assertEqual(q["start_date[min]"], [d(30)])


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FetchTests(unittest.TestCase):
    def test_build_url(self):
        url = build_url("migraine cap", ["DE", "FR"], "TOKEN", days=30, today=TODAY)
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertEqual(q["search_terms"], ["migraine cap"])
        self.assertEqual(json.loads(q["ad_reached_countries"][0]), ["DE", "FR"])
        self.assertEqual(q["ad_active_status"], ["ACTIVE"])
        self.assertEqual(q["ad_delivery_date_min"], [d(30)])
        self.assertIn("eu_total_reach", q["fields"][0])

    def test_pagination_and_max(self):
        pages = {
            "first": {"data": [{"id": "1"}, {"id": "2"}], "paging": {"next": "page2"}},
            "page2": {"data": [{"id": "3"}], "paging": {}},
        }
        calls = []

        def opener(url, timeout):
            key = "page2" if url == "page2" else "first"
            calls.append(key)
            return FakeResponse(json.dumps(pages[key]).encode())

        ads = fetch_ads("x", ["DE"], "TOKEN", opener=opener, today=TODAY)
        self.assertEqual([a["id"] for a in ads], ["1", "2", "3"])
        self.assertEqual(calls, ["first", "page2"])
        self.assertEqual(len(fetch_ads("x", ["DE"], "T", max_ads=2, opener=opener, today=TODAY)), 2)

    def test_missing_token(self):
        with self.assertRaises(AdLibraryError):
            fetch_ads("x", ["DE"], "")


if __name__ == "__main__":
    unittest.main()
