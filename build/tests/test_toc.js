const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const url = 'file://' + path.resolve('ship_it_with_ai.html');
  await page.goto(url);

  const tocLinks = page.locator('.sidebar a[href^="#"]');
  const count = await tocLinks.count();
  console.log(`TOC anchor links found: ${count}`);

  let missing = 0;
  for (let i = 0; i < count; i++) {
    const link = tocLinks.nth(i);
    const href = await link.getAttribute('href');
    const text = (await link.textContent()).trim();
    const id = href.slice(1);
    const target = page.locator(`#${id}`).first();
    const targetCount = await target.count();
    if (targetCount === 0) {
      console.log(`  MISSING TARGET: "${text}" -> ${href}`);
      missing++;
    }
  }
  console.log(`Missing targets: ${missing}`);

  const partI = page.locator('a[href="#part-i"]').first();
  if (await partI.count() > 0) {
    await partI.click();
    await page.waitForTimeout(800);
    const partIHeading = page.locator('#part-i');
    const box = await partIHeading.boundingBox();
    console.log(`After click on #part-i: heading bounding box=${JSON.stringify(box)}`);
  } else {
    console.log('  Part I link NOT FOUND in TOC');
  }

  await browser.close();
})();
