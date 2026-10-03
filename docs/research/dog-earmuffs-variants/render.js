// Render each src/*.html concept sheet to a PNG next to this script.
// Usage: node render.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const src = path.join(__dirname, 'src');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1100 } });
  for (const f of fs.readdirSync(src).filter((f) => f.endsWith('.html')).sort()) {
    await page.goto('file://' + path.join(src, f));
    await page.waitForTimeout(200);
    const out = path.join(__dirname, f.replace('.html', '.png'));
    await page.screenshot({ path: out });
    console.log('wrote', out);
  }
  await browser.close();
})();
