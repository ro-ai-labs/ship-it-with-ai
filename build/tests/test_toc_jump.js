const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve('ship_it_with_ai.html'));

  const tests = [
    { tocSelector: 'a[href="#chapter-1"]', targetId: 'chapter-1', label: 'Chapter 1' },
    { tocSelector: 'a[href="#chapter-5"]', targetId: 'chapter-5', label: 'Chapter 5' },
    { tocSelector: 'a[href="#nine-seconds"]', targetId: 'nine-seconds', label: 'Nine seconds' },
    { tocSelector: 'a[href="#appendix-c"]', targetId: 'appendix-c', label: 'Appendix C' },
    { tocSelector: 'a[href="#where-i-am-coming-from"]', targetId: 'where-i-am-coming-from', label: 'Where I am coming from (H3)' },
  ];

  for (const t of tests) {
    // Start fresh: scroll to top
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
    await page.waitForTimeout(200);

    // Click TOC link
    await page.locator(t.tocSelector).first().click();
    await page.waitForTimeout(2500); // wait for smooth scroll to fully complete

    // Measure where the target landed in viewport
    const measurement = await page.locator('#' + t.targetId).boundingBox();
    const scrollY = await page.evaluate(() => window.scrollY);
    const topbarHeight = await page.locator('header.topbar').boundingBox();
    const topbarBottom = topbarHeight ? (topbarHeight.y + topbarHeight.height) : 0;

    const targetTopInViewport = measurement ? measurement.y : null;
    const distanceFromTopbar = targetTopInViewport !== null ? (targetTopInViewport - topbarBottom) : null;
    const verdict = distanceFromTopbar !== null
      ? (Math.abs(distanceFromTopbar) < 30 ? 'OK' : (distanceFromTopbar < 0 ? 'TARGET HIDDEN UNDER TOPBAR' : `TARGET ${distanceFromTopbar.toFixed(0)}px BELOW TOPBAR`))
      : 'NO TARGET FOUND';

    console.log(`${t.label}: scrollY=${scrollY.toFixed(0)} | target top in viewport=${targetTopInViewport?.toFixed(0)} | topbar bottom=${topbarBottom?.toFixed(0)} | ${verdict}`);
  }

  await browser.close();
})();
