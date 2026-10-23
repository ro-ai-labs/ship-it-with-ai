// Verification for the 2026-05-26 feedback pass (updated for the October 2026
// short edition: new chapter format on /read/, old-format renderers on /full/).
// Runs the build, then opens the generated index.html across viewports + themes,
// asserts feature presence, and saves screenshots.

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { buildAndUrl } = require('./lib/build_and_open');

const VIEWPORTS = [
  { name: 'mobile',  width: 375,  height: 812 },
  { name: 'tablet',  width: 768,  height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
];

const THEMES = ['light', 'dark'];

const SHOTS_DIR = path.resolve(__dirname, 'screenshots', 'feedback-pass');

async function setTheme(page, theme) {
  await page.evaluate((t) => {
    localStorage.setItem('theme', t);
    document.documentElement.setAttribute('data-theme', t);
  }, theme);
  await page.waitForTimeout(150);
}

function fail(msg) {
  console.error('FAIL:', msg);
  process.exitCode = 1;
}

function ok(msg) {
  console.log('OK:', msg);
}

async function main() {
  fs.mkdirSync(SHOTS_DIR, { recursive: true });
  const url = buildAndUrl();
  const browser = await chromium.launch();

  for (const vp of VIEWPORTS) {
    for (const theme of THEMES) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await ctx.newPage();
      await page.goto(url);
      await setTheme(page, theme);

      // Short edition (Oct 2026): each chapter ends with "When it breaks" /
      // "Do this Monday" / "Go deeper" instead of the Artifact / Ship this week /
      // Try it boxes, and source notes moved to Appendix D. Those renderers still
      // run on the archived full edition, so their checks moved to the /full/
      // block below; here we assert the new chapter format on every chapter.
      if (vp.name === 'desktop' && theme === 'light') {
        const fmt = await page.evaluate(() => {
          const chapters = Array.from(document.querySelectorAll('h2.chapter-heading'));
          const isBoundary = (el) => el.tagName === 'H2' && (
            /^chapter-/.test(el.id) || /^part-/.test(el.id) || el.id === 'closing' ||
            el.id === 'about-the-author' || el.id === 'changelog' || /^appendix-/.test(el.id));
          const missing = [];
          for (const h of chapters) {
            const heads = [];
            let tldr = false;
            for (let n = h.nextElementSibling; n && !isBoundary(n); n = n.nextElementSibling) {
              if (n.tagName === 'H3') heads.push(n.textContent.replace('\u00b6', '').trim());
              if (n.tagName === 'P' && n.textContent.trim() === 'TL;DR') tldr = true;
            }
            for (const want of ['When it breaks', 'Do this Monday', 'Go deeper']) {
              if (!heads.includes(want)) missing.push(`${h.id}: ${want}`);
            }
            if (!tldr) missing.push(`${h.id}: TL;DR`);
          }
          return { n: chapters.length, missing };
        });
        if (fmt.n !== 9) fail(`expected 9 chapters on /read/, got ${fmt.n}`);
        else ok('/read/ has 9 chapters');
        if (fmt.missing.length) fail(`chapter format gaps: ${fmt.missing.join('; ')}`);
        else ok('every chapter has TL;DR + When it breaks + Do this Monday + Go deeper');

        // Chapter-end screenshot: Chapter 3's "Do this Monday" checklist.
        const ch3Monday = page.locator('h2#chapter-3 ~ h3', { hasText: 'Do this Monday' }).first();
        if (await ch3Monday.count()) {
          await ch3Monday.scrollIntoViewIfNeeded();
          await page.waitForTimeout(150);
          await page.screenshot({ path: path.join(SHOTS_DIR, 'ch3-end_desktop_light.png'), fullPage: false });
        } else fail('chapter 3 "Do this Monday" not found');
      }

      // Appendix C source-card visual check on mobile.
      if (vp.name === 'mobile' && theme === 'light') {
        await page.locator('article.source-card').first().scrollIntoViewIfNeeded();
        await page.waitForTimeout(150);
        await page.locator('article.source-card').first().screenshot({
          path: path.join(SHOTS_DIR, 'source-card_mobile_light.png'),
        });
      }

      // Hero dek: present in article-header with the control-thesis text.
      if (theme === 'light' && vp.name === 'desktop') {
        const dek = await page.locator('header.article-header .article-dek').textContent();
        if (!dek || !/control problem/i.test(dek)) {
          fail(`hero dek missing or doesn't contain "control problem": ${JSON.stringify(dek)}`);
        } else ok('hero dek present');
      }

      // Hero CTA row: three buttons in the hero with correct targets.
      if (theme === 'light' && vp.name === 'desktop') {
        const ctas = await page.locator('nav.hero-cta a').all();
        if (ctas.length !== 3) fail(`expected 3 hero CTAs, got ${ctas.length}`);
        const hrefs = await Promise.all(ctas.map(c => c.getAttribute('href')));
        const expected = ['#chapter-7', '#appendix-b', /^mailto:info@ship-it-with\.ai\?subject=/];
        let ctaOk = true;
        for (let i = 0; i < 3; i++) {
          const h = hrefs[i] || '';
          const want = expected[i];
          const matched = (want instanceof RegExp) ? want.test(h) : h === want;
          if (!matched) { ctaOk = false; fail(`hero CTA ${i} href: got ${h}, want ${want}`); }
        }
        if (ctaOk) ok('hero CTA row: 3 correct targets');
      }

      // Mobile CTA stack: buttons full-width.
      if (theme === 'light' && vp.name === 'mobile') {
        const firstCta = page.locator('nav.hero-cta a').first();
        const box = await firstCta.boundingBox();
        if (box && box.width < vp.width * 0.7) fail(`mobile CTA not stacked full-width: ${box.width}px on ${vp.width}px viewport`);
        else ok('mobile CTAs stacked');
      }

      // About-the-author section: heading + #contact anchor present.
      if (theme === 'light' && vp.name === 'desktop') {
        const about = page.locator('#about-the-author');
        if (await about.count() !== 1) fail('#about-the-author heading missing');
        else ok('#about-the-author present');

        const contact = page.locator('#contact');
        if (await contact.count() !== 1) fail('#contact anchor missing (should be inside About)');
        else ok('#contact anchor present in About');

        // The Foreword is gone; its author note now sits in the Prologue.
        const aboutLink = page.locator('#nine-seconds ~ p a[href="#about-the-author"]');
        if (await aboutLink.count() < 1) fail('prologue "About the author" link missing');
        else ok('prologue links to About');
        if (await page.locator('#foreword').count() !== 0) fail('/read/ still has a #foreword section');
        else ok('/read/ has no Foreword');
      }

      // AGENTS.md de-linking: per chapter, at most one link.
      if (theme === 'light' && vp.name === 'desktop') {
        const tooMany = await page.evaluate(() => {
          const chapters = Array.from(document.querySelectorAll('h2[id^="chapter-"]'));
          // A chapter's region ends at the NEXT section-level heading - the next
          // chapter, or (for the last chapter) Closing/About/Changelog/an
          // Appendix. Without this, the last chapter would swallow the trailing
          // sections and miscount their (correctly un-delinked) AGENTS.md links.
          const isBoundary = (el) => el.tagName === 'H2' && (
            /^chapter-/.test(el.id) || el.id === 'closing' ||
            el.id === 'about-the-author' || el.id === 'changelog' ||
            /^appendix-/.test(el.id));
          for (let i = 0; i < chapters.length; i++) {
            const start = chapters[i];
            const links = [];
            let n = start.nextElementSibling;
            while (n && !isBoundary(n)) {
              if (n.querySelectorAll) {
                n.querySelectorAll('a[href^="https://agents.md"]').forEach(a => links.push(a));
              }
              n = n.nextElementSibling;
            }
            if (links.length > 1) return { chapter: start.id, count: links.length };
          }
          return null;
        });
        if (tooMany) fail(`chapter ${tooMany.chapter} has ${tooMany.count} AGENTS.md links (max 1)`);
        else ok('AGENTS.md links: <= 1 per chapter');
      }

      // Anchor links on every chapter h2 (artifact-box anchors: see /full/ below).
      if (theme === 'light' && vp.name === 'desktop') {
        const headingAnchors = await page.locator('h2[id^="chapter-"] a.anchor-link').count();
        if (headingAnchors < 9) fail(`expected >= 9 anchor links on chapter h2s, got ${headingAnchors}`);
        else ok(`anchor links on chapter h2s: ${headingAnchors}`);

        await page.locator('h2[id^="chapter-"] a.anchor-link').first().click();
        await page.waitForTimeout(200);
        const toastVisible = await page.locator('.anchor-toast.show').count();
        if (!toastVisible) fail('anchor-link click did not show toast');
        else ok('anchor-link click shows toast');
      }

      // No horizontal scrollbar on any viewport.
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
      if (scrollWidth > clientWidth + 1) {
        fail(`${vp.name}/${theme}: horizontal overflow (scrollWidth ${scrollWidth} > clientWidth ${clientWidth})`);
      } else {
        ok(`${vp.name}/${theme}: no horizontal overflow`);
      }

      // Reading times: every chapter TOC entry should have a non-empty min value.
      if (theme === 'light' && vp.name === 'desktop') {
        const missing = await page.evaluate(() =>
          Array.from(document.querySelectorAll('.toc-list .toc-time'))
            .filter(s => !s.textContent || !/\d+ min/.test(s.textContent)).length
        );
        if (missing > 0) fail(`${missing} chapters have missing/malformed reading-time`);
        else ok('all chapter reading-times present');
      }

      // Re-navigate to the clean URL (no #hash) then scroll to top so the
      // hero screenshot captures the actual hero, not whatever the previous
      // scrollIntoView left behind.
      await page.goto(url);
      await setTheme(page, theme);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(200);
      await page.screenshot({
        path: path.join(SHOTS_DIR, `hero_${vp.name}_${theme}.png`),
        fullPage: false,
      });
      ok(`hero screenshot saved: ${vp.name}/${theme}`);

      await ctx.close();
    }
  }

  // ===== /full/ archive (frozen September 2026 edition, old structure) =====
  // The source-note / artifact-box / callout renderers are exercised here now
  // that the short edition no longer uses them.
  const fullUrl = url.replace(/\/read\/index\.html$/, '/full/index.html');
  for (const theme of THEMES) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await ctx.newPage();
    await page.goto(fullUrl);
    await setTheme(page, theme);
    await page.screenshot({ path: path.join(SHOTS_DIR, `full-banner_desktop_${theme}.png`), fullPage: false });

    if (theme === 'light') {
      const banner = page.locator('aside.edition-banner');
      const btxt = (await banner.count()) ? await banner.first().textContent() : '';
      if (!/September 2026 archive\..*historical guidance.*maintained edition/.test(btxt || '')) {
        fail(`/full/ banner missing or wrong: ${JSON.stringify(btxt)}`);
      } else ok('/full/ banner present');
      const bannerLink = await banner.locator('a[href="/"]').count();
      if (!bannerLink) fail('/full/ banner missing link to the current edition (/)');
      else ok('/full/ banner links to the current edition');
      // Banner sits above the hero.
      const order = await page.evaluate(() => {
        const b = document.querySelector('aside.edition-banner');
        const h = document.querySelector('header.article-header');
        return b && h ? !!(b.compareDocumentPosition(h) & Node.DOCUMENT_POSITION_FOLLOWING) : false;
      });
      if (!order) fail('/full/ banner is not above the hero');
      else ok('/full/ banner is above the hero');

      for (let n = 1; n <= 10; n++) {
        if (await page.locator(`#chapter-${n}`).count() === 0) fail(`/full/ missing #chapter-${n}`);
      }
      if (await page.locator('#foreword').count() !== 1) fail('/full/ missing #foreword');
      else ok('/full/ has the old structure (Foreword + 10 chapters)');

      const sourceCount = await page.locator('aside.source-note').count();
      if (sourceCount < 3) fail(`/full/: expected >= 3 .source-note elements, got ${sourceCount}`);
      else ok(`/full/ source-note count: ${sourceCount}`);

      const artifactCount = await page.locator('aside.artifact-box').count();
      if (artifactCount < 10) fail(`/full/: expected >= 10 .artifact-box elements, got ${artifactCount}`);
      else ok(`/full/ artifact-box count: ${artifactCount}`);
      const firstArtifact = page.locator('aside.artifact-box').first();
      if (!await firstArtifact.locator('svg.artifact-icon').count()) fail('first artifact-box missing svg.artifact-icon');
      if (!await firstArtifact.locator('.artifact-label').count()) fail('first artifact-box missing .artifact-label');
      if (!await firstArtifact.locator('.artifact-title').count()) fail('first artifact-box missing .artifact-title');
      const artifactAnchors = await page.locator('aside.artifact-box a.anchor-link').count();
      if (artifactAnchors < 10) fail(`/full/: expected >= 10 anchor links on artifact-boxes, got ${artifactAnchors}`);
      else ok(`/full/ anchor links on artifact-boxes: ${artifactAnchors}`);

      const stackHasHr = await page.evaluate(() => {
        for (const a of document.querySelectorAll('aside.artifact-box')) {
          const n = a.nextElementSibling;
          if (n && n.tagName === 'HR') return true;
        }
        return false;
      });
      if (stackHasHr) fail('/full/: found <hr> right after an artifact-box');
      else ok('/full/: chapter-end stack has no <hr> after artifact-boxes');

      const aboutLink = page.locator('#where-i-am-coming-from ~ p a[href="#about-the-author"]');
      if (await aboutLink.count() < 1) fail('/full/ foreword "About the author" link missing');
      else ok('/full/ foreword links to About');
    }

    const note = page.locator('aside.source-note').first();
    if (await note.count()) {
      await note.scrollIntoViewIfNeeded();
      await page.waitForTimeout(150);
      await note.screenshot({ path: path.join(SHOTS_DIR, `source-note_desktop_${theme}.png`) });
    }
    const art = page.locator('aside.artifact-box').first();
    if (await art.count()) {
      await art.scrollIntoViewIfNeeded();
      await page.waitForTimeout(150);
      await art.screenshot({ path: path.join(SHOTS_DIR, `artifact_desktop_${theme}.png`) });
    }
    await ctx.close();
  }
  {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
    const page = await ctx.newPage();
    await page.goto(fullUrl);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    const cw = await page.evaluate(() => document.documentElement.clientWidth);
    if (sw > cw + 1) fail(`/full/ mobile: horizontal overflow (${sw} > ${cw})`);
    else ok('/full/ mobile: no horizontal overflow');
    await page.screenshot({ path: path.join(SHOTS_DIR, 'full-banner_mobile_light.png'), fullPage: false });
    await ctx.close();
  }

  await browser.close();
  if (process.exitCode) {
    console.error('\nVerification FAILED - see above.');
  } else {
    console.log('\nVerification PASSED.');
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
