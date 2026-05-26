const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('file://' + path.resolve('ship_it_with_ai.html'));

  await page.locator('.article-footer').scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.locator('.article-footer').screenshot({ path: 'screenshots/25_footer_light.png' });
  console.log('25_footer_light.png saved');

  await page.locator('#themeToggle').click();
  await page.waitForTimeout(400);
  await page.locator('.article-footer').scrollIntoViewIfNeeded();
  await page.waitForTimeout(200);
  await page.locator('.article-footer').screenshot({ path: 'screenshots/26_footer_dark.png' });
  console.log('26_footer_dark.png saved');

  await browser.close();
})();
