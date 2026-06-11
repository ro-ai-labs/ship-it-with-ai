// Run the python build via execFileSync (arg-array form: no shell, no injection),
// then return a file:// URL for the generated index.html.
const { execFileSync } = require('child_process');
const path = require('path');

function buildAndUrl() {
  const repoRoot = path.resolve(__dirname, '..', '..', '..');
  execFileSync('python3', ['build/build_spa.py'], { cwd: repoRoot, stdio: 'inherit' });
  // The all-in-one document (formerly the repo-root index.html) now lives at
  // _site/read/index.html; the root index.html is the thin landing page.
  return 'file://' + path.join(repoRoot, '_site', 'read', 'index.html');
}

module.exports = { buildAndUrl };
