const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  const url = 'file://' + path.resolve('ship_it_with_ai.html');
  await page.goto(url);

  const tryBoxes = page.locator('.try-box');
  const count = await tryBoxes.count();
  console.log(`try-box count: ${count}`);

  // Screenshot the new Ch 7 architecture-review box (index 3 of 5: Ch2=0, Ch3=1, Ch6=2, Ch7=3, Ch8=4)
  await tryBoxes.nth(3).scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await tryBoxes.nth(3).screenshot({ path: 'screenshots/21_try_box_ch7.png' });
  console.log('21_try_box_ch7.png saved (Ch 7 architecture-review box)');

  await browser.close();
})();
