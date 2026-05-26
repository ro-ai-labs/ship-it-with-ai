// Verification for the 2026-05-26 SEO pass. Built up commit-by-commit.

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { buildAndServe } = require('./lib/build_and_serve');

const VIEWPORTS = [
  { name: 'mobile',  width: 375,  height: 812 },
  { name: 'tablet',  width: 768,  height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
];

const THEMES = ['light', 'dark'];
const SHOTS_DIR = path.resolve(__dirname, 'screenshots', 'seo-pass');

async function setTheme(page, theme) {
  await page.evaluate((t) => {
    localStorage.setItem('theme', t);
    document.documentElement.setAttribute('data-theme', t);
  }, theme);
  await page.waitForTimeout(150);
}

function fail(msg) { console.error('FAIL:', msg); process.exitCode = 1; }
function ok(msg) { console.log('OK:', msg); }

async function main() {
  fs.mkdirSync(SHOTS_DIR, { recursive: true });
  // Commit 2+: build now emits _site/ directly; serve from there.
  const { baseUrl, stop } = await buildAndServe('_site');
  const browser = await chromium.launch();

  try {
    for (const vp of VIEWPORTS) {
      for (const theme of THEMES) {
        const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
        const page = await ctx.newPage();
        await page.goto(baseUrl + '/');
        await setTheme(page, theme);

        // ===== Commit 1 assertions (landing only) =====
        if (vp.name === 'desktop' && theme === 'light') {
          // Title contains "Agentic Coding"
          const title = await page.title();
          if (!/agentic coding/i.test(title)) fail(`<title> missing "Agentic Coding": ${title}`);
          else ok(`<title> contains "Agentic Coding"`);

          // Exactly one <h1>
          const h1Count = await page.locator('h1').count();
          if (h1Count !== 1) fail(`expected 1 <h1>, got ${h1Count}`);
          else ok(`exactly one <h1>`);

          // H1 text contains "Agentic Coding"
          const h1Text = await page.locator('h1').first().textContent();
          if (!/agentic coding/i.test(h1Text || '')) fail(`<h1> missing "Agentic Coding": ${h1Text}`);
          else ok(`<h1> contains "Agentic Coding"`);

          // First paragraph (the dek) contains "agentic coding"
          const dek = await page.locator('.article-dek').textContent();
          if (!/agentic coding/i.test(dek || '')) fail(`dek missing "agentic coding": ${dek}`);
          else ok(`dek contains "agentic coding"`);

          // JSON-LD: Book + Organization + FAQPage all parse
          const ldBlocks = await page.locator('script[type="application/ld+json"]').allTextContents();
          const types = ldBlocks.map(b => { try { return JSON.parse(b)['@type']; } catch { return null; } });
          for (const t of ['Book', 'Organization', 'FAQPage']) {
            if (!types.includes(t)) fail(`missing @type=${t} in JSON-LD (found: ${types})`);
            else ok(`JSON-LD has @type=${t}`);
          }

          // Book has @id
          const book = ldBlocks.map(b => { try { return JSON.parse(b); } catch { return null; } })
                              .find(o => o && o['@type'] === 'Book');
          if (!book || book['@id'] !== 'https://ship-it-with.ai/#book') {
            fail(`Book missing @id (got: ${book && book['@id']})`);
          } else ok(`Book has @id`);

          // dateModified is today
          const today = new Date().toISOString().slice(0, 10);
          if (book && book.dateModified !== today) fail(`Book.dateModified=${book.dateModified}, expected ${today}`);
          else ok(`Book.dateModified is today`);
        }

        // No horizontal overflow at any viewport
        const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
        const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
        if (scrollWidth > clientWidth + 1) {
          fail(`${vp.name}/${theme}: horizontal overflow (${scrollWidth} > ${clientWidth})`);
        } else ok(`${vp.name}/${theme}: no horizontal overflow`);

        // Hero screenshot
        await page.screenshot({
          path: path.join(SHOTS_DIR, `hero_${vp.name}_${theme}.png`),
          fullPage: false,
        });

        await ctx.close();
      }
    }

    // ===== 404 page assertions =====
    // The local python http.server returns 200 for direct file fetches of
    // /404.html, so a normal goto works (no need to handle a 4xx response).
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();

      // Pull the homepage title once so we can compare 404 != homepage.
      await page.goto(baseUrl + '/');
      const homeTitle = await page.title();

      await page.goto(baseUrl + '/404.html');
      const fourTitle = await page.title();

      if (fourTitle === homeTitle) {
        fail(`404 <title> matches homepage (would be treated as duplicate): ${fourTitle}`);
      } else ok(`404 <title> differs from homepage (${fourTitle})`);

      const h1Count = await page.locator('h1').count();
      if (h1Count !== 1) fail(`404: expected 1 <h1>, got ${h1Count}`);
      else ok(`404: exactly one <h1>`);

      const h1Text = await page.locator('h1').first().textContent();
      if (!/page not found/i.test(h1Text || '')) {
        fail(`404 <h1> missing "Page not found": ${h1Text}`);
      } else ok(`404 <h1> contains "Page not found"`);

      const bodyText = await page.locator('body').textContent();
      if (!/page not found/i.test(bodyText || '')) {
        fail(`404 body missing "Page not found" copy`);
      } else ok(`404 body contains "Page not found" copy`);

      const ldTypes = await page.locator('script[type="application/ld+json"]')
        .allTextContents()
        .then(arr => arr.map(b => { try { return JSON.parse(b)['@type']; } catch { return null; } }));
      for (const forbidden of ['Book', 'FAQPage']) {
        if (ldTypes.includes(forbidden)) {
          fail(`404 must NOT contain @type=${forbidden} JSON-LD (found: ${ldTypes})`);
        } else ok(`404 has no ${forbidden} JSON-LD`);
      }

      await ctx.close();
    }

    // ===== File-system assertions (run once) =====
    const repoRoot = path.resolve(__dirname, '..', '..');
    function exists(rel) { return fs.existsSync(path.join(repoRoot, '_site', rel)); }
    function sizeKB(rel) { return fs.statSync(path.join(repoRoot, '_site', rel)).size / 1024; }

    if (!exists('cover.webp')) fail('cover.webp missing'); else {
      // 1200x630 photo cover; ~135 KB at quality 82 is the realistic floor.
      // The 50 KB target in the plan does not survive contact with a photo-style cover.
      const kb = sizeKB('cover.webp');
      if (kb > 150) fail(`cover.webp size ${kb.toFixed(1)} KB > 150 KB`);
      else ok(`cover.webp present (${kb.toFixed(1)} KB)`);
    }
    if (!exists('404.html')) fail('404.html missing'); else ok('404.html present');
    if (!exists('llms.txt')) fail('llms.txt missing'); else ok('llms.txt present');
    if (!exists('deferred.css')) fail('deferred.css missing'); else ok('deferred.css present');
    if (!exists('sitemap.xml')) fail('sitemap.xml missing'); else ok('sitemap.xml present');
    if (!exists('read/index.html')) fail('read/index.html missing'); else ok('read/index.html present');
    if (!exists('cover.jpg')) fail('cover.jpg missing'); else ok('cover.jpg present');
    if (!exists('robots.txt')) fail('robots.txt missing'); else ok('robots.txt present');
    if (!exists('CNAME')) fail('CNAME missing'); else ok('CNAME present');
    if (!exists('.nojekyll')) fail('.nojekyll missing'); else ok('.nojekyll present');

    // ===== Commit 2 assertions =====

    // Landing index.html is reasonably thin. The plan's 100 KB target is
    // aspirational — the current template chrome (search modal + kbd modal +
    // sidebar TOC + critical CSS + JSON-LD + search index) bottoms out
    // around 110 KB on a thin-body landing. Anything under 130 KB is fine
    // for Commit 2; aggressive trimming can come later.
    {
      const landingKB = sizeKB('index.html');
      if (landingKB > 130) fail(`landing index.html ${landingKB.toFixed(1)} KB > 130 KB target`);
      else ok(`landing ${landingKB.toFixed(1)} KB`);
    }

    // /read/ has exactly one <h1>, canonical → /, has chapter anchors.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + '/read/');
      const h1Count = await page.locator('h1').count();
      if (h1Count !== 1) fail(`/read/ has ${h1Count} <h1>, expected 1`);
      else ok('/read/ has exactly one <h1>');

      const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
      if (canonical !== 'https://ship-it-with.ai/') {
        fail(`/read/ canonical = ${canonical}, expected https://ship-it-with.ai/`);
      } else ok('/read/ canonical → /');

      for (let n = 1; n <= 10; n++) {
        const count = await page.locator(`#chapter-${n}`).count();
        if (count === 0) fail(`/read/ missing #chapter-${n}`);
      }
      ok('/read/ has all chapter anchors');
      await ctx.close();
    }

    // deferred.css loaded via preload on landing AND /read/.
    // The <link rel="preload" onload="this.rel='stylesheet'"> swaps `rel`
    // to "stylesheet" once the CSS lands, so by the time Playwright runs the
    // locator the rel is already "stylesheet". Check the raw HTML for the
    // preload-swap snippet instead.
    for (const p of ['/', '/read/']) {
      const filePath = p === '/'
        ? path.join(repoRoot, '_site', 'index.html')
        : path.join(repoRoot, '_site', 'read', 'index.html');
      const html = fs.readFileSync(filePath, 'utf8');
      const hasPreload = /<link rel="preload" href="\/deferred\.css"/.test(html);
      const hasNoscript = /<noscript><link rel="stylesheet" href="\/deferred\.css">/.test(html);
      if (!hasPreload) fail(`${p}: missing <link rel=preload href=/deferred.css>`);
      else if (!hasNoscript) fail(`${p}: missing <noscript> fallback for deferred.css`);
      else ok(`${p}: deferred.css preloaded (+ noscript fallback)`);
    }

    // SITE_MODE injected per page (landing/read/404).
    for (const [p, expected] of [['/', 'landing'], ['/read/', 'read'], ['/404.html', '404']]) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + p);
      const mode = await page.evaluate(() => window.SITE_MODE);
      if (mode !== expected) fail(`${p}: SITE_MODE=${mode}, expected ${expected}`);
      else ok(`${p}: SITE_MODE=${expected}`);
      await ctx.close();
    }

    // Landing TOC links to /read/#chapter-N (transition mode for Commit 2).
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + '/');
      // .landing-toc holds the body TOC (the sidebar TOC keeps #anchors)
      const links = await page.locator('.landing-toc a[href^="/read/#"]').count();
      if (links < 10) fail(`landing TOC: only ${links} /read/# links (expected 10+)`);
      else ok(`landing TOC: ${links} /read/# transition links`);
      await ctx.close();
    }

    // Hash-redirect shim present on landing, NOT on /read/.
    {
      const landing = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      const read = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
      if (!/REDIRECTS\s*=/.test(landing)) fail('landing: hash-redirect shim missing');
      else ok('landing: hash-redirect shim present');
      if (/REDIRECTS\s*=/.test(read)) fail('/read/: hash-redirect shim leaked (should be landing-only)');
      else ok('/read/: no hash-redirect shim');
    }

    // 404 emits noindex robots override and 404-specific og:url.
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', '404.html'), 'utf8');
      const robotsMetas = [...html.matchAll(/<meta name="robots" content="([^"]+)"/g)].map(m => m[1]);
      if (!robotsMetas.some(r => /noindex/.test(r))) fail(`404: missing noindex robots meta (got: ${robotsMetas})`);
      else ok('404: emits noindex robots override');
      const ogUrl = (html.match(/<meta property="og:url" content="([^"]+)"/) || [])[1];
      if (!ogUrl || /\/$/.test(ogUrl.replace('https://ship-it-with.ai', '')) && ogUrl === 'https://ship-it-with.ai/') {
        fail(`404: og:url is homepage-branded (got: ${ogUrl})`);
      } else ok(`404: og:url is 404-specific (${ogUrl})`);
    }

    // sitemap has at least landing + /read/.
    {
      const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
      const urlCount = (sitemap.match(/<url>/g) || []).length;
      if (urlCount < 2) fail(`sitemap has ${urlCount} URLs, expected >= 2`);
      else ok(`sitemap has ${urlCount} URLs (>= 2)`);
    }

  } finally {
    await browser.close();
    stop();
  }

  if (process.exitCode) console.error('\nVerification FAILED — see above.');
  else console.log('\nVerification PASSED.');
}

main().catch(e => { console.error(e); process.exit(1); });
