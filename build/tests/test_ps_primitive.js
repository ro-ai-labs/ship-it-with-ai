// E2E verification of the Permissions / Sandbox primitive cascade.
// Server expected to be running on http://127.0.0.1:8780 serving _site/.

const { chromium } = require('playwright');
const http = require('http');

const BASE = 'http://127.0.0.1:8780';
const results = [];

function record(id, name, pass, evidence) {
  results.push({ id, name, pass, evidence });
  const tag = pass ? 'PASS' : 'FAIL';
  console.log(`[${tag}] ${id}. ${name}`);
  if (evidence) console.log('       ' + String(evidence).slice(0, 240));
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      if (res.statusCode !== 200) { reject(new Error('status ' + res.statusCode)); return; }
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function main() {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();

  try {
    // ===== 1. Ch.1 P/S section navigability =====
    {
      await page.goto(BASE + '/chapter-1-primitives/');
      const tocLink = page.locator('a[href*="#permissions-sandbox"]').first();
      const tocCount = await page.locator('a[href*="#permissions-sandbox"]').count();
      if (tocCount === 0) {
        record(1, 'Ch.1 P/S section navigability', false, 'no TOC anchor for #permissions-sandbox found');
      } else {
        await tocLink.click();
        await page.waitForTimeout(400);
        const h3 = await page.locator('h3#permissions-sandbox').first();
        const h3Exists = await h3.count();
        const h3Text = h3Exists ? (await h3.textContent() || '').trim() : '';
        const ok = h3Exists && /Permissions\s*\/\s*Sandbox/i.test(h3Text);
        record(1, 'Ch.1 P/S section navigability', ok,
          `TOC links: ${tocCount}, h3 text: "${h3Text}"`);
      }
    }

    // ===== 2. Diagram cell ordering =====
    {
      await page.goto(BASE + '/chapter-1-primitives/');
      const names = await page.locator('.primitives-grid > .primitive .primitive-name').allTextContents();
      const trimmed = names.map(n => n.trim().toLowerCase());
      const expected = ['context window', 'tools', 'permissions / sandbox', 'skills', 'plugins', 'mcp', 'memory'];
      const orderOk = JSON.stringify(trimmed) === JSON.stringify(expected);

      const recursive = await page.locator('.primitives-recursive .primitive').count();
      const recursiveName = recursive ? (await page.locator('.primitives-recursive .primitive .primitive-name').first().textContent() || '').trim().toLowerCase() : '';
      const recursiveOk = recursive === 1 && /subagent/.test(recursiveName);

      record(2, 'Diagram cell ordering (7 main + 1 recursive subagents)', orderOk && recursiveOk,
        `grid: [${trimmed.join(', ')}]; recursive count: ${recursive} ("${recursiveName}")`);
    }

    // ===== 3. Sublists on Memory and P/S =====
    {
      const sublistCount = await page.locator('.primitive-sublist').count();
      // Find P/S sublist spans
      const psSublistSpans = await page.locator('.primitives-grid > .primitive:has(.primitive-name:has-text("Permissions")) .primitive-sublist span').allTextContents();
      const memSublistSpans = await page.locator('.primitives-grid > .primitive:has(.primitive-name:has-text("Memory")) .primitive-sublist span').allTextContents();
      const psTexts = psSublistSpans.map(s => s.trim().toLowerCase());
      const memTexts = memSublistSpans.map(s => s.trim().toLowerCase());
      const psOk = psTexts.includes('decision layer') && psTexts.includes('os enforcement');
      const memOk = memTexts.includes('manually defined') && memTexts.includes('auto-memory system');
      const ok = sublistCount === 2 && psOk && memOk;
      record(3, 'Sublists present on Memory + P/S', ok,
        `count: ${sublistCount}, P/S: [${psTexts.join(', ')}], Mem: [${memTexts.join(', ')}]`);
    }

    // ===== 4. Vocabulary note rewrite =====
    {
      const body = await page.locator('body').textContent();
      const hasNew = body.includes('The test for primitiveness is convergence');
      const hasOld = body.includes('are not additional primitives');
      const ok = hasNew && !hasOld;
      record(4, 'Vocabulary note rewrite', ok,
        `new phrase present: ${hasNew}, old phrase present: ${hasOld}`);
    }

    // ===== 5. Ch.1 "Nine questions today" =====
    {
      const body = await page.locator('body').textContent();
      const hasNine = body.includes('Nine questions today');
      const hasEight = /Eight questions today/.test(body);
      record(5, 'Ch.1 "Nine questions today"', hasNine && !hasEight,
        `nine present: ${hasNine}, eight present: ${hasEight}`);
    }

    // ===== 6. Ch.2 "Eight inspection points" =====
    {
      await page.goto(BASE + '/chapter-2-anatomy-invariant/');
      const body = await page.locator('body').textContent();
      const hasEight = body.includes('Eight inspection points');
      const hasNine = body.includes('Nine inspection points');
      record(6, 'Ch.2 "Eight inspection points"', hasEight && !hasNine,
        `eight present: ${hasEight}, nine present: ${hasNine}`);
    }

    // ===== 7. Ch.2 Artifact callout =====
    {
      const body = await page.locator('body').textContent();
      const hasNew = /the eight inspection points from this chapter/i.test(body);
      const hasOld = /the nine inspection points from this chapter/i.test(body);
      record(7, 'Ch.2 Artifact callout', hasNew && !hasOld,
        `new phrase: ${hasNew}, old phrase: ${hasOld}`);
    }

    // ===== 8. Ch.3 framing paragraph =====
    {
      await page.goto(BASE + '/chapter-3-governance-in-layers/');
      const body = await page.locator('body').textContent();
      const ok = body.includes('configuration surfaces of the Permissions / Sandbox primitive');
      record(8, 'Ch.3 framing paragraph', ok,
        `phrase present: ${ok}`);
    }

    // ===== 9. Ch.3 PocketOS callout =====
    {
      const body = await page.locator('body').textContent();
      const ok = body.includes('Permissions / Sandbox would have caught it twice');
      record(9, 'Ch.3 PocketOS callout', ok,
        `phrase present: ${ok}`);
    }

    // ===== 10. Ch.3 layer headings preserved =====
    {
      const layerHeadings = [
        'Layer one: permissions',
        'Layer two:',
        'Layer three:',
        'Layer four:',
        'Layer five: telemetry',
      ];
      const body = await page.locator('body').textContent();
      // Check each appears
      const found = {};
      for (let i = 1; i <= 5; i++) {
        const words = ['one','two','three','four','five'];
        const re = new RegExp(`Layer ${words[i-1]}:`, 'i');
        found[words[i-1]] = re.test(body);
      }
      const hasPermissions = body.includes('Layer one: permissions');
      const hasTelemetry = body.includes('Layer five: telemetry');
      const ok = Object.values(found).every(Boolean) && hasPermissions && hasTelemetry;
      record(10, 'Ch.3 five layer headings preserved', ok,
        `headings found: ${JSON.stringify(found)}, perm: ${hasPermissions}, tel: ${hasTelemetry}`);
    }

    // ===== 11. Appendix C 3 new entries =====
    {
      await page.goto(BASE + '/appendix-c-sources/');
      const body = await page.locator('body').textContent();
      const html = await page.content();
      const h3Exists = await page.locator('h3:has-text("Permissions / Sandbox primitive sources")').count();
      const claudeOk = body.includes('Claude Code ships an Allow/Ask/Deny');
      const codexOk = body.includes('Codex CLI enforces OS-level sandbox by default');
      const opencodeOk = body.includes('opencode ships an in-agent permission-prompt');
      const link1 = /developers\.openai\.com\/codex\/concepts\/sandboxing/.test(html);
      const link2 = /vercel\.com\/kb\/guide\/running-opencode-securely/.test(html);
      const ok = h3Exists > 0 && claudeOk && codexOk && opencodeOk && link1 && link2;
      record(11, 'Appendix C: 3 new P/S entries', ok,
        `h3:${h3Exists}, claude:${claudeOk}, codex:${codexOk}, opencode:${opencodeOk}, link1:${link1}, link2:${link2}`);
    }

    // ===== 12. Changelog entry =====
    {
      await page.goto(BASE + '/changelog/');
      const body = await page.locator('body').textContent();
      const hasEntry = body.includes('2026-05-27 - Permissions / Sandbox primitive')
                       || body.includes('2026-05-27 - Permissions / Sandbox primitive')
                       || body.includes('2026-05-27 - Permissions / Sandbox primitive');
      // Check it's the top dated entry - first date-style heading should be 2026-05-27
      const headings = await page.locator('h2, h3').allTextContents();
      const dateHeadings = headings.filter(h => /^\s*\d{4}-\d{2}-\d{2}/.test(h));
      const topIsToday = dateHeadings.length > 0 && /^\s*2026-05-27/.test(dateHeadings[0]);
      const hasThirdSlot = body.includes('third slot');
      const hasMemoryHalves = /two halves like Memory/i.test(body);
      const ok = hasEntry && topIsToday && hasThirdSlot && hasMemoryHalves;
      record(12, 'Changelog entry top + body text', ok,
        `entry:${hasEntry}, topIs2026-05-27:${topIsToday}, thirdSlot:${hasThirdSlot}, halves:${hasMemoryHalves}; first 3 date headings: ${JSON.stringify(dateHeadings.slice(0,3))}`);
    }

    // ===== 13. llms-full.txt =====
    {
      const txt = await fetchText(BASE + '/llms-full.txt');
      const hasBold = txt.includes('**Permissions / Sandbox**');
      const canonical = 'Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents.';
      const hasCanonical = txt.includes(canonical);
      const hasEight = txt.includes('Eight inspection points');
      const ok = hasBold && hasCanonical && hasEight;
      record(13, 'llms-full.txt content', ok,
        `bold:${hasBold}, canonical:${hasCanonical}, eight:${hasEight}`);
    }

    // ===== 14. Cross-section linking =====
    {
      await page.goto(BASE + '/chapter-1-primitives/');
      const body = await page.locator('body').textContent();
      // Spec wording: "Chapter 3 walks the configuration surfaces..."
      const hasForwardRef = /Chapter\s*3\s+walks the configuration surfaces/i.test(body);
      record(14, 'Cross-section linking: forward-ref to Ch.3', hasForwardRef,
        `forward ref present: ${hasForwardRef}`);
    }

    // ===== 15. Anchor copy-link =====
    {
      const h3Id = await page.locator('h3#permissions-sandbox').count();
      // Look for copy-link anchor - convention is a sibling/child <a> with ¶ character.
      // Check inside h3, then immediately after.
      const html = await page.content();
      // Find the h3 and a nearby ¶ link
      const m = html.match(/<h3[^>]*id="permissions-sandbox"[^>]*>([\s\S]{0,400})/);
      const snippet = m ? m[0] : '';
      const hasPilcrow = snippet.includes('¶') || snippet.includes('&para;') || snippet.includes('&#182;');
      // Also check for an <a> with href pointing back to #permissions-sandbox near the heading
      const hasAnchorLink = /href=["']#permissions-sandbox["']/i.test(snippet);
      const ok = h3Id > 0 && (hasPilcrow || hasAnchorLink);
      record(15, 'Anchor copy-link on h3', ok,
        `h3 id present:${h3Id > 0}, pilcrow near:${hasPilcrow}, anchor href#permissions-sandbox:${hasAnchorLink}`);
    }

    // ===== 16. Read-mode integration =====
    {
      await page.goto(BASE + '/read/');
      // Approach: the canonical primitive list "Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents."
      // appears in /read/ - confirms the section is integrated in the right order.
      // Also confirm an h3#permissions-sandbox is present in /read/.
      const html = await page.content();
      const canonical = 'Context window. Tools. Permissions / Sandbox. Skills. Plugins. MCP. Memory. Subagents.';
      const hasCanonical = html.includes(canonical);
      const hasH3 = /<h3[^>]*id="permissions-sandbox"[^>]*>\s*Permissions\s*\/\s*Sandbox/i.test(html);
      // Positional: find where the h3#permissions-sandbox sits and confirm "Skills" content appears after it in the same Ch.1 region.
      const psIdx = html.indexOf('id="permissions-sandbox"');
      // Skills mention as a primitive-cell - find ".primitive-name">Skills inside the primitives-grid that follows the section
      const psToEnd = psIdx >= 0 ? html.slice(psIdx, psIdx + 200000) : '';
      // The very next "Tools section" of Ch.2 / Ch.3 doesn't matter; we just need P/S h3 to appear at the right depth.
      const ok = hasCanonical && hasH3 && psIdx > 0;
      record(16, 'Read-mode P/S section integrated', ok,
        `canonical list present:${hasCanonical}, h3#permissions-sandbox present:${hasH3}, byte offset:${psIdx}`);
    }

    // ===== 17. Sitemap unchanged count =====
    {
      const xml = await fetchText(BASE + '/sitemap.xml');
      const urlCount = (xml.match(/<url>/g) || []).length;
      const ok = urlCount === 21;
      record(17, 'Sitemap has 21 URLs', ok, `count: ${urlCount}`);
    }

  } finally {
    await browser.close();
  }

  console.log('\n===== SUMMARY =====');
  const pass = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(`${pass}/${total} pass`);
  for (const r of results) {
    if (!r.pass) console.log(`  FAIL ${r.id}: ${r.name} - ${r.evidence}`);
  }
  process.exit(pass === total ? 0 : 1);
}

main().catch(e => { console.error('ERROR:', e); process.exit(2); });
