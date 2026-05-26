const { chromium } = require('playwright');
const path = require('path');

const VIEWPORTS = [
  { name: 'mobile',  width: 375,  height: 812,  isMobile: true,  hasTouch: true  },
  { name: 'desktop', width: 1440, height: 900,  isMobile: false, hasTouch: false },
];

(async () => {
  const browser = await chromium.launch();
  const url = 'file://' + path.resolve('ship_it_with_ai.html');

  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: vp.isMobile, hasTouch: vp.hasTouch });
    const page = await ctx.newPage();
    await page.goto(url);
    await page.waitForTimeout(600);

    const coverInfo = await page.evaluate(() => {
      const img = document.querySelector('.article-cover img');
      if (!img) return null;
      const r = img.getBoundingClientRect();
      return { src: img.getAttribute('src'), naturalW: img.naturalWidth, naturalH: img.naturalHeight, displayW: r.width.toFixed(0), displayH: r.height.toFixed(0), loaded: img.complete };
    });
    console.log(`${vp.name.padEnd(8)} cover:`, coverInfo);

    await page.screenshot({ path: `screenshots/50_cover_${vp.name}.png`, fullPage: false });
    await ctx.close();
  }

  await browser.close();
})();
