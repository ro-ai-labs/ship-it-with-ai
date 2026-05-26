/**
 * Take verification screenshots of ship_it_with_ai.html
 * Usage: node screenshot_spa.js
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const FILE_URL = 'file://' + path.resolve(__dirname, 'ship_it_with_ai.html');
const OUTDIR = path.resolve(__dirname, 'screenshots');

if (!fs.existsSync(OUTDIR)) {
  fs.mkdirSync(OUTDIR, { recursive: true });
} else {
  // Clean prior screenshots so file sizes don't mislead
  fs.readdirSync(OUTDIR).forEach(f => {
    if (f.endsWith('.png')) fs.unlinkSync(path.join(OUTDIR, f));
  });
}

async function captureAt(page, selector, name) {
  const handle = await page.locator(selector).first();
  await handle.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  // Get the bounding box and capture a region around it
  const box = await handle.boundingBox();
  if (!box) {
    console.warn('⚠ no box for', selector);
    return;
  }
  // Capture viewport-sized screenshot at current scroll
  await page.screenshot({ path: path.join(OUTDIR, name), fullPage: false });
  console.log('✓', name);
}

(async () => {
  const browser = await chromium.launch();

  // ----- Desktop, light theme -----
  const desktopCtx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });
  const page = await desktopCtx.newPage();
  await page.goto(FILE_URL, { waitUntil: 'networkidle' });

  // Top of page
  await page.screenshot({ path: path.join(OUTDIR, '01_top.png'), fullPage: false });
  console.log('✓ 01_top.png');

  // 5 diagrams
  await captureAt(page, '.diagram-primitives', '02_diagram_primitives.png');
  await captureAt(page, '.diagram-layers', '03_diagram_layers.png');
  await captureAt(page, '.diagram-loop', '04_diagram_loop.png');
  await captureAt(page, '.diagram-traffic', '05_diagram_traffic.png');
  await captureAt(page, '.diagram-arc', '06_diagram_arc.png');

  // Action box
  await captureAt(page, '.action-box', '07_action_box.png');

  // Case note
  await captureAt(page, '.case-note', '08_case_note.png');

  // Epigraph
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(200);
  await page.locator('.epigraph').first().scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(OUTDIR, '09_epigraph.png'), fullPage: false });
  console.log('✓ 09_epigraph.png');

  // ----- Dark mode -----
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'dark');
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(OUTDIR, '10_dark_top.png'), fullPage: false });
  console.log('✓ 10_dark_top.png');

  await captureAt(page, '.diagram-primitives', '11_dark_primitives.png');
  await captureAt(page, '.diagram-traffic', '12_dark_traffic.png');
  await captureAt(page, '.action-box', '13_dark_action.png');

  await desktopCtx.close();

  // ----- Mobile (light) -----
  const mobileCtx = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
  });
  const m = await mobileCtx.newPage();
  await m.goto(FILE_URL, { waitUntil: 'networkidle' });
  await m.screenshot({ path: path.join(OUTDIR, '14_mobile_top.png'), fullPage: false });
  console.log('✓ 14_mobile_top.png');

  // Mobile menu open
  await m.locator('#menuToggle').click();
  await m.waitForTimeout(400);
  await m.screenshot({ path: path.join(OUTDIR, '15_mobile_menu_open.png'), fullPage: false });
  console.log('✓ 15_mobile_menu_open.png');

  // Close menu by tapping outside (click body in upper-right area)
  await m.mouse.click(380, 100);
  await m.waitForTimeout(400);

  // Mobile diagram
  await m.locator('.diagram-traffic').first().scrollIntoViewIfNeeded();
  await m.waitForTimeout(400);
  await m.screenshot({ path: path.join(OUTDIR, '16_mobile_diagram.png'), fullPage: false });
  console.log('✓ 16_mobile_diagram.png');

  await mobileCtx.close();
  await browser.close();

  console.log('\nAll screenshots saved to:', OUTDIR);
})();
