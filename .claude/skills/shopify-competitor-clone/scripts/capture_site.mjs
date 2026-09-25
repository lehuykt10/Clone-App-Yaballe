#!/usr/bin/env node
// Capture a website's structure, design tokens, tech stack and performance
// so it can be analysed (competitor teardown) or benchmarked (our own preview).
//
// Usage:
//   node capture_site.mjs <url> [--out <dir>] [--pages <n>] [--no-products]
//
// Output (in --out, default ./teardown/<hostname>):
//   report.json               full machine-readable data
//   report.md                 human-readable summary
//   screens/<page>-<vp>.png   full-page screenshots (desktop + mobile)

import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const require = createRequire(import.meta.url);
function loadPlaywright() {
  try {
    return require('playwright');
  } catch {
    const globalRoot = execSync('npm root -g').toString().trim();
    return require(path.join(globalRoot, 'playwright'));
  }
}
const { chromium } = loadPlaywright();

// ---------- args ----------
const args = process.argv.slice(2);
if (!args[0] || args[0].startsWith('--')) {
  console.error('Usage: node capture_site.mjs <url> [--out <dir>] [--pages <n>] [--no-products]');
  process.exit(1);
}
const startUrl = new URL(args[0].startsWith('http') ? args[0] : `https://${args[0]}`);
const flag = (name, def) => {
  const i = args.indexOf(name);
  return i === -1 ? def : args[i + 1];
};
const outDir = path.resolve(flag('--out', path.join('teardown', startUrl.hostname)));
const maxPages = Number(flag('--pages', 5));
const fetchProducts = !args.includes('--no-products');
fs.mkdirSync(path.join(outDir, 'screens'), { recursive: true });

const VIEWPORTS = {
  desktop: { width: 1440, height: 900, isMobile: false },
  mobile: { width: 390, height: 844, isMobile: true, deviceScaleFactor: 2, hasTouch: true },
};
const UA_MOBILE =
  'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

// ---------- in-page collectors ----------
// Installed before navigation so LCP / CLS are observed from the start.
const PERF_INIT = () => {
  window.__perf = { lcp: 0, cls: 0 };
  try {
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) window.__perf.lcp = e.startTime;
    }).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) if (!e.hadRecentInput) window.__perf.cls += e.value;
    }).observe({ type: 'layout-shift', buffered: true });
  } catch {}
};

function extractPage() {
  const txt = (el) => (el?.innerText || el?.textContent || '').replace(/\s+/g, ' ').trim();
  const cs = (el) => (el ? getComputedStyle(el) : null);
  const pick = (sel) => document.querySelector(sel);

  // Sections: Shopify wraps each section in #shopify-section-*; otherwise use
  // top-level semantic blocks.
  let sectionEls = [...document.querySelectorAll('[id^="shopify-section-"]')];
  const isShopifySections = sectionEls.length > 0;
  if (!isShopifySections) {
    sectionEls = [...document.querySelectorAll('body > *, main > *, main > * > section')].filter(
      (el) => el.offsetHeight > 40 && !['SCRIPT', 'STYLE', 'NOSCRIPT', 'LINK'].includes(el.tagName),
    );
  }
  const sections = sectionEls.map((el, i) => {
    const r = el.getBoundingClientRect();
    const heading = el.querySelector('h1,h2,h3');
    return {
      order: i + 1,
      id: el.id || null,
      type: isShopifySections
        ? el.id.replace(/^shopify-section-(template--\d+__)?/, '').replace(/_[A-Za-z0-9]{6}$/, '')
        : el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''),
      heading: heading ? txt(heading).slice(0, 120) : null,
      top: Math.round(r.top + window.scrollY),
      height: Math.round(r.height),
      images: el.querySelectorAll('img').length,
      buttons: [...el.querySelectorAll('a.button,a.btn,button,[class*="button"]')]
        .map(txt)
        .filter(Boolean)
        .slice(0, 5),
    };
  });

  const outline = [...document.querySelectorAll('h1,h2,h3')]
    .slice(0, 60)
    .map((h) => `${h.tagName}: ${txt(h).slice(0, 100)}`)
    .filter((s) => s.length > 4);

  const btn = pick('button[name="add"], form[action*="/cart/add"] button, .button--primary, .btn-primary, a.button, .btn');
  const header = pick('header, .header, #shopify-section-header');
  const styleOf = (el) =>
    el && {
      font: cs(el).fontFamily,
      size: cs(el).fontSize,
      weight: cs(el).fontWeight,
      color: cs(el).color,
      bg: cs(el).backgroundColor,
      radius: cs(el).borderRadius,
    };

  // Colour frequency across visible elements -> rough palette.
  const colors = {};
  for (const el of [...document.querySelectorAll('body *')].slice(0, 3000)) {
    const s = cs(el);
    for (const c of [s.backgroundColor, s.color]) {
      if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') colors[c] = (colors[c] || 0) + 1;
    }
  }
  const palette = Object.entries(colors)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([c, n]) => ({ color: c, uses: n }));

  const scripts = [...document.scripts].map((s) => s.src).filter(Boolean);
  const thirdParty = [...new Set(scripts.map((s) => { try { return new URL(s).hostname; } catch { return null; } }))]
    .filter((h) => h && h !== location.hostname);

  const jsonLd = [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map((s) => { try { const j = JSON.parse(s.textContent); return [].concat(j).map((x) => x['@type']); } catch { return []; } })
    .flat();

  const imgs = [...document.images];
  const links = [...document.querySelectorAll('a[href]')].map((a) => a.href);
  const nav = [...document.querySelectorAll('header nav a, header a[href*="/collections"], header a[href*="/pages"]')]
    .map(txt)
    .filter(Boolean)
    .slice(0, 30);

  const perf = performance.getEntriesByType('navigation')[0];
  const resources = performance.getEntriesByType('resource');

  return {
    title: document.title,
    metaDescription: pick('meta[name="description"]')?.content || null,
    canonical: pick('link[rel="canonical"]')?.href || null,
    ogImage: pick('meta[property="og:image"]')?.content || null,
    lang: document.documentElement.lang || null,
    shopify: window.Shopify
      ? { shop: window.Shopify.shop, theme: window.Shopify.theme?.name || null, themeStoreId: window.Shopify.theme?.theme_store_id || null, currency: window.Shopify.currency?.active || null }
      : null,
    sections,
    outline,
    nav: [...new Set(nav)],
    design: { body: styleOf(document.body), h1: styleOf(pick('h1')), h2: styleOf(pick('h2')), button: styleOf(btn), header: styleOf(header), palette },
    seo: {
      h1Count: document.querySelectorAll('h1').length,
      jsonLd,
      imagesTotal: imgs.length,
      imagesMissingAlt: imgs.filter((i) => !i.alt?.trim()).length,
    },
    trustSignals: {
      reviewsWidget: /judge\.me|loox|yotpo|okendo|stamped|reviews\.io|trustpilot/i.test(scripts.join(' ') + document.body.innerHTML.slice(0, 200000)),
      guaranteeText: /money[- ]back|guarantee|hoàn tiền|bảo hành/i.test(document.body.innerText),
      freeShippingText: /free shipping|miễn phí vận chuyển|freeship/i.test(document.body.innerText),
      countdownOrUrgency: /only \d+ left|sold out soon|ends in|hurry|limited/i.test(document.body.innerText),
    },
    thirdPartyScripts: thirdParty,
    links,
    perf: {
      ttfbMs: perf ? Math.round(perf.responseStart) : null,
      domContentLoadedMs: perf ? Math.round(perf.domContentLoadedEventEnd) : null,
      loadMs: perf ? Math.round(perf.loadEventEnd) : null,
      lcpMs: Math.round(window.__perf?.lcp || 0),
      cls: Number((window.__perf?.cls || 0).toFixed(3)),
      requests: resources.length + 1,
      transferKB: Math.round((resources.reduce((a, r) => a + (r.transferSize || 0), 0) + (perf?.transferSize || 0)) / 1024),
      scripts: scripts.length,
    },
    pageHeight: document.documentElement.scrollHeight,
  };
}

// ---------- helpers ----------
async function autoScroll(page) {
  await page.evaluate(async () => {
    const step = window.innerHeight * 0.8;
    for (let y = 0; y < document.documentElement.scrollHeight && y < 30000; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 150));
    }
    window.scrollTo(0, 0);
  });
}

function slug(u) {
  const p = new URL(u).pathname.replace(/\/+$/, '');
  return p ? p.slice(1).replace(/[^a-z0-9]+/gi, '-').slice(0, 60) : 'home';
}

// Pick representative internal pages: collection, product, about, contact...
function discoverPages(links, origin) {
  const internal = [...new Set(links)]
    .filter((l) => { try { return new URL(l).origin === origin; } catch { return false; } })
    .map((l) => l.split('#')[0].split('?')[0]);
  const patterns = [/\/collections\/(?!all$)[^/]+$/, /\/products\/[^/]+$/, /\/pages\/(about|our-story|story)/i, /\/pages\/(faq|contact)/i, /\/collections\/all$/, /\/blogs\//];
  const chosen = [];
  for (const re of patterns) {
    const hit = internal.find((l) => re.test(new URL(l).pathname) && !chosen.includes(l));
    if (hit) chosen.push(hit);
  }
  return chosen;
}

async function capture(browser, url, vpName) {
  const vp = VIEWPORTS[vpName];
  const ctx = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    isMobile: vp.isMobile,
    hasTouch: vp.hasTouch,
    deviceScaleFactor: vp.deviceScaleFactor || 1,
    userAgent: vp.isMobile ? UA_MOBILE : undefined,
  });
  const page = await ctx.newPage();
  await page.addInitScript(PERF_INIT);
  try {
    const res = await page.goto(url, { waitUntil: 'load', timeout: 60000 });
    if (res && res.status() >= 400) {
      await ctx.close();
      return { error: `HTTP ${res.status()}` };
    }
  } catch (e) {
    await ctx.close();
    return { error: String(e.message || e) };
  }
  await page.waitForTimeout(1500);
  const data = await page.evaluate(extractPage);
  await autoScroll(page);
  await page.waitForTimeout(800);
  const file = path.join(outDir, 'screens', `${slug(url)}-${vpName}.png`);
  await page.screenshot({ path: file, fullPage: true }).catch(() => {});
  await ctx.close();
  return { ...data, screenshot: path.relative(outDir, file) };
}

// Shopify exposes a public catalog feed; summarise it for pricing/assortment analysis.
// Fetched through the browser so it follows the same proxy settings as the pages.
async function productSummary(browser, origin) {
  const ctx = await browser.newContext();
  try {
    const res = await ctx.request.get(`${origin}/products.json?limit=250`);
    if (!res.ok()) return null;
    const { products = [] } = await res.json();
    const prices = products.flatMap((p) => p.variants.map((v) => Number(v.price))).filter((n) => n > 0);
    const compare = products.flatMap((p) => p.variants.map((v) => Number(v.compare_at_price) || 0)).filter((n) => n > 0);
    const count = (arr) => Object.entries(arr.reduce((m, k) => ((m[k] = (m[k] || 0) + 1), m), {})).sort((a, b) => b[1] - a[1]).slice(0, 15);
    return {
      productCount: products.length,
      priceMin: prices.length ? Math.min(...prices) : null,
      priceMax: prices.length ? Math.max(...prices) : null,
      priceMedian: prices.length ? prices.sort((a, b) => a - b)[Math.floor(prices.length / 2)] : null,
      onSaleVariants: compare.length,
      productTypes: count(products.map((p) => p.product_type || '(none)')),
      topTags: count(products.flatMap((p) => p.tags || [])),
      optionNames: count(products.flatMap((p) => p.options?.map((o) => o.name) || [])),
      // Titles + prices only: structure for analysis, not content to copy.
      products: products.slice(0, 50).map((p) => ({
        title: p.title,
        handle: p.handle,
        type: p.product_type,
        price: p.variants?.[0]?.price,
        compareAt: p.variants?.[0]?.compare_at_price,
        variants: p.variants?.length,
        images: p.images?.length,
      })),
    };
  } catch {
    return null;
  } finally {
    await ctx.close();
  }
}

// ---------- main ----------
// Honour HTTPS_PROXY explicitly so pages and the catalog request share one route.
const proxyServer = process.env.HTTPS_PROXY || process.env.https_proxy;
const browser = await chromium.launch(
  proxyServer ? { proxy: { server: proxyServer, bypass: '<-loopback>,localhost,127.0.0.1' } } : {},
);
const report = { url: startUrl.href, capturedAt: new Date().toISOString(), pages: [] };

const home = { desktop: await capture(browser, startUrl.href, 'desktop'), mobile: await capture(browser, startUrl.href, 'mobile') };
if (home.desktop.error) {
  console.error(`Failed to load ${startUrl.href}: ${home.desktop.error}`);
  await browser.close();
  process.exit(2);
}
report.pages.push({ url: startUrl.href, ...home });

const extra = discoverPages(home.desktop.links || [], startUrl.origin).slice(0, Math.max(0, maxPages - 1));
for (const url of extra) {
  report.pages.push({ url, desktop: await capture(browser, url, 'desktop'), mobile: await capture(browser, url, 'mobile') });
}
report.shopify = home.desktop.shopify;
report.catalog = fetchProducts && report.shopify ? await productSummary(browser, startUrl.origin) : null;
await browser.close();
for (const p of report.pages) for (const vp of ['desktop', 'mobile']) if (p[vp]) delete p[vp].links;

fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2));

// ---------- markdown summary ----------
const md = [];
const d = home.desktop;
md.push(`# Site capture: ${startUrl.hostname}`, '', `Captured: ${report.capturedAt}`, '');
md.push('## Platform', '');
md.push(report.shopify ? `- Shopify store \`${report.shopify.shop}\`, theme **${report.shopify.theme}** (theme store id: ${report.shopify.themeStoreId ?? 'custom'}), currency ${report.shopify.currency}` : '- Not detected as Shopify');
md.push(`- Third-party scripts / apps: ${d.thirdPartyScripts.join(', ') || 'none'}`, '');
md.push('## Performance (home)', '', '| Metric | Desktop | Mobile |', '|---|---|---|');
for (const k of ['ttfbMs', 'lcpMs', 'cls', 'loadMs', 'requests', 'transferKB', 'scripts']) {
  md.push(`| ${k} | ${home.desktop.perf?.[k] ?? '-'} | ${home.mobile.perf?.[k] ?? '-'} |`);
}
md.push('', '## Design tokens (home, desktop)', '');
for (const [k, v] of Object.entries(d.design)) if (k !== 'palette' && v) md.push(`- **${k}**: ${v.font} · ${v.size} / ${v.weight} · color ${v.color} · bg ${v.bg} · radius ${v.radius}`);
md.push(`- **palette** (most used): ${d.design.palette.map((p) => p.color).join(' · ')}`, '');
md.push('## SEO & trust', '');
md.push(`- Title: ${d.title}`, `- Meta description: ${d.metaDescription ?? '**missing**'}`, `- H1 count: ${d.seo.h1Count}`, `- JSON-LD: ${d.seo.jsonLd.join(', ') || '**none**'}`, `- Images missing alt: ${d.seo.imagesMissingAlt}/${d.seo.imagesTotal}`);
md.push(`- Trust signals: ${Object.entries(d.trustSignals).map(([k, v]) => `${k}=${v ? 'yes' : 'no'}`).join(', ')}`, '');
md.push('## Navigation', '', d.nav.join(' · ') || '(not detected)', '');
for (const p of report.pages) {
  const pd = p.desktop;
  md.push(`## Page: ${p.url}`, '');
  if (pd?.error) { md.push(`Error: ${pd.error}`, ''); continue; }
  md.push(`Screens: \`${pd.screenshot}\`, \`${p.mobile?.screenshot}\` · LCP desktop ${pd.perf.lcpMs}ms / mobile ${p.mobile?.perf?.lcpMs}ms`, '');
  md.push('| # | Section type | Heading | Height | Imgs | Buttons |', '|---|---|---|---|---|---|');
  for (const s of pd.sections) md.push(`| ${s.order} | ${s.type} | ${(s.heading || '').replace(/\|/g, '/')} | ${s.height} | ${s.images} | ${s.buttons.join(' / ').replace(/\|/g, '/')} |`);
  md.push('');
}
if (report.catalog) {
  const c = report.catalog;
  md.push('## Catalog', '', `- Products: ${c.productCount} · price ${c.priceMin}–${c.priceMax} (median ${c.priceMedian}) · variants on sale: ${c.onSaleVariants}`);
  md.push(`- Types: ${c.productTypes.map(([k, n]) => `${k} (${n})`).join(', ')}`, `- Options: ${c.optionNames.map(([k, n]) => `${k} (${n})`).join(', ')}`, '');
}
fs.writeFileSync(path.join(outDir, 'report.md'), md.join('\n'));
console.log(`Saved ${path.join(outDir, 'report.md')} (${report.pages.length} pages)`);
