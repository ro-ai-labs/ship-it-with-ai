const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const url = 'file://' + path.resolve('ship_it_with_ai.html');
  await page.goto(url);

  const tryBox = page.locator('.try-box').first();
  await tryBox.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await tryBox.screenshot({ path: 'screenshots/17_try_box.png' });
  console.log('17_try_box.png saved');

  await page.locator('header.topbar').screenshot({ path: 'screenshots/18_topbar_with_font_controls.png' });
  console.log('18_topbar_with_font_controls.png saved');

  // Start at medium, click A+ once to reach large
  await page.locator('#fontInc').click();
  await page.waitForTimeout(200);
  await tryBox.scrollIntoViewIfNeeded();
  await page.waitForTimeout(200);
  await tryBox.screenshot({ path: 'screenshots/19_try_box_large_font.png' });
  console.log('19_try_box_large_font.png saved');

  const dataFontLarge = await page.locator('html').getAttribute('data-font');
  const incDisabled = await page.locator('#fontInc').isDisabled();
  console.log(`After one A+ click: data-font=${dataFontLarge}, fontInc disabled=${incDisabled}`);

  // Click A- twice to reach small
  await page.locator('#fontDec').click();
  await page.waitForTimeout(100);
  await page.locator('#fontDec').click();
  await page.waitForTimeout(200);
  const dataFontSmall = await page.locator('html').getAttribute('data-font');
  const decDisabled = await page.locator('#fontDec').isDisabled();
  console.log(`After two A- clicks: data-font=${dataFontSmall}, fontDec disabled=${decDisabled}`);

  await browser.close();
})();
