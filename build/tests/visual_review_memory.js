// Visual review of the Memory primitive update across viewports + themes.
// Loops mobile/tablet/desktop x light/dark, screenshots:
//   - chapter-1 diagram region (figure.diagram.diagram-primitives)
//   - chapter-1 Memory section (h3#memory + following viewport-height region)
//   - chapter-6 intro paragraph (top of /chapter-6-agents-md/)
//   - appendix-c "Memory primitive sources" section
// Saves to /tmp/memory-visual-review/

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:8765';
const OUT = '/tmp/memory-visual-review';

const VIEWPORTS = [
  { name: 'mobile',  width: 375,  height: 812 },
  { name: 'tablet',  width: 768,  height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
];
const THEMES = ['light', 'dark'];

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
  // Screenshot a viewport-height clip starting at the selector's top.
  const el = page.locator(selector).first();
  await el.waitFor({ state: 'visible', timeout: 5000 });
  await el.scrollIntoViewIfNeeded();
  // Scroll the heading near the very top of the viewport so the clip
  // starts at the heading itself, not 200px below it.
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

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();

  try {
    for (const vp of VIEWPORTS) {
      for (const theme of THEMES) {
        const tag = `${vp.name}_${theme}`;
        console.log(`\n=== ${tag} ===`);
        const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
        const page = await ctx.newPage();

        // ---- Chapter 1 (diagram + Memory section) ----
        await page.goto(`${BASE}/chapter-1-primitives/`);
        await setTheme(page, theme);
        // give web fonts a beat
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(200);

        // Diagram region
        await shotElement(
          page,
          'figure.diagram.diagram-primitives',
          path.join(OUT, `diagram_${tag}.png`)
        );

        // Memory section: clip viewport-height starting at h3#memory
        await shotRegionFromSelector(
          page,
          'h3#memory',
          path.join(OUT, `memory_${tag}.png`),
          vp.height
        );

        // ---- Chapter 6 intro ----
        await page.goto(`${BASE}/chapter-6-agents-md/`);
        await setTheme(page, theme);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(200);
        await shotTop(page, path.join(OUT, `ch6intro_${tag}.png`), vp.height);

        // ---- Appendix C Memory primitive sources ----
        await page.goto(`${BASE}/appendix-c-sources/`);
        await setTheme(page, theme);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(200);

        // Find the heading by text. It's likely an <h2> "Memory primitive sources".
        const headingHandle = await page.evaluateHandle(() => {
          const els = [...document.querySelectorAll('h2, h3, h4')];
          return els.find(e => /memory primitive sources/i.test(e.textContent)) || null;
        });
        const headingEl = headingHandle.asElement();
        if (!headingEl) {
          console.log('  WARN: "Memory primitive sources" heading not found on appendix-c');
        } else {
          // scroll it to top of viewport and clip viewport height + some
          await page.evaluate((el) => {
            const top = el.getBoundingClientRect().top + window.scrollY - 8;
            window.scrollTo(0, top);
          }, headingEl);
          await page.waitForTimeout(200);
          // Clip a bit more than vp.height so we likely catch the 3 cards
          const clipH = Math.min(vp.height + 600, 2400);
          await page.screenshot({
            path: path.join(OUT, `appendixC_${tag}.png`),
            clip: { x: 0, y: 0, width: vp.width, height: vp.height },
          });
          // Also a taller capture to inspect the cards together
          // Use fullPage=false but a custom clip is bounded by viewport, so
          // resize page to taller viewport for the long shot.
          console.log('  wrote', `appendixC_${tag}.png`);
        }

        await ctx.close();
      }
    }

    // Second pass for appendix-c: capture a TALLER viewport so we can see
    // the whole "Memory primitive sources" subsection with its 3 cards in one shot
    // (per-theme, desktop width only — we just need to inspect content).
    for (const theme of THEMES) {
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
      }
      await ctx.close();
    }

  } finally {
    await browser.close();
  }
})();
