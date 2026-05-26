const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve('ship_it_with_ai.html'));

  // Top of page: no cover anymore
  await page.locator('.article-header').screenshot({ path: 'screenshots/51_header_no_cover.png' });
  console.log('51_header_no_cover.png');

  // Scroll to the new cover at the end
  await page.locator('.article-cover-end').scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'screenshots/52_cover_at_end.png' });
  console.log('52_cover_at_end.png');

  // Verify cover at top is gone but cover at end is rendered
  const topCover = await page.locator('.article-header .article-cover').count();
  const endCover = await page.locator('.article-cover-end').count();
  console.log(`top cover count: ${topCover}, end cover count: ${endCover}`);

  await browser.close();
})();
