// Visual review of the Permissions / Sandbox primitive update across viewports + themes.
// Captures:
//   - chapter-1 diagram region (figure.diagram.diagram-primitives)
//   - chapter-1 Permissions / Sandbox section (#permissions-sandbox)
//   - chapter-3 framing paragraph (the "Three of these five layers" text)
//   - appendix-c "Permissions / Sandbox primitive sources" group
// Saves to /tmp/ps-visual-review/

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:8781';
const OUT = '/tmp/ps-visual-review';

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

async function injectThemeInit(ctx, theme) {
  // Set the theme in localStorage and on <html> before any page script runs.
  await ctx.addInitScript((t) => {
    try { localStorage.setItem('theme', t); } catch (e) {}
    document.documentElement.setAttribute('data-theme', t);
  }, theme);
}

async function shotElement(page, selector, file) {
  const el = page.locator(selector).first();
  await el.waitFor({ state: 'visible', timeout: 5000 });
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(150);
  await el.screenshot({ path: file });
  console.log('  wrote', path.basename(file));
}

async function shotRegionFromSelector(page, selector, file) {
  const el = page.locator(selector).first();
  await el.waitFor({ state: 'visible', timeout: 5000 });
  await el.scrollIntoViewIfNeeded();
  await page.evaluate((sel) => {
    const e = document.querySelector(sel);
    if (e) {
      const top = e.getBoundingClientRect().top + window.scrollY - 8;
      window.scrollTo({ top, behavior: 'instant' });
    }
  }, selector);
  await page.waitForTimeout(200);
  // Use viewport screenshot (no clip) so it captures the currently visible area,
  // not a clip from absolute page y=0.
  await page.screenshot({ path: file, fullPage: false });
  console.log('  wrote', path.basename(file));
}

async function shotRegionFromTextMatch(page, regex, file) {
  const handle = await page.evaluateHandle((re) => {
    const reObj = new RegExp(re, 'i');
    const els = [...document.querySelectorAll('h1, h2, h3, h4, p, li')];
    return els.find((e) => reObj.test(e.textContent)) || null;
  }, regex.source);
  const el = handle.asElement();
  if (!el) {
    console.log('  WARN: no element matching', regex);
    return;
  }
  await page.evaluate((e) => {
    const top = e.getBoundingClientRect().top + window.scrollY - 8;
    window.scrollTo({ top, behavior: 'instant' });
  }, el);
  await page.waitForTimeout(200);
  await page.screenshot({ path: file, fullPage: false });
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
        await injectThemeInit(ctx, theme);
        const page = await ctx.newPage();

        // ---- Chapter 1: diagram + P/S section ----
        await page.goto(`${BASE}/chapter-1-primitives/`);
        await setTheme(page, theme);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(200);

        await shotElement(
          page,
          'figure.diagram.diagram-primitives',
          path.join(OUT, `diagram_${tag}.png`)
        );

        await shotRegionFromSelector(
          page,
          'h3#permissions-sandbox',
          path.join(OUT, `pssection_${tag}.png`)
        );

        // ---- Chapter 3 framing paragraph ----
        await page.goto(`${BASE}/chapter-3-governance-in-layers/`);
        await setTheme(page, theme);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(200);
        await shotRegionFromTextMatch(
          page,
          /Three of these five layers/,
          path.join(OUT, `ch3framing_${tag}.png`)
        );

        // ---- Appendix C: P/S primitive sources group ----
        await page.goto(`${BASE}/appendix-c-sources/`);
        await setTheme(page, theme);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(200);

        const headingHandle = await page.evaluateHandle(() => {
          const els = [...document.querySelectorAll('h2, h3, h4')];
          return els.find(e => /permissions \/ sandbox primitive sources/i.test(e.textContent)) || null;
        });
        const headingEl = headingHandle.asElement();
        if (!headingEl) {
          console.log('  WARN: "Permissions / Sandbox primitive sources" heading not found');
        } else {
          await page.evaluate((el) => {
            const top = el.getBoundingClientRect().top + window.scrollY - 8;
            window.scrollTo({ top, behavior: 'instant' });
          }, headingEl);
          await page.waitForTimeout(200);
          await page.screenshot({
            path: path.join(OUT, `appendixC_${tag}.png`),
            fullPage: false,
          });
          console.log('  wrote', `appendixC_${tag}.png`);
        }

        await ctx.close();
      }
    }

    // Second pass: a taller desktop shot capturing the entire P/S sources group
    for (const theme of THEMES) {
      // Use a moderately-tall viewport (not 2400, which is taller than the document
      // — the browser caps scrollY at docHeight - viewportHeight, leaving the
      // target heading way above the top edge).
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 1400 } });
      await injectThemeInit(ctx, theme);
      const page = await ctx.newPage();
      await page.goto(`${BASE}/appendix-c-sources/`);
      await setTheme(page, theme);
      await page.waitForLoadState('networkidle').catch(() => {});
      const headingHandle = await page.evaluateHandle(() => {
        const els = [...document.querySelectorAll('h2, h3, h4')];
        return els.find(e => /permissions \/ sandbox primitive sources/i.test(e.textContent)) || null;
      });
      const headingEl = headingHandle.asElement();
      if (headingEl) {
        await page.evaluate((el) => {
          const top = el.getBoundingClientRect().top + window.scrollY - 8;
          window.scrollTo({ top, behavior: 'instant' });
        }, headingEl);
        await page.waitForTimeout(200);
        await page.screenshot({
          path: path.join(OUT, `appendixC_full_desktop_${theme}.png`),
          fullPage: false,
        });
        console.log(`  wrote appendixC_full_desktop_${theme}.png`);
      }
      await ctx.close();
    }

    // Third pass: also a taller desktop shot of the Ch.1 P/S section so we can
    // see both halves of the prose (decision layer + OS enforcement + "Said plainly").
    for (const theme of THEMES) {
      // Use a moderately-tall viewport (not 2400, which is taller than the document
      // — the browser caps scrollY at docHeight - viewportHeight, leaving the
      // target heading way above the top edge).
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 1400 } });
      await injectThemeInit(ctx, theme);
      const page = await ctx.newPage();
      await page.goto(`${BASE}/chapter-1-primitives/`);
      await setTheme(page, theme);
      await page.waitForLoadState('networkidle').catch(() => {});
      await page.evaluate(() => {
        const e = document.querySelector('h3#permissions-sandbox');
        if (e) {
          const top = e.getBoundingClientRect().top + window.scrollY - 8;
          window.scrollTo({ top, behavior: 'instant' });
        }
      });
      await page.waitForTimeout(200);
      await page.screenshot({
        path: path.join(OUT, `pssection_full_desktop_${theme}.png`),
        fullPage: false,
      });
      console.log(`  wrote pssection_full_desktop_${theme}.png`);
      await ctx.close();
    }

  } finally {
    await browser.close();
  }
})();
