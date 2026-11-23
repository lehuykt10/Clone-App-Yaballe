#!/usr/bin/env python3
"""Ad Library Scout: find products/stores that look like winners in the Meta Ad Library.

Examples:
  export META_ACCESS_TOKEN=...            # see README.md
  python3 tools/ads_library_scout/scout.py run --terms "migraine cap" --countries DE,FR,NL,SE --aov 35
  python3 tools/ads_library_scout/scout.py analyze --manual my_us_ads.csv --aov 35
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ads_library import EU_COUNTRIES, AdLibraryError, fetch_ads  # noqa: E402
from analyze import Assumptions, ads_from_manual_csv, analyze, write_csv, write_markdown  # noqa: E402


def _countries(value):
    if value.upper() == "EU":
        return EU_COUNTRIES
    return [c.strip().upper() for c in value.split(",") if c.strip()]


def _add_assumption_args(p):
    d = Assumptions()
    p.add_argument("--aov", type=float, default=d.aov, help="giá trị đơn trung bình (USD)")
    p.add_argument("--cpm-low", type=float, default=d.cpm_low)
    p.add_argument("--cpm-high", type=float, default=d.cpm_high)
    p.add_argument("--frequency", type=float, default=d.frequency)
    p.add_argument("--roas-low", type=float, default=d.roas_low)
    p.add_argument("--roas-high", type=float, default=d.roas_high)
    p.add_argument("--daily-per-ad-low", type=float, default=d.daily_per_ad_low)
    p.add_argument("--daily-per-ad-high", type=float, default=d.daily_per_ad_high)
    p.add_argument("--min-active", type=int, default=3, help="bỏ nhà quảng cáo có ít ads đang chạy hơn số này")
    p.add_argument("--out-dir", default="ad-scout-reports")


def _assumptions(args):
    return Assumptions(cpm_low=args.cpm_low, cpm_high=args.cpm_high, frequency=args.frequency,
                       daily_per_ad_low=args.daily_per_ad_low, daily_per_ad_high=args.daily_per_ad_high,
                       roas_low=args.roas_low, roas_high=args.roas_high, aov=args.aov)


def _fetch(args):
    ads = []
    for term in args.terms:
        got = fetch_ads(term, _countries(args.countries), os.environ.get("META_ACCESS_TOKEN", ""),
                        days=args.days, max_ads=args.max_ads)
        print(f"  '{term}': {len(got)} ads", file=sys.stderr)
        ads.extend(got)
    seen, unique = set(), []
    for ad in ads:
        if ad.get("id") not in seen:
            seen.add(ad.get("id"))
            unique.append(ad)
    return unique


def _report(ads, args, slug):
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    a = _assumptions(args)
    groups = analyze(ads, a, min_active=args.min_active)
    stem = f"{date.today().isoformat()}-{slug}"
    write_csv(groups, out / f"{stem}.csv")
    write_markdown(groups, out / f"{stem}.md", a, title=f"Ad Library Scout: {slug}")
    print(f"{len(ads)} ads → {len(groups)} nhà quảng cáo. Báo cáo: {out / (stem + '.md')} và .csv")
    for i, g in enumerate(groups[:5], 1):
        print(f"  {i}. [{g.score}] {g.page_name} ({g.domain or '-'}) · {g.active_ads} ads · "
              f"{g.days_running} ngày · ~${g.daily_spend_low:,.0f}-{g.daily_spend_high:,.0f}/ngày")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name in ("fetch", "run"):
        p = sub.add_parser(name)
        p.add_argument("--terms", nargs="+", required=True, help="từ khóa, mỗi từ khóa trong ngoặc kép")
        p.add_argument("--countries", default="DE,FR,NL,SE,IT,ES",
                       help="mã quốc gia EU, cách nhau bởi dấu phẩy, hoặc 'EU'")
        p.add_argument("--days", type=int, default=30, help="ads có hiển thị trong N ngày gần nhất")
        p.add_argument("--max-ads", type=int, default=1000, help="tối đa số ads cho mỗi từ khóa")
        if name == "fetch":
            p.add_argument("--out", default="ad-scout-reports/raw-ads.json")
        else:
            _add_assumption_args(p)

    p = sub.add_parser("analyze")
    p.add_argument("--raw", nargs="*", default=[], help="file JSON từ lệnh fetch")
    p.add_argument("--manual", nargs="*", default=[], help="file CSV ads tự sưu tầm (xem README)")
    _add_assumption_args(p)

    args = ap.parse_args(argv)
    try:
        if args.cmd == "fetch":
            ads = _fetch(args)
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(json.dumps(ads, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"Đã lưu {len(ads)} ads vào {args.out}")
        elif args.cmd == "run":
            ads = _fetch(args)
            _report(ads, args, "-".join(t.replace(" ", "_") for t in args.terms)[:60])
        else:
            ads = []
            for f in args.raw:
                ads.extend(json.loads(Path(f).read_text(encoding="utf-8")))
            for f in args.manual:
                ads.extend(ads_from_manual_csv(f))
            if not ads:
                ap.error("cần ít nhất một --raw hoặc --manual")
            _report(ads, args, "analysis")
    except AdLibraryError as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
