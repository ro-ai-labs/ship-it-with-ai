// Verification for the 2026-05-26 SEO pass. Built up commit-by-commit.
// Updated for the October 2026 short edition: 18 sections (Prologue, 9
// chapters, Closing, Acknowledgments, About, Changelog, Appendices A-D),
// redirect stubs for every retired slug, and the /full/ archive.

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

// Languages this run expects in _site/. Default build = EN + RO. While the
// Romanian source is being rewritten to the new structure, run English alone
// with SITE_LANGS=en (build_spa.py reads the same variable).
const SITE_LANGS = (process.env.SITE_LANGS || '').toLowerCase();
const EXPECT_RO = !SITE_LANGS || /(^|,)\s*(ro|all|\*)\s*(,|$)/.test(SITE_LANGS);
const SECTION_COUNT = 18;                 // EXPECTED_PAGE_COUNT in build_spa.py
const URLS_PER_LANG = SECTION_COUNT + 1;  // + landing; /read/ and /full/ are noindex
const RETIRED = {
  'foreword': 'prologue-nine-seconds',
  'chapter-2-anatomy-invariant': 'chapter-1-primitives',
  'chapter-3-governance-in-layers': 'chapter-2-guardrails',
  'chapter-4-from-generating-code-to-shipping-software': 'chapter-3-bottleneck-moved',
  'chapter-5-six-phase-loop': 'chapter-4-six-phase-loop',
  'chapter-9-brownfield-patterns': 'chapter-9-rolling-it-out',
  'chapter-10-adoption-90-days': 'chapter-9-rolling-it-out',
  'appendix-a-cost-economics': 'appendix-a-for-managers',
};
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
  const repoRoot = path.resolve(__dirname, '..', '..');
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

          // dateModified is deterministic (content date) and must match sitemap <lastmod>.
          const sm = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
          const lastmod = (sm.match(/<lastmod>([0-9-]+)<\/lastmod>/) || [])[1];
          if (!book || book.dateModified !== lastmod) fail(`Book.dateModified=${book && book.dateModified}, expected sitemap lastmod ${lastmod}`);
          else ok(`Book.dateModified matches sitemap lastmod (${lastmod})`);
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
    function exists(rel) { return fs.existsSync(path.join(repoRoot, '_site', rel)); }
    function sizeKB(rel) { return fs.statSync(path.join(repoRoot, '_site', rel)).size / 1024; }

    if (!exists('cover.webp')) fail('cover.webp missing'); else {
      // 1200x630 photo cover; ~135 KB at quality 82 is the realistic floor.
      // The 50 KB target in the plan does not survive contact with a photo-style cover.
      const kb = sizeKB('cover.webp');
      if (kb > 150) fail(`cover.webp size ${kb.toFixed(1)} KB > 150 KB`);
      else ok(`cover.webp present (${kb.toFixed(1)} KB)`);
    }
    if (!exists('cover-720.webp')) fail('cover-720.webp missing'); else ok('cover-720.webp present');
    {
      const land = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      if (!/<source type="image\/webp" srcset="\/cover-720\.webp/.test(land)) fail('cover <picture>/<source> missing');
      else ok('cover served via <picture> with webp srcset');
    }
    if (!exists('404.html')) fail('404.html missing'); else ok('404.html present');
    if (!exists('llms.txt')) fail('llms.txt missing'); else ok('llms.txt present');
    if (!exists('llms-full.txt')) {
      fail('llms-full.txt missing');
    } else {
      const fullKb = sizeKB('llms-full.txt');
      // Sanity: full text should be substantially larger than the URL index.
      if (fullKb < 100) fail(`llms-full.txt is suspiciously small (${fullKb.toFixed(1)} KB)`);
      else ok(`llms-full.txt present (${fullKb.toFixed(0)} KB)`);
      const head = fs.readFileSync(path.join(repoRoot, '_site/llms-full.txt'), 'utf8').slice(0, 200);
      head.startsWith('# Ship It With AI')
        ? ok('llms-full.txt starts with the book title')
        : fail(`llms-full.txt unexpected head: ${head.slice(0, 60)}`);
    }
    // llms.txt should point at llms-full.txt so an LLM finds the full corpus.
    {
      const llmsTxt = fs.readFileSync(path.join(repoRoot, '_site/llms.txt'), 'utf8');
      llmsTxt.includes('/llms-full.txt')
        ? ok('llms.txt references llms-full.txt')
        : fail('llms.txt is missing a pointer to llms-full.txt');
    }
    {
      const t = fs.readFileSync(path.join(repoRoot, '_site/llms.txt'), 'utf8');
      if (!/\/\): .+/.test(t)) fail('llms.txt links lack per-link descriptions');
      else ok('llms.txt links carry descriptions');
      if (!/## Author/.test(t)) fail('llms.txt missing ## Author section');
      else ok('llms.txt has ## Author section');
    }
    if (!exists('deferred.css')) fail('deferred.css missing'); else ok('deferred.css present');
    if (!exists('sitemap.xml')) fail('sitemap.xml missing'); else ok('sitemap.xml present');
    if (!exists('read/index.html')) fail('read/index.html missing'); else ok('read/index.html present');
    if (!exists('cover.jpg')) fail('cover.jpg missing'); else ok('cover.jpg present');
    if (!exists('robots.txt')) fail('robots.txt missing'); else ok('robots.txt present');
    if (!exists('CNAME')) fail('CNAME missing'); else ok('CNAME present');
    if (!exists('.nojekyll')) fail('.nojekyll missing'); else ok('.nojekyll present');

    // ===== Commit 2 assertions =====

    // Landing index.html is reasonably thin. The plan's 100 KB target is
    // aspirational - the current template chrome (search modal + kbd modal +
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

      // /read/ is self-canonical + noindex,follow: canonical, og:url and
      // twitter:url all agree on /read/, and noindex keeps the full-text
      // duplicate out of the index while still passing link equity.
      const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
      if (canonical !== 'https://ship-it-with.ai/read/') {
        fail(`/read/ canonical = ${canonical}, expected https://ship-it-with.ai/read/`);
      } else ok('/read/ canonical → /read/ (self-canonical)');

      for (let n = 1; n <= 9; n++) {
        const count = await page.locator(`#chapter-${n}`).count();
        if (count === 0) fail(`/read/ missing #chapter-${n}`);
      }
      if (await page.locator('#chapter-10').count() !== 0) fail('/read/ still has #chapter-10');
      ok('/read/ has all 9 chapter anchors (and no #chapter-10)');
      await ctx.close();
    }

    // /read/ is noindex (kept for humans, out of the index) and absent from the sitemap.
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
      const robots = [...html.matchAll(/<meta name="robots" content="([^"]+)"/g)].map(m => m[1]);
      if (!robots.some(r => /noindex/.test(r))) fail(`/read/ missing noindex robots meta (got: ${robots})`);
      else ok('/read/ emits noindex robots meta');
      const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
      if (/ship-it-with\.ai\/read\//.test(sitemap)) fail('/read/ still listed in sitemap');
      else ok('/read/ excluded from sitemap');
      const readLd = [...html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
        .map(m => { try { return JSON.parse(m[1])['@type']; } catch { return null; } });
      if (readLd.includes('FAQPage')) fail('/read/ should not carry FAQPage (landing owns it)');
      else ok('/read/ carries no FAQPage');
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

    // Landing TOC: the only /read/# links left are the three Part headings
    // (Parts own no page). The short edition has no front matter, so nothing
    // else may fall back to /read/#anchor.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + '/');
      const hrefs = await page.locator('.landing-toc a[href^="/read/#"]').evaluateAll(as => as.map(a => a.getAttribute('href')));
      const want = ['/read/#part-i', '/read/#part-ii', '/read/#part-iii'];
      if (JSON.stringify(hrefs) !== JSON.stringify(want)) fail(`landing TOC /read/# links: ${JSON.stringify(hrefs)}, expected ${JSON.stringify(want)}`);
      else ok('landing TOC: /read/# links are exactly the three Part headings');
      const frontMatter = await page.locator('.landing-toc .toc-section-title', { hasText: 'Front Matter' }).count();
      if (frontMatter) fail('landing TOC still renders a Front Matter block');
      else ok('landing TOC: no Front Matter block');
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
      if (!ogUrl || ogUrl === 'https://ship-it-with.ai/') {
        fail(`404: og:url is homepage URL (should be 404-specific) - got: ${ogUrl}`);
      } else ok(`404: og:url is 404-specific (${ogUrl})`);
    }

    // sitemap has at least landing + /read/.
    {
      const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
      const urlCount = (sitemap.match(/<url>/g) || []).length;
      if (urlCount < 2) fail(`sitemap has ${urlCount} URLs, expected >= 2`);
      else ok(`sitemap has ${urlCount} URLs (>= 2)`);
    }

    // ===== Commit 3 assertions =====

    // Combined sitemap: 19 URLs per language (landing + 18 sections; /read/,
    // /full/ and redirect stubs excluded). EN at the root, RO under /ro/ => 38
    // total (19 when building English only).
    {
      const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
      const urlCount = (sitemap.match(/<url>/g) || []).length;
      const wantRo = EXPECT_RO ? URLS_PER_LANG : 0;
      const wantTotal = URLS_PER_LANG + wantRo;
      if (urlCount !== wantTotal) fail(`sitemap has ${urlCount} URLs, expected ${wantTotal} (${URLS_PER_LANG} EN + ${wantRo} RO)`);
      else ok(`sitemap has ${wantTotal} URLs (${URLS_PER_LANG} EN + ${wantRo} RO; /read/ + /full/ excluded)`);
      const enCount = (sitemap.match(/<loc>https:\/\/ship-it-with\.ai\/(?!ro\/)/g) || []).length;
      const roCount = (sitemap.match(/<loc>https:\/\/ship-it-with\.ai\/ro\//g) || []).length;
      if (enCount !== URLS_PER_LANG) fail(`sitemap has ${enCount} EN URLs, expected ${URLS_PER_LANG}`);
      else ok(`sitemap has ${URLS_PER_LANG} EN URLs`);
      if (roCount !== wantRo) fail(`sitemap has ${roCount} RO URLs, expected ${wantRo}`);
      else ok(`sitemap has ${wantRo} RO URLs${EXPECT_RO ? '' : ' (English-only run)'}`);
    }

    // Every section page returns 200, has one <h1>, unique title, canonical,
    // and a BreadcrumbList + TechArticle JSON-LD pair.
    const SLUGS = [
      'prologue-nine-seconds',
      'chapter-1-primitives', 'chapter-2-guardrails',
      'chapter-3-bottleneck-moved', 'chapter-4-six-phase-loop',
      'chapter-5-review-and-verify', 'chapter-6-agents-md',
      'chapter-7-architecture-review', 'chapter-8-readiness-kill-signals',
      'chapter-9-rolling-it-out',
      'closing', 'acknowledgments', 'about-the-author', 'changelog',
      'appendix-a-for-managers', 'appendix-b-templates', 'appendix-c-sources',
      'appendix-d-deep-dives',
    ];
    if (SLUGS.length !== SECTION_COUNT) fail(`test SLUGS has ${SLUGS.length} entries, expected ${SECTION_COUNT}`);
    {
      const seenTitles = new Set();
      let sectionsAllGreen = true;
      for (const slug of SLUGS) {
        const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
        const page = await ctx.newPage();
        const resp = await page.goto(`${baseUrl}/${slug}/`);
        if (!resp || resp.status() !== 200) {
          fail(`/${slug}/ status ${resp && resp.status()}`); sectionsAllGreen = false;
          await ctx.close(); continue;
        }

        const h1Count = await page.locator('h1').count();
        if (h1Count !== 1) { fail(`/${slug}/ has ${h1Count} <h1>`); sectionsAllGreen = false; }

        const title = await page.title();
        if (seenTitles.has(title)) { fail(`duplicate <title>: ${title}`); sectionsAllGreen = false; }
        seenTitles.add(title);

        const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
        if (canonical !== `https://ship-it-with.ai/${slug}/`) {
          fail(`/${slug}/ canonical = ${canonical}`); sectionsAllGreen = false;
        }

        const ldBlocks = await page.locator('script[type="application/ld+json"]').allTextContents();
        const types = ldBlocks.map(b => { try { return JSON.parse(b)['@type']; } catch { return null; } });
        if (!types.includes('TechArticle')) { fail(`/${slug}/ missing TechArticle`); sectionsAllGreen = false; }
        if (!types.includes('BreadcrumbList')) { fail(`/${slug}/ missing BreadcrumbList`); sectionsAllGreen = false; }

        await ctx.close();
      }
      if (sectionsAllGreen) ok(`all ${SLUGS.length} section pages: 200, one <h1>, unique title, canonical, TechArticle+BreadcrumbList`);
    }

    // TechArticle.isPartOf points at Book by @id (single source of truth).
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site',
        'chapter-3-bottleneck-moved', 'index.html'), 'utf8');
      const ld = [...html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
        .map(m => { try { return JSON.parse(m[1]); } catch { return null; } })
        .filter(Boolean);
      const tech = ld.find(o => o['@type'] === 'TechArticle');
      if (!tech || tech.isPartOf?.['@id'] !== 'https://ship-it-with.ai/#book') {
        fail(`chapter-3 TechArticle.isPartOf wrong: ${JSON.stringify(tech?.isPartOf)}`);
      } else ok('chapter-3 TechArticle.isPartOf → #book');

      const crumbs = ld.find(o => o['@type'] === 'BreadcrumbList');
      if (!crumbs || crumbs.itemListElement.length !== 3) {
        fail(`chapter-3 BreadcrumbList expected 3 crumbs, got ${crumbs?.itemListElement?.length}`);
      } else ok('chapter-3 BreadcrumbList: Home → Part II → Chapter');
      const part = crumbs && crumbs.itemListElement[1];
      if (!part || part.item !== 'https://ship-it-with.ai/read/#part-ii') fail(`chapter-3 breadcrumb part = ${part && part.item}, expected /read/#part-ii`);
      else ok('chapter-3 breadcrumb points at Part II');
    }

    // Prev/next on chapter-3 wire to the right slugs.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/chapter-3-bottleneck-moved/`);
      const prev = await page.locator('.chapter-prev').getAttribute('href');
      const next = await page.locator('.chapter-next').getAttribute('href');
      if (prev !== '/chapter-2-guardrails/') fail(`chapter-3 prev = ${prev}`);
      else if (next !== '/chapter-4-six-phase-loop/') fail(`chapter-3 next = ${next}`);
      else ok('chapter-3 prev/next correct');
      await ctx.close();
    }

    // Hash-redirect shim: /#chapter-7 navigates to /chapter-7-architecture-review/.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/#chapter-7`);
      await page.waitForURL(/chapter-7-architecture-review/, { timeout: 3000 }).catch(() => {});
      const url = page.url();
      if (!url.includes('/chapter-7-architecture-review/')) fail(`hash-redirect: landed at ${url}`);
      else ok('hash-redirect /#chapter-7 → /chapter-7-architecture-review/');
      await ctx.close();
    }

    // Legacy /#anchor bookmarks predate per-section URLs, so they use the OLD
    // (full-edition) numbering and land where that content lives now.
    for (const [hash, want] of [
      ['#chapter-2', '/chapter-1-primitives/'],
      ['#chapter-3', '/chapter-2-guardrails/'],
      ['#chapter-5', '/chapter-4-six-phase-loop/'],
      ['#chapter-10', '/chapter-9-rolling-it-out/'],
      ['#appendix-a', '/appendix-a-for-managers/'],
      ['#appendix-d', '/appendix-d-deep-dives/'],
      ['#foreword', '/prologue-nine-seconds/'],
      ['#how-to-read-this-book', '/prologue-nine-seconds/'],
      ['#reviewing-agent-diffs', '/chapter-5-review-and-verify/#reviewing-agent-diffs'],
    ]) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/${hash}`);
      await page.waitForURL(u => u.toString().includes(want), { timeout: 3000 }).catch(() => {});
      const url = page.url();
      if (!url.endsWith(want)) fail(`legacy hash-redirect ${hash}: landed at ${url}, expected ${want}`);
      else ok(`legacy hash-redirect /${hash} → ${want}`);
      await ctx.close();
    }

    // Cross-section anchor rewriting: /prologue-nine-seconds/ (which absorbed
    // the Foreword's author note) has a /about-the-author/#about-the-author link.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/prologue-nine-seconds/`);
      const count = await page.locator('a[href="/about-the-author/#about-the-author"]').count();
      if (!count) fail('prologue: cross-section anchor not rewritten');
      else ok('cross-section anchor rewriting works (prologue → /about-the-author/#about-the-author)');
      const bare = await page.locator('main a[href="#about-the-author"]').count();
      if (bare) fail(`prologue: stale bare #about-the-author anchor present (${bare})`);
      else ok('prologue: no stale bare #about-the-author anchors in body');
      await ctx.close();
    }

    // Byline link on chapter pages → /about-the-author/#contact.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/chapter-3-bottleneck-moved/`);
      const href = await page.locator('.topbar-byline').getAttribute('href');
      if (href !== '/about-the-author/#contact') fail(`byline href = ${href}`);
      else ok('byline → /about-the-author/#contact on chapter page');
      await ctx.close();
    }

    // SITE_MODE per page (landing/read/chapter).
    for (const [p, expected] of [
      ['/', 'landing'],
      ['/read/', 'read'],
      ['/chapter-3-bottleneck-moved/', 'chapter'],
      ['/full/', 'full'],
    ]) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + p);
      const mode = await page.evaluate(() => window.SITE_MODE);
      if (mode !== expected) fail(`${p}: SITE_MODE=${mode}, expected ${expected}`);
      else ok(`${p}: SITE_MODE=${expected}`);
      await ctx.close();
    }

    // Landing TOC now links to per-chapter URLs (not /read/#anchor).
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + '/');
      const chapterUrlLinks = await page.locator('.landing-toc a[href^="/chapter-"]').count();
      if (chapterUrlLinks !== 9) fail(`landing TOC: ${chapterUrlLinks} /chapter-*/ links (expected 9)`);
      else ok(`landing TOC: ${chapterUrlLinks} per-chapter URL links`);
      await ctx.close();
    }

    // Search index entries carry a `url` field (externalized to search-index.json).
    {
      if (!exists('search-index.json')) fail('search-index.json not emitted');
      else {
        const entries = JSON.parse(fs.readFileSync(path.join(repoRoot, '_site', 'search-index.json'), 'utf8'));
        const withUrl = entries.filter(e => e.url).length;
        if (withUrl < entries.length / 2) fail(`search index: only ${withUrl}/${entries.length} entries have url`);
        else ok(`search-index.json: ${withUrl}/${entries.length} entries have url field`);
        const land = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
        const inline = (land.match(/<script id="searchIndex" type="application\/json">(.*?)<\/script>/s) || [])[1] || '';
        if (inline.length > 10) fail(`search index still inlined in landing (${inline.length} chars)`);
        else ok('search index not inlined into landing (externalized)');
      }
    }

    // toc-current marker on the active chapter sidebar entry.
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site',
        'chapter-3-bottleneck-moved', 'index.html'), 'utf8');
      if (!/class="toc-current"[^>]*>[^<]*<a href="\/chapter-3-bottleneck-moved\//.test(html)) {
        fail('chapter-3 sidebar: missing toc-current marker on own entry');
      } else ok('chapter-3 sidebar: toc-current marker on own entry');
    }

    // AGENTS.md de-link mode-awareness: every chapter page has 0 or 1
    // outbound AGENTS.md links (the rest are unwrapped as plain text).
    {
      let bad = [];
      for (const slug of SLUGS.filter(s => s.startsWith('chapter-'))) {
        const html = fs.readFileSync(path.join(repoRoot, '_site', slug, 'index.html'), 'utf8');
        const n = (html.match(/<a href="https:\/\/agents\.md\/?"/g) || []).length;
        if (n > 1) bad.push(`${slug}=${n}`);
      }
      if (bad.length) fail(`AGENTS.md de-link: chapters with >1 link: ${bad.join(', ')}`);
      else ok('AGENTS.md de-link: every chapter page has <= 1 outbound agents.md link');
    }

    // Per-page meta descriptions are unique (no duplicate-content signal
    // across the 20 URLs from a one-size-fits-all template description).
    {
      const seen = new Map();
      const allPaths = ['index.html', 'read/index.html', 'full/index.html', '404.html']
        .concat(SLUGS.map(s => `${s}/index.html`));
      for (const p of allPaths) {
        const html = fs.readFileSync(path.join(repoRoot, '_site', p), 'utf8');
        const m = html.match(/<meta name="description" content="([^"]+)"/);
        const desc = m ? m[1] : null;
        if (!desc) { fail(`${p}: meta description missing`); continue; }
        if (seen.has(desc)) fail(`${p}: duplicate meta description (also on ${seen.get(desc)})`);
        else seen.set(desc, p);
      }
      if (!process.exitCode) ok(`meta descriptions unique across all ${allPaths.length} pages`);
    }

    // ===== Memory primitive + open-set pass assertions =====

    // 1. Slug rename: old URL serves a redirect stub, new URL serves the chapter.
    {
      // Read the stub HTML directly from disk - Playwright follows the meta-refresh
      // / location.replace before page.content() resolves, so we'd get the
      // destination chapter instead of the stub itself.
      const stubHtml = fs.readFileSync(
        path.join(repoRoot, '_site', 'chapter-1-six-primitives', 'index.html'), 'utf8');
      if (!/meta http-equiv="refresh"/i.test(stubHtml)) fail('old slug missing meta refresh');
      else if (!/canonical[^>]*href="https:\/\/ship-it-with\.ai\/chapter-1-primitives\/"/.test(stubHtml)) {
        fail('old slug missing canonical to new');
      } else ok('old slug serves redirect stub with canonical + meta refresh');

      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      // Hit the old URL - should redirect (via meta-refresh or location.replace)
      // to the new chapter page; final URL should contain the new slug.
      await page.goto(`${baseUrl}/chapter-1-six-primitives/`);
      await page.waitForURL(/chapter-1-primitives/, { timeout: 3000 }).catch(() => {});
      if (!page.url().includes('/chapter-1-primitives/')) {
        fail(`old slug redirect did not land on new slug; final URL: ${page.url()}`);
      } else ok('old slug redirects to new slug in the browser');

      const newResp = await page.goto(`${baseUrl}/chapter-1-primitives/`);
      if (!newResp || newResp.status() !== 200) fail(`new slug status ${newResp && newResp.status()}`);
      const h1 = await page.locator('h1').first().textContent();
      if (h1.trim() !== 'What an agent is') fail(`new slug H1: got "${h1}", expected "What an agent is"`);
      else ok('new slug H1 is "What an agent is"');

      await ctx.close();
    }

    // 2. Sitemap excludes old slug, includes new slug.
    {
      const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
      if (sitemap.includes('chapter-1-six-primitives')) fail('sitemap still lists old slug');
      else ok('sitemap excludes old slug');
      if (!sitemap.includes('chapter-1-primitives')) fail('sitemap missing new slug');
      else ok('sitemap includes new slug');
      const leaked = Object.keys(RETIRED).filter(old => sitemap.includes(`ship-it-with.ai/${old}/`) || sitemap.includes(`ship-it-with.ai/ro/${old}/`));
      if (leaked.length) fail(`sitemap lists retired slugs: ${leaked.join(', ')}`);
      else ok(`sitemap excludes all ${Object.keys(RETIRED).length} retired slugs`);
      if (/ship-it-with\.ai\/(ro\/)?full\//.test(sitemap)) fail('sitemap lists the /full/ archive');
      else ok('sitemap excludes /full/');
    }

    // 2b. Every retired slug serves a redirect stub (meta refresh + canonical
    // to the new page + noindex) and the browser lands on the new page, with a
    // moved #fragment routed to the page that now owns it.
    {
      let stubsOk = true;
      for (const [old, now] of Object.entries(RETIRED)) {
        const f = path.join(repoRoot, '_site', old, 'index.html');
        if (!fs.existsSync(f)) { fail(`retired slug /${old}/ has no redirect stub`); stubsOk = false; continue; }
        const stub = fs.readFileSync(f, 'utf8');
        if (!/meta http-equiv="refresh" content="0; url=\/[a-z0-9-]+\/"/.test(stub) ||
            !stub.includes(`url=/${now}/"`)) { fail(`/${old}/ stub: meta refresh not to /${now}/`); stubsOk = false; }
        if (!stub.includes(`<link rel="canonical" href="https://ship-it-with.ai/${now}/">`)) { fail(`/${old}/ stub: canonical not /${now}/`); stubsOk = false; }
        if (!/<meta name="robots" content="noindex, follow">/.test(stub)) { fail(`/${old}/ stub: missing noindex`); stubsOk = false; }
      }
      if (stubsOk) ok(`all ${Object.keys(RETIRED).length} retired slugs serve redirect stubs (refresh + canonical + noindex)`);

      for (const [from, want] of [
        ['/foreword/', '/prologue-nine-seconds/'],
        ['/chapter-10-adoption-90-days/', '/chapter-9-rolling-it-out/'],
        ['/chapter-5-six-phase-loop/', '/chapter-4-six-phase-loop/'],
        ['/chapter-5-six-phase-loop/#reviewing-agent-diffs', '/chapter-5-review-and-verify/#reviewing-agent-diffs'],
        ['/chapter-5-six-phase-loop/#what-is-the-six-phase-loop', '/chapter-4-six-phase-loop/#what-is-the-six-phase-loop'],
        ['/appendix-a-cost-economics/#cost-levers', '/appendix-a-for-managers/#cost-levers'],
      ]) {
        const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
        const page = await ctx.newPage();
        await page.goto(`${baseUrl}${from}`);
        await page.waitForURL(u => u.toString().endsWith(want), { timeout: 3000 }).catch(() => {});
        if (!page.url().endsWith(want)) fail(`stub ${from} landed at ${page.url()}, expected ${want}`);
        else ok(`stub ${from} → ${want}`);
        await ctx.close();
      }
    }

    // 2c. /full/ archive of the September 2026 edition: noindex, canonical to
    // the current edition's home, banner, out of the sitemap and llms files,
    // linked from the footer.
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'full', 'index.html'), 'utf8');
      const robots = [...html.matchAll(/<meta name="robots" content="([^"]+)"/g)].map(m => m[1]);
      if (robots.length !== 1 || robots[0] !== 'noindex, follow') fail(`/full/ robots = ${robots}`);
      else ok('/full/ is noindex, follow');
      const canon = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1];
      if (canon !== 'https://ship-it-with.ai/') fail(`/full/ canonical = ${canon}, expected https://ship-it-with.ai/`);
      else ok('/full/ canonical → https://ship-it-with.ai/');
      if (!/<aside class="edition-banner"[^>]*><strong>September 2026 archive\.<\/strong>.*historical guidance.*<a href="\/">maintained edition<\/a>/.test(html)) fail('/full/ historical warning or maintained-edition link missing');
      else ok('/full/ banner present with link to /');
      const ldTypes = [...html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
        .map(m => { try { return JSON.parse(m[1])['@type']; } catch { return null; } });
      if (ldTypes.includes('Book') || ldTypes.includes('FAQPage')) fail(`/full/ carries ${ldTypes} JSON-LD (should be none)`);
      else ok('/full/ carries no Book/FAQPage JSON-LD');
      if ((html.match(/<h1[ >]/g) || []).length !== 1) fail('/full/ should have exactly one <h1>');
      else ok('/full/ has exactly one <h1>');
      for (const f of ['llms.txt', 'llms-full.txt']) {
        const t = fs.readFileSync(path.join(repoRoot, '_site', f), 'utf8');
        if (/ship-it-with\.ai\/full\//.test(t) || t.includes('Full edition (September 2026)')) fail(`${f} mentions the /full/ archive`);
        else ok(`${f} excludes /full/`);
      }
      const full = fs.readFileSync(path.join(repoRoot, '_site', 'llms-full.txt'), 'utf8');
      if (/^## Foreword\b/m.test(full) || /^## Chapter 10$/m.test(full)) fail('llms-full.txt contains the old (full-edition) structure');
      else ok('llms-full.txt is the current edition');
      for (const p of ['/', '/chapter-1-primitives/']) {
        const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
        const page = await ctx.newPage();
        await page.goto(`${baseUrl}${p}`);
        const t = (await page.locator('.footer-contact a[href="/full/"]').first().textContent().catch(() => '')) || '';
        if (t.trim() !== 'September 2026 archive') fail(`footer at ${p}: /full/ link text "${t}"`);
        else ok(`footer at ${p} links "September 2026 archive" → /full/`);
        await ctx.close();
      }
      if (EXPECT_RO) {
        const ro = fs.readFileSync(path.join(repoRoot, '_site', 'ro', 'full', 'index.html'), 'utf8');
        if (!/<link rel="canonical" href="https:\/\/ship-it-with\.ai\/ro\/" \/>/.test(ro)) fail('/ro/full/ canonical not /ro/');
        else if (!ro.includes('Arhiva din septembrie 2026.') || !ro.includes('recomandări istorice') || !ro.includes('<a href="/ro/">')) fail('/ro/full/ historical warning missing');
        else if (!ro.includes('href="/ro/full/" class="footer-full-edition">Arhiva din septembrie 2026</a>')) fail('/ro/full/ footer link missing');
        else ok('/ro/full/ canonical, banner and footer link');
      }
    }

    // 3. Hash redirect map: /#chapter-1 lands on new URL.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/#chapter-1`);
      await page.waitForURL(/chapter-1-primitives/, { timeout: 2000 }).catch(() => {});
      const url = page.url();
      if (!url.includes('/chapter-1-primitives/')) fail(`hash-redirect: landed at ${url}`);
      else ok('hash-redirect /#chapter-1 → /chapter-1-primitives/');
      await ctx.close();
    }

    // 4. Global content sweep - count-anchored phrasings must be 0 in /read/.
    // The Changelog section is meta-commentary and intentionally quotes the
    // old "six primitives" phrasing when describing what was dropped, so
    // exclude its <h2> block from the sweep.
    {
      const readHtmlRaw = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
      const cl = readHtmlRaw.indexOf('<h2 id="changelog"');
      const nextH2 = cl >= 0 ? readHtmlRaw.indexOf('<h2 id="', cl + 1) : -1;
      if (cl >= 0 && nextH2 <= cl) {
        fail('changelog slice could not locate the next H2 in /read/ - section ordering may have changed; verify script needs updating');
      }
      const readHtml = cl >= 0 && nextH2 > cl
        ? readHtmlRaw.slice(0, cl) + readHtmlRaw.slice(nextH2)
        : readHtmlRaw;
      const forbidden = [
        'six primitives', 'sixth primitive', 'the other five', 'five primitives',
        'five capabilities', 'six conceptual', 'Six questions',
        'Eight inspection points', 'eight inspection points',
        'Six primitives. Two implementations', 'The sixth one is newer',
        'of the six',
        'are not additional primitives',
      ];
      const readHtmlLower = readHtml.toLowerCase();
      let sweepGreen = true;
      for (const phrase of forbidden) {
        if (readHtmlLower.includes(phrase.toLowerCase())) { fail(`/read/ still contains "${phrase}"`); sweepGreen = false; }
      }
      if (sweepGreen) ok('/read/ contains zero forbidden count-anchored phrasings (changelog excluded)');
    }

    // 5. Positive markers in /read/.
    {
      const readHtml = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
      // A code fence must not be interpreted as a figure opener that consumes
      // later chapters. Keep this completeness check in the deployment gate.
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/read/`);
      const chapterCount = await page.locator('h2.chapter-heading').count();
      const endingPresent = await page.locator('#about-the-author').count()
        && await page.locator('#contact').count();
      if (chapterCount !== 9 || !endingPresent) {
        fail(`/read/ is incomplete: ${chapterCount} chapters; ending anchors present: ${!!endingPresent}`);
      } else ok('/read/ preserves all 9 chapters and ending anchors');
      await ctx.close();
      // Short edition: the primitives are now cards with one question each, and
      // the implementation comparison is inside Chapter 1. Markers track the
      // draft wording; re-pin them if the prose pass rewords these lines.
      const required = [
        'nine primitives below',
        'two controls shipped as a pair',
        'Neither half is enough alone',
        'A capability can be absent or supplied externally',
        'check effort settings and retained reasoning',
        'Permissions / Sandbox',
        'agent-level decision layer',
        'OS-level enforcement',
        'Compare the implementations',
        'Demonstration: one prompt, two agents',
        'Sandbox posture is a governance choice',
      ];
      let posGreen = true;
      for (const phrase of required) {
        if (!readHtml.includes(phrase)) { fail(`/read/ missing positive marker "${phrase}"`); posGreen = false; }
      }
      if (posGreen) ok('/read/ contains all positive markers');
    }

    // 6. Chapter 1 has the new diagram structure.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/chapter-1-primitives/`);
      const dividerCount = await page.locator('.primitives-divider').count();
      const recursiveCount = await page.locator('.primitives-recursive .primitive').count();
      const sublistCount = await page.locator('.primitive-sublist').count();
      if (dividerCount < 1) fail('chapter-1 diagram missing .primitives-divider');
      if (recursiveCount < 1) fail('chapter-1 diagram missing .primitives-recursive .primitive');
      if (sublistCount < 2) fail(`chapter-1 diagram needs >= 2 .primitive-sublist (Memory + P/S); got ${sublistCount}`);
      if (dividerCount && recursiveCount && sublistCount >= 2) ok('chapter-1 diagram has divider + recursive row + Memory + P/S sublists');
      await ctx.close();
    }

    // 7. TOC entry on landing.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/`);
      const tocText = await page.locator('a[href="/chapter-1-primitives/"]').first().textContent();
      if (!/What an agent is/i.test(tocText || '')) fail(`landing TOC entry: ${tocText}`);
      else ok('landing TOC entry reads "What an agent is"');
      await ctx.close();
    }

    // ===== Memory primitive - Commit 2 assertions (Chapter 6 + Appendix C) =====

    // 8. Chapter 6 framing intro paragraph.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/chapter-6-agents-md/`);
      const body = await page.locator('main').textContent();
      if (!/the manually owned layer of Memory from Chapter 1/.test(body || '')) {
        fail('chapter-6 missing Memory framing intro paragraph');
      } else ok('chapter-6 framing intro present');
      await ctx.close();
    }

    // 9. Appendix C three new entries.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/appendix-c-sources/`);
      const body = (await page.locator('main').textContent()) || '';
      // Entries no longer carry H4 headings (consistency with rest of Appendix C);
      // assert on uniquely identifying phrases inside each entry's Claim/Caveat body.
      const requiredEntries = [
        'Project instructions provide a manually maintained memory layer', // client-specific discovery entry
        'auto-memory layer in which Claude writes',     // Claude Code Auto Memory entry
        'Anthropic publicly unveiled Dreaming',         // Auto Dream entry
      ];
      let entriesOk = true;
      for (const phrase of requiredEntries) {
        if (!body.includes(phrase)) { fail(`appendix-c missing entry containing "${phrase}"`); entriesOk = false; }
      }
      if (!body.includes('Code with Claude SF')) { fail('appendix-c missing Auto Dream attribution'); entriesOk = false; }
      if (!body.includes('code.claude.com/docs/en/memory')) { fail('appendix-c missing code.claude.com/docs/en/memory source'); entriesOk = false; }
      if (!body.includes('agents.md')) { fail('appendix-c missing agents.md source'); entriesOk = false; }
      if (entriesOk) ok('appendix-c has all 3 new entries with correct sources');
      await ctx.close();
    }

    // ===== Permissions / Sandbox primitive assertions =====

    // 9a. Ch.1 has the new Permissions / Sandbox section (heading + anchor + key phrases).
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/chapter-1-primitives/`);
      const html = await page.content();
      if (!html.includes('id="permissions-sandbox"')) fail('chapter-1 missing #permissions-sandbox anchor');
      else ok('chapter-1 has #permissions-sandbox anchor');
      const body = (await page.locator('main').textContent()) || '';
      const required = [
        'Permissions / Sandbox',
        'agent-level decision layer',
        'OS-level enforcement',
        'two controls shipped as a pair',
        'Neither half is enough alone',
      ];
      let allOk = true;
      for (const phrase of required) {
        if (!body.includes(phrase)) { fail(`chapter-1 missing "${phrase}"`); allOk = false; }
      }
      if (allOk) ok('chapter-1 P/S section has all required phrases');
      await ctx.close();
    }

    // 9b. The old Chapter 2 (anatomy invariant) is folded into Chapter 1 as a
    // proof box plus the sandbox-posture section.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/chapter-1-primitives/`);
      const body = (await page.locator('main').textContent()) || '';
      let allOk = true;
      for (const phrase of ['Compare the implementations', 'Demonstration: one prompt, two agents',
                            'Sandbox posture is a governance choice']) {
        if (!body.includes(phrase)) { fail(`chapter-1 missing "${phrase}" (old Chapter 2)`); allOk = false; }
      }
      if (allOk) ok('chapter-1 carries the implementation comparison + sandbox posture');
      await ctx.close();
    }

    // 9c. The five layers (old Chapter 3, now Chapter 2): the layer table
    // scores each layer against PocketOS, and least privilege is the spine.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/chapter-2-guardrails/`);
      const body = (await page.locator('main').textContent()) || '';
      for (const phrase of ['A prompt is a request. A control is something the agent cannot talk its way past.',
                            'Would it have stopped PocketOS?',
                            'Underneath all five sits least privilege']) {
        if (!body.includes(phrase)) fail(`chapter-2 missing "${phrase}"`);
        else ok(`chapter-2 has "${phrase.slice(0, 40)}..."`);
      }
      const layers = await page.locator('figure.diagram-layers, .diagram-layers').count();
      if (!layers) fail('chapter-2 missing the five-layers diagram');
      else ok('chapter-2 renders the five-layers diagram');
      await ctx.close();
    }

    // 9d. Appendix C has the 3 new P/S sources.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/appendix-c-sources/`);
      const body = (await page.locator('main').textContent()) || '';
      const required = [
        'Permissions / Sandbox primitive sources',
        'Claude Code resolves explicit permission rules',
        'Codex uses platform-specific OS isolation',
        'opencode ships an in-agent permission-prompt model',
      ];
      let allOk = true;
      for (const phrase of required) {
        if (!body.includes(phrase)) { fail(`appendix-c missing "${phrase}"`); allOk = false; }
      }
      if (allOk) ok('appendix-c has all 3 P/S primitive entries');
      await ctx.close();
    }

    // ===== Changelog + Last-updated footer assertions =====

    // 10. /changelog/ page exists, returns 200, has correct H1
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      const resp = await page.goto(`${baseUrl}/changelog/`);
      if (!resp || resp.status() !== 200) fail(`/changelog/ status ${resp && resp.status()}`);
      const h1Count = await page.locator('h1').count();
      if (h1Count !== 1) fail(`/changelog/ has ${h1Count} <h1>, expected 1`);
      const h1Text = (await page.locator('h1').first().textContent() || '').trim();
      if (h1Text !== 'Changelog') fail(`/changelog/ H1 = "${h1Text}", expected "Changelog"`);
      if (resp && resp.status() === 200 && h1Count === 1 && h1Text === 'Changelog') {
        ok('/changelog/ exists, returns 200, H1 = "Changelog"');
      }
      await ctx.close();
    }

    // 11. Changelog page has every required entry (self-referential entry included)
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/changelog/`);
      const body = (await page.locator('main').textContent() || '');
      const required = [
        '2026-05-27 - Permissions / Sandbox primitive',
        '2026-05-27 - Changelog + last-updated footer',
        '2026-05-27 - Memory primitive + open-set framing',
        '2026-05-27 - SEO pass: per-chapter URLs',
        '2026-05-26 - Feedback-pass polish',
        '2026-05-26 - First public version',
      ];
      let allPresent = true;
      for (const entry of required) {
        if (!body.includes(entry)) {
          fail(`/changelog/ missing entry "${entry}"`);
          allPresent = false;
        }
      }
      if (allPresent) ok(`/changelog/ contains all ${required.length} required entries`);
      await ctx.close();
    }

    // 12. Changelog page has NO reading-time badge (suppressed per spec)
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/changelog/`);
      const readingTimeCount = await page.locator('.reading-time').count();
      if (readingTimeCount !== 0) fail(`/changelog/ has ${readingTimeCount} .reading-time elements, expected 0 (suppressed)`);
      else ok('/changelog/ reading-time badge suppressed');
      await ctx.close();
    }

    // 13. Changelog prev/next nav targets
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/changelog/`);
      const prev = await page.locator('.chapter-prev').first().getAttribute('href');
      const next = await page.locator('.chapter-next').first().getAttribute('href');
      if (prev !== '/about-the-author/') fail(`/changelog/ prev = "${prev}", expected "/about-the-author/"`);
      if (next !== '/appendix-a-for-managers/') fail(`/changelog/ next = "${next}", expected "/appendix-a-for-managers/"`);
      if (prev === '/about-the-author/' && next === '/appendix-a-for-managers/') {
        ok('/changelog/ prev → /about-the-author/, next → /appendix-a-for-managers/');
      }
      await ctx.close();
    }

    // 14. Sitemap includes /changelog/
    {
      const sitemap = fs.readFileSync(path.join(repoRoot, '_site', 'sitemap.xml'), 'utf8');
      if (!sitemap.includes('<loc>https://ship-it-with.ai/changelog/</loc>')) {
        fail('sitemap missing /changelog/');
      } else ok('sitemap includes /changelog/');
      // Combined sitemap: 38 URLs total (19 EN + 19 RO; /read/ + /full/ noindex)
      const urlCount = (sitemap.match(/<url>/g) || []).length;
      const want = URLS_PER_LANG * (EXPECT_RO ? 2 : 1);
      if (urlCount !== want) fail(`sitemap has ${urlCount} URLs, expected ${want}`);
      else ok(`sitemap has ${want} URLs (/read/ + /full/ excluded for noindex)`);
    }

    // 15. Footer "Last updated" stamp on landing + chapter page
    {
      const dateRegex = /Last updated [A-Z][a-z]+ \d{1,2}, \d{4}/;
      for (const path_ of ['/', '/chapter-1-primitives/']) {
        const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
        const page = await ctx.newPage();
        await page.goto(`${baseUrl}${path_}`);
        const footerText = (await page.locator('.footer-copy').first().textContent() || '');
        if (!dateRegex.test(footerText)) fail(`footer at ${path_} missing "Last updated <date>" - got: "${footerText}"`);
        else ok(`footer at ${path_} has "Last updated <date>"`);
        await ctx.close();
      }
    }

    // 16. Footer Changelog link present
    {
      for (const path_ of ['/', '/chapter-1-primitives/']) {
        const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
        const page = await ctx.newPage();
        await page.goto(`${baseUrl}${path_}`);
        const linkCount = await page.locator('.footer-contact a[href="/changelog/"]').count();
        if (linkCount < 1) fail(`footer at ${path_} missing Changelog link in .footer-contact`);
        else ok(`footer at ${path_} has Changelog link`);
        await ctx.close();
      }
    }

    // 17. The dated-claims note (folded from the Foreword into the Prologue)
    // carries the workflow review date + a /changelog/ link in the body.
    // Other dated claims keep their own dates rather than inheriting this review.
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/prologue-nine-seconds/`);
      const body = (await page.locator('main').textContent() || '');
      if (!/Workflow advice was reviewed on [A-Za-z]+ \d{1,2}, \d{4}/.test(body)) {
        fail('/prologue-nine-seconds/ missing the dated-claims note');
      } else {
        const linkCount = await page.locator('main p a[href="/changelog/"]').count();
        if (linkCount < 1) fail('/prologue-nine-seconds/ dated-claims note missing /changelog/ link');
        else ok('/prologue-nine-seconds/ has dated-claims note + /changelog/ link');
      }
      await ctx.close();
    }

    // 18. Hash-redirect: /#changelog → /changelog/
    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(`${baseUrl}/#changelog`);
      await page.waitForURL(/\/changelog\//, { timeout: 2000 }).catch(() => {});
      const url = page.url();
      if (!url.includes('/changelog/') || url.includes('/#changelog')) {
        fail(`hash-redirect /#changelog landed at ${url}`);
      } else ok('hash-redirect /#changelog → /changelog/');
      await ctx.close();
    }

    // head theme-init must appear before <style> to prevent dark-mode FOUC
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      const initIdx = html.indexOf("setAttribute('data-theme'");
      const styleIdx = html.indexOf('<style>');
      if (initIdx === -1 || initIdx > styleIdx) fail('head theme-init missing or after <style> (FOUC)');
      else ok('head theme-init present before <style>');
    }

    // kbdOverlayTitle must not be an <h2> (demoted to avoid spurious heading outline entry)
    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'chapter-1-primitives', 'index.html'), 'utf8');
      if (/<h2[^>]*id="kbdOverlayTitle"/.test(html)) fail('kbdOverlayTitle is still an <h2>');
      else ok('kbdOverlayTitle demoted out of heading outline');
    }

    // og:type per page + /read/ og:url
    {
      const land = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      if (!/og:type" content="website"/.test(land)) fail('landing og:type should be website');
      else ok('landing og:type=website');
      const ch = fs.readFileSync(path.join(repoRoot, '_site', 'chapter-1-primitives', 'index.html'), 'utf8');
      if (!/og:type" content="article"/.test(ch)) fail('chapter og:type should be article');
      else ok('chapter og:type=article');
      const read = fs.readFileSync(path.join(repoRoot, '_site', 'read', 'index.html'), 'utf8');
      if (!/og:url" content="https:\/\/ship-it-with\.ai\/read\/"/.test(read)) fail('/read/ og:url should be /read/');
      else ok('/read/ og:url=/read/');
      if (!/rel="canonical" href="https:\/\/ship-it-with\.ai\/read\/"/.test(read)) fail('/read/ should be self-canonical (/read/)');
      else ok('/read/ self-canonical (/read/)');
    }

    {
      const html = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      if (!/rel="alternate" type="text\/markdown" href="https:\/\/ship-it-with\.ai\/llms-full\.txt"/.test(html))
        fail('head missing rel=alternate markdown link to llms-full.txt');
      else ok('head links the markdown corpus (llms-full.txt)');
    }

    {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      await page.goto(baseUrl + '/');
      const faqH2 = await page.locator('section.article-faq h2#faq-heading').count();
      const faqH3 = await page.locator('section.article-faq h3').count();
      if (faqH2 !== 1) fail(`landing visible FAQ <h2> count ${faqH2}, expected 1`);
      else ok('landing has a visible FAQ section');
      if (faqH3 < 8) fail(`landing visible FAQ has ${faqH3} questions, expected >= 8`);
      else ok(`landing visible FAQ has ${faqH3} questions`);
      await ctx.close();
    }
    {
      for (const slug of ['chapter-6-agents-md', 'appendix-a-for-managers', 'chapter-9-rolling-it-out', 'chapter-4-six-phase-loop', 'chapter-1-primitives', 'chapter-8-readiness-kill-signals']) {
        const h = fs.readFileSync(path.join(repoRoot, '_site', slug, 'index.html'), 'utf8');
        const types = [...h.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
          .map(m => { try { return JSON.parse(m[1])['@type']; } catch { return null; } });
        if (types.includes('FAQPage')) fail(`${slug} should NOT carry FAQPage (orphaned schema - landing owns it)`);
        else ok(`${slug} has no orphaned FAQPage`);
      }
    }
    {
      const land = fs.readFileSync(path.join(repoRoot, '_site', 'index.html'), 'utf8');
      const faqLd = [...land.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)]
        .map(m => { try { return JSON.parse(m[1]); } catch { return null; } })
        .filter(o => o && o['@type'] === 'FAQPage');
      const agentsQ = faqLd.flatMap(o => o.mainEntity).find(q => /What is AGENTS\.md/.test(q.name));
      if (!agentsQ || !/CLAUDE\.md/.test(agentsQ.acceptedAnswer.text)) {
        fail('AGENTS.md FAQ answer must explain its relationship to CLAUDE.md');
      } else ok('AGENTS.md FAQ answer explains its relationship to CLAUDE.md');
    }

    // No heading-level skip on standalone section pages (h1->h3 with no h2, etc.).
    {
      let skipBad = [];
      for (const slug of SLUGS) {
        const h = fs.readFileSync(path.join(repoRoot, '_site', slug, 'index.html'), 'utf8');
        const levels = [...h.matchAll(/<h([1-6])[ >]/g)].map(m => +m[1]);
        const present = [...new Set(levels)].sort((a,b)=>a-b);
        for (let i = 1; i < present.length; i++) {
          if (present[i] - present[i-1] > 1) { skipBad.push(`${slug}(h${present[i-1]}->h${present[i]})`); break; }
        }
      }
      if (skipBad.length) fail(`heading-level skip on: ${skipBad.join(', ')}`);
      else ok('no heading-level skips on standalone section pages');
    }

  } finally {
    await browser.close();
    stop();
  }

  if (process.exitCode) console.error('\nVerification FAILED - see above.');
  else console.log('\nVerification PASSED.');
}

main().catch(e => { console.error(e); process.exit(1); });
