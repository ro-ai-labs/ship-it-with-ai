const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('file://' + path.resolve('ship_it_with_ai.html'));

  await page.locator('.article-author').scrollIntoViewIfNeeded();
  await page.waitForTimeout(200);
  await page.locator('.article-header').screenshot({ path: 'screenshots/22_byline_with_link.png' });
  console.log('22_byline_with_link.png saved');

  await page.locator('.article-author a').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'screenshots/23_contact_after_click.png', fullPage: false });
  console.log('23_contact_after_click.png saved (after clicking byline link)');

  const sampleAppendixLink = page.locator('a[href="https://arxiv.org/abs/2507.09089"]').first();
  await sampleAppendixLink.scrollIntoViewIfNeeded();
  await page.waitForTimeout(200);
  const linkParent = sampleAppendixLink.locator('xpath=..');
  await linkParent.screenshot({ path: 'screenshots/24_appendix_link.png' });
  console.log('24_appendix_link.png saved');

  await browser.close();
})();
