// Resume run: only does desktop_light appendix-c (partial), all desktop_dark,
// and the tall full-section appendix-c desktop screenshots.

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:8765';
const OUT = '/tmp/memory-visual-review';

async function setTheme(page, theme) {
  await page.evaluate((t) => {
    localStorage.setItem('theme', t);
    document.documentElement.setAttribute('data-theme', t);
  }, theme);
  await page.waitForTimeout(200);
}

async function shotElement(page, selector, file) {
  const el = page.locator(selector).first();
  await el.waitFor({ state: 'visible', timeout: 5000 });
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(150);
  await el.screenshot({ path: file });
  console.log('  wrote', path.basename(file));
}

async function shotRegionFromSelector(page, selector, file, vpHeight) {
  const el = page.locator(selector).first();
  await el.waitFor({ state: 'visible', timeout: 5000 });
  await el.scrollIntoViewIfNeeded();
  await page.evaluate((sel) => {
    const e = document.querySelector(sel);
    if (e) {
      const top = e.getBoundingClientRect().top + window.scrollY - 8;
      window.scrollTo(0, top);
    }
  }, selector);
  await page.waitForTimeout(200);
  await page.screenshot({
    path: file,
    clip: { x: 0, y: 0, width: page.viewportSize().width, height: vpHeight },
  });
  console.log('  wrote', path.basename(file));
}

async function shotTop(page, file, vpHeight) {
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(150);
  await page.screenshot({
    path: file,
    clip: { x: 0, y: 0, width: page.viewportSize().width, height: vpHeight },
  });
  console.log('  wrote', path.basename(file));
}

async function appendixCShot(page, vp, theme) {
  const headingHandle = await page.evaluateHandle(() => {
    const els = [...document.querySelectorAll('h2, h3, h4')];
    return els.find(e => /memory primitive sources/i.test(e.textContent)) || null;
  });
  const headingEl = headingHandle.asElement();
  if (!headingEl) {
    console.log('  WARN: heading not found');
    return;
  }
  await page.evaluate((el) => {
    const top = el.getBoundingClientRect().top + window.scrollY - 8;
    window.scrollTo(0, top);
  }, headingEl);
  await page.waitForTimeout(200);
  await page.screenshot({
    path: path.join(OUT, `appendixC_${vp.name}_${theme}.png`),
    clip: { x: 0, y: 0, width: vp.width, height: vp.height },
  });
  console.log(`  wrote appendixC_${vp.name}_${theme}.png`);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  try {
    // desktop_light appendix-c (missing)
    {
      const vp = { name: 'desktop', width: 1280, height: 800 };
      const theme = 'light';
      console.log(`=== resume desktop_light (appendix-c only) ===`);
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await ctx.newPage();
      await page.goto(`${BASE}/appendix-c-sources/`);
      await setTheme(page, theme);
      await page.waitForLoadState('networkidle').catch(() => {});
      await appendixCShot(page, vp, theme);
      await ctx.close();
    }

    // entire desktop_dark
    {
      const vp = { name: 'desktop', width: 1280, height: 800 };
      const theme = 'dark';
      console.log(`=== desktop_dark (all 4 shots) ===`);
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await ctx.newPage();

      await page.goto(`${BASE}/chapter-1-primitives/`);
      await setTheme(page, theme);
      await page.waitForLoadState('networkidle').catch(() => {});
      await shotElement(page, 'figure.diagram.diagram-primitives', path.join(OUT, `diagram_desktop_dark.png`));
      await shotRegionFromSelector(page, 'h3#memory', path.join(OUT, `memory_desktop_dark.png`), vp.height);

      await page.goto(`${BASE}/chapter-6-agents-md/`);
      await setTheme(page, theme);
      await page.waitForLoadState('networkidle').catch(() => {});
      await shotTop(page, path.join(OUT, `ch6intro_desktop_dark.png`), vp.height);

      await page.goto(`${BASE}/appendix-c-sources/`);
      await setTheme(page, theme);
      await page.waitForLoadState('networkidle').catch(() => {});
      await appendixCShot(page, vp, theme);

      await ctx.close();
    }

    // full appendix C captures (tall viewport)
    for (const theme of ['light', 'dark']) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 2200 } });
      const page = await ctx.newPage();
      await page.goto(`${BASE}/appendix-c-sources/`);
      await setTheme(page, theme);
      await page.waitForLoadState('networkidle').catch(() => {});
      const headingHandle = await page.evaluateHandle(() => {
        const els = [...document.querySelectorAll('h2, h3, h4')];
        return els.find(e => /memory primitive sources/i.test(e.textContent)) || null;
      });
      const headingEl = headingHandle.asElement();
      if (headingEl) {
        await page.evaluate((el) => {
          const top = el.getBoundingClientRect().top + window.scrollY - 8;
          window.scrollTo(0, top);
        }, headingEl);
        await page.waitForTimeout(200);
        await page.screenshot({
          path: path.join(OUT, `appendixC_full_desktop_${theme}.png`),
          clip: { x: 0, y: 0, width: 1280, height: 2000 },
        });
        console.log(`  wrote appendixC_full_desktop_${theme}.png`);
      } else {
        console.log('  WARN: heading not found in full pass');
      }
      await ctx.close();
    }

  } finally {
    await browser.close();
  }
})();
