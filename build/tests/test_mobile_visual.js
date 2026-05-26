const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve('ship_it_with_ai.html'));
  await page.waitForTimeout(500);

  // Top of page
  await page.screenshot({ path: 'screenshots/55_mobile_top.png' });

  // Find the first case-note and screenshot around it
  const caseNote = page.locator('.case-note').first();
  await caseNote.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.screenshot({ path: 'screenshots/56_mobile_case_note.png' });

  // Scroll-right test: try to scroll the page right
  const scrollXBefore = await page.evaluate(() => window.scrollX);
  await page.evaluate(() => window.scrollTo({ left: 500, top: 100 }));
  await page.waitForTimeout(200);
  const scrollXAfter = await page.evaluate(() => window.scrollX);
  console.log(`scrollX before=${scrollXBefore}, after attempt=${scrollXAfter} (should be 0 - page should not scroll horizontally)`);

  await browser.close();
})();
