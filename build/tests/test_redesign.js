const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const url = 'file://' + path.resolve('ship_it_with_ai.html');

  // ---- DESKTOP ----
  const desk = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const dp = await desk.newPage();
  await dp.goto(url);

  await dp.screenshot({ path: 'screenshots/30_desktop_top.png' });
  console.log('30_desktop_top.png');

  const card = dp.locator('.source-card').first();
  await card.scrollIntoViewIfNeeded();
  await dp.waitForTimeout(300);
  await card.screenshot({ path: 'screenshots/31_source_card_light.png' });
  console.log('31_source_card_light.png');

  await dp.locator('#themeToggle').click();
  await dp.waitForTimeout(400);
  await card.scrollIntoViewIfNeeded();
  await dp.waitForTimeout(200);
  await card.screenshot({ path: 'screenshots/32_source_card_dark.png' });
  console.log('32_source_card_dark.png');

  await dp.locator('#themeToggle').click();
  await dp.waitForTimeout(300);

  await dp.evaluate(() => window.scrollTo(0, 0));
  await dp.waitForTimeout(200);
  await dp.locator('#widthToggle').click();
  await dp.waitForTimeout(300);
  const w1 = await dp.locator('html').getAttribute('data-width');
  console.log('after 1 click width =', w1);
  await dp.screenshot({ path: 'screenshots/33_width_wide.png' });

  await dp.locator('#widthToggle').click();
  await dp.waitForTimeout(300);
  const w2 = await dp.locator('html').getAttribute('data-width');
  console.log('after 2 clicks width =', w2);

  await dp.locator('#widthToggle').click();
  await dp.waitForTimeout(300);
  await dp.locator('#tocCollapse').click();
  await dp.waitForTimeout(500);
  const tocState = await dp.locator('html').getAttribute('data-toc');
  console.log('after toc-collapse click, data-toc =', tocState);
  await dp.screenshot({ path: 'screenshots/34_toc_collapsed.png' });

  await dp.locator('#tocRail').click();
  await dp.waitForTimeout(500);
  const tocState2 = await dp.locator('html').getAttribute('data-toc');
  console.log('after toc-rail click, data-toc =', tocState2);

  const preEl = dp.locator('.article pre').first();
  await preEl.scrollIntoViewIfNeeded();
  await dp.waitForTimeout(200);
  await preEl.hover();
  await dp.waitForTimeout(300);
  await preEl.screenshot({ path: 'screenshots/35_copy_button_visible.png' });
  console.log('35_copy_button_visible.png');

  const copyBtn = preEl.locator('.copy-btn');
  await copyBtn.click();
  await dp.waitForTimeout(200);
  const copyLabel = await copyBtn.locator('.copy-label').textContent();
  console.log('after copy click, label =', copyLabel);
  await preEl.screenshot({ path: 'screenshots/36_copy_button_copied.png' });

  await desk.close();

  // ---- MOBILE ----
  const mob = await browser.newContext({ viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true });
  const mp = await mob.newPage();
  await mp.goto(url);
  await mp.screenshot({ path: 'screenshots/37_mobile_top.png' });
  console.log('37_mobile_top.png');

  const mCard = mp.locator('.source-card').first();
  await mCard.scrollIntoViewIfNeeded();
  await mp.waitForTimeout(300);
  await mCard.screenshot({ path: 'screenshots/38_mobile_source_card.png' });
  console.log('38_mobile_source_card.png');

  const mPre = mp.locator('.article pre').first();
  await mPre.scrollIntoViewIfNeeded();
  await mp.waitForTimeout(300);
  await mPre.screenshot({ path: 'screenshots/39_mobile_copy_btn.png' });
  console.log('39_mobile_copy_btn.png');

  await mob.close();
  await browser.close();
  console.log('\nAll captures done.');
})();
