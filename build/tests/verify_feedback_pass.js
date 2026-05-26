// Verification for the 2026-05-26 feedback pass.
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

      // Assertion: Source-note callouts present in body.
      if (vp.name === 'desktop' && theme === 'light') {
        const sourceCount = await page.locator('aside.source-note').count();
        if (sourceCount < 3) fail(`expected >= 3 .source-note elements, got ${sourceCount}`);
        else ok(`source-note count: ${sourceCount}`);

        const note = page.locator('aside.source-note').first();
        if (await note.count()) {
          await note.scrollIntoViewIfNeeded();
          await page.waitForTimeout(150);
          await note.screenshot({ path: path.join(SHOTS_DIR, 'source-note_desktop_light.png') });
        }
      }
      if (vp.name === 'desktop' && theme === 'dark') {
        const note = page.locator('aside.source-note').first();
        if (await note.count()) {
          await note.scrollIntoViewIfNeeded();
          await page.waitForTimeout(150);
          await note.screenshot({ path: path.join(SHOTS_DIR, 'source-note_desktop_dark.png') });
        }
      }

      // Assertion: Artifact-box wrapping — should match the 10 chapters.
      if (vp.name === 'desktop' && theme === 'light') {
        const artifactCount = await page.locator('aside.artifact-box').count();
        if (artifactCount < 10) fail(`expected >= 10 .artifact-box elements, got ${artifactCount}`);
        else ok(`artifact-box count: ${artifactCount}`);

        const firstArtifact = page.locator('aside.artifact-box').first();
        const hasIcon = await firstArtifact.locator('svg.artifact-icon').count();
        const hasLabel = await firstArtifact.locator('.artifact-label').count();
        const hasTitle = await firstArtifact.locator('.artifact-title').count();
        if (!hasIcon)  fail('first artifact-box missing svg.artifact-icon');
        if (!hasLabel) fail('first artifact-box missing .artifact-label');
        if (!hasTitle) fail('first artifact-box missing .artifact-title');

        await firstArtifact.scrollIntoViewIfNeeded();
        await page.waitForTimeout(150);
        await firstArtifact.screenshot({ path: path.join(SHOTS_DIR, 'artifact_desktop_light.png') });
      }
      if (vp.name === 'desktop' && theme === 'dark') {
        const firstArtifact = page.locator('aside.artifact-box').first();
        if (await firstArtifact.count()) {
          await firstArtifact.scrollIntoViewIfNeeded();
          await page.waitForTimeout(150);
          await firstArtifact.screenshot({ path: path.join(SHOTS_DIR, 'artifact_desktop_dark.png') });
        }
      }

      // Chapter-end stack: no <hr> between artifact-box and the following action/try boxes.
      if (vp.name === 'desktop' && theme === 'light') {
        const stackHasHr = await page.evaluate(() => {
          const artifacts = document.querySelectorAll('aside.artifact-box');
          for (const a of artifacts) {
            let n = a.nextElementSibling;
            while (n && n.tagName === 'HR') return true;
            if (n && (n.classList.contains('action-box') || n.classList.contains('try-box'))) continue;
          }
          return false;
        });
        if (stackHasHr) fail('found <hr> between artifact-box and next callout');
        else ok('chapter-end stack has no <hr> between siblings');

        const ch3End = page.locator('aside.artifact-box').nth(2);
        await ch3End.scrollIntoViewIfNeeded();
        await page.waitForTimeout(150);
        await page.screenshot({
          path: path.join(SHOTS_DIR, 'ch3-end_desktop_light.png'),
          fullPage: false,
        });
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

        const aboutLink = page.locator('#where-i-am-coming-from ~ p a[href="#about-the-author"]');
        if (await aboutLink.count() < 1) fail('foreword "About the author" link missing');
        else ok('foreword links to About');
      }

      // AGENTS.md de-linking: per chapter, at most one link.
      if (theme === 'light' && vp.name === 'desktop') {
        const tooMany = await page.evaluate(() => {
          const chapters = Array.from(document.querySelectorAll('h2[id^="chapter-"]'));
          for (let i = 0; i < chapters.length; i++) {
            const start = chapters[i];
            const end = chapters[i + 1] || null;
            const links = [];
            let n = start.nextElementSibling;
            while (n && n !== end) {
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

      // Anchor links: at least one on a chapter h2 and one on an artifact-box.
      if (theme === 'light' && vp.name === 'desktop') {
        const headingAnchors = await page.locator('h2[id^="chapter-"] a.anchor-link').count();
        if (headingAnchors < 10) fail(`expected >= 10 anchor links on chapter h2s, got ${headingAnchors}`);
        else ok(`anchor links on chapter h2s: ${headingAnchors}`);

        const artifactAnchors = await page.locator('aside.artifact-box a.anchor-link').count();
        if (artifactAnchors < 10) fail(`expected >= 10 anchor links on artifact-boxes, got ${artifactAnchors}`);
        else ok(`anchor links on artifact-boxes: ${artifactAnchors}`);

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

  await browser.close();
  if (process.exitCode) {
    console.error('\nVerification FAILED — see above.');
  } else {
    console.log('\nVerification PASSED.');
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
