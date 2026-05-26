const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, isMobile: false });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve('ship_it_with_ai.html'));
  await page.waitForTimeout(600);

  const result = await page.evaluate(() => {
    const vw = window.innerWidth;
    const docW = document.documentElement.scrollWidth;
    const bodyW = document.body.scrollWidth;
    const offenders = [];
    document.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.right > vw + 1 || r.width > vw + 1) {
        const desc = `<${el.tagName.toLowerCase()}${el.className ? '.' + el.className.split(' ').slice(0,3).join('.') : ''}${el.id ? '#'+el.id : ''}>`;
        offenders.push({ el: desc, width: Math.round(r.width), right: Math.round(r.right), text: (el.textContent || '').slice(0, 50).replace(/\s+/g, ' ').trim() });
      }
    });
    return { viewport: vw, documentScrollWidth: docW, bodyScrollWidth: bodyW, offenderCount: offenders.length, topOffenders: offenders.slice(0, 20) };
  });
  console.log(JSON.stringify(result, null, 2));

  await browser.close();
})();
