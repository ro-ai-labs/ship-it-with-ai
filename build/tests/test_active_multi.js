const { chromium } = require('playwright');
const path = require('path');

const VIEWPORTS = [
  { name: 'mobile',  width: 375,  height: 812,  isMobile: true,  hasTouch: true  },
  { name: 'tablet',  width: 768,  height: 1024, isMobile: false, hasTouch: false },
  { name: 'desktop', width: 1440, height: 900,  isMobile: false, hasTouch: false },
  { name: 'wide',    width: 1920, height: 1080, isMobile: false, hasTouch: false },
];

const CHECKS = [
  { href: '#chapter-10', label: 'Chapter 10 (Adoption)' },
  { href: '#chapter-5',  label: 'Chapter 5 (Six-phase loop)' },
  { href: '#appendix-c', label: 'Appendix C (Sources)' },
  { href: '#foreword',   label: 'Foreword' },
];

(async () => {
  const browser = await chromium.launch();
  const url = 'file://' + path.resolve('ship_it_with_ai.html');

  for (const vp of VIEWPORTS) {
    console.log(`\n=== ${vp.name} (${vp.width}x${vp.height}) ===`);
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: vp.isMobile, hasTouch: vp.hasTouch });
    const page = await ctx.newPage();
    await page.goto(url);
    await page.waitForTimeout(400);

    for (const check of CHECKS) {
      // Reset to top
      await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
      await page.waitForTimeout(150);
      // On mobile/tablet TOC is a drawer - open it first
      const menuToggle = page.locator('#menuToggle');
      const menuVisible = await menuToggle.isVisible().catch(() => false);
      if (menuVisible) {
        await menuToggle.click();
        await page.waitForTimeout(150);
      }
      // Find the TOC link and click
      const link = page.locator(`.sidebar a[href="${check.href}"]`).first();
      const linkCount = await link.count();
      if (linkCount === 0) {
        console.log(`  ${check.label.padEnd(30)} - LINK NOT FOUND in sidebar`);
        continue;
      }
      await link.click();
      // Wait long enough for smooth scroll on a long page (4s budget)
      await page.waitForTimeout(2800);

      const activeAfter = await page.evaluate(() => {
        const a = document.querySelector('.sidebar a.active');
        return a ? a.getAttribute('href') : null;
      });
      const scrollY = await page.evaluate(() => window.scrollY);
      const targetVp = await page.evaluate((id) => {
        const el = document.getElementById(id);
        return el ? el.getBoundingClientRect().top : null;
      }, check.href.slice(1));
      const okHref = activeAfter === check.href;
      const okPos = targetVp !== null && Math.abs(targetVp - 72) < 30;
      const verdict = (okHref && okPos) ? 'OK' : `BAD (active=${activeAfter}, viewport y=${targetVp?.toFixed?.(0) ?? targetVp})`;
      console.log(`  ${check.label.padEnd(30)} - scrollY=${String(scrollY).padStart(7)} - ${verdict}`);
    }

    await ctx.close();
  }

  await browser.close();
})();
