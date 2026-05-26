const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve('ship_it_with_ai.html'));

  // Reading-time badges visible in sidebar
  await page.locator('.sidebar').screenshot({ path: 'screenshots/40_sidebar_with_times.png' });
  const timeCount = await page.locator('.toc-time').count();
  console.log('reading-time badges in DOM:', timeCount);

  // Open search via topbar trigger
  await page.locator('#searchTrigger').click();
  await page.waitForTimeout(300);
  await page.locator('#searchInput').fill('agents');
  await page.waitForTimeout(250);
  await page.screenshot({ path: 'screenshots/41_search_open.png' });
  const resultCount = await page.locator('.search-result').count();
  console.log('search results for "agents":', resultCount);

  // Press Esc to close
  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);

  // Cmd+K toggle
  await page.keyboard.down('Control');
  await page.keyboard.press('K');
  await page.keyboard.up('Control');
  await page.waitForTimeout(300);
  const overlayHidden = await page.locator('#searchOverlay').isHidden();
  console.log('after Ctrl+K, overlay hidden =', overlayHidden);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);

  // ? opens shortcuts help
  await page.keyboard.press('?');
  await page.waitForTimeout(300);
  const kbdHidden = await page.locator('#kbdOverlay').isHidden();
  console.log('after ?, kbd overlay hidden =', kbdHidden);
  await page.screenshot({ path: 'screenshots/42_kbd_help.png' });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);

  // Arrow right jumps to next chapter
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(200);
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(500);
  const scrollAfter = await page.evaluate(() => window.scrollY);
  console.log('after ArrowRight from top, scrollY =', scrollAfter);

  // Mobile pass
  await ctx.close();
  const mob = await browser.newContext({ viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true });
  const mp = await mob.newPage();
  await mp.goto('file://' + path.resolve('ship_it_with_ai.html'));
  await mp.locator('#searchTrigger').click();
  await mp.waitForTimeout(300);
  await mp.locator('#searchInput').fill('govern');
  await mp.waitForTimeout(250);
  await mp.screenshot({ path: 'screenshots/43_mobile_search.png' });
  const mResultCount = await mp.locator('.search-result').count();
  console.log('mobile search results for "govern":', mResultCount);

  await mob.close();
  await browser.close();
})();
