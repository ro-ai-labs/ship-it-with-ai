// Run the python build, serve _site/ (or the repo root in Commit 1's interim
// state) on a free local port, and return baseUrl + a stop() function.
//
// Uses execFileSync (no shell) for safety and spawn for the long-lived server.
// The caller MUST call stop() in a finally block so the server doesn't leak.

const { execFileSync, spawn } = require('child_process');
const net = require('net');
const path = require('path');

function freePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.unref();
    srv.on('error', reject);
    srv.listen(0, () => {
      const port = srv.address().port;
      srv.close(() => resolve(port));
    });
  });
}

async function waitForReady(port, timeoutMs = 5000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      await new Promise((resolve, reject) => {
        const sock = net.connect(port, '127.0.0.1', () => { sock.end(); resolve(); });
        sock.on('error', reject);
      });
      return;
    } catch (_e) {
      await new Promise(r => setTimeout(r, 100));
    }
  }
  throw new Error(`server did not bind ${port} within ${timeoutMs}ms`);
}

async function buildAndServe(serveDir = '.') {
  const repoRoot = path.resolve(__dirname, '..', '..', '..');
  // CI builds once (the workflow's Build step) then verifies those exact bytes.
  // Set SITE_NO_REBUILD=1 to serve the existing _site/ without rebuilding.
  if (!process.env.SITE_NO_REBUILD) {
    execFileSync('python3', ['build/build_spa.py'], { cwd: repoRoot, stdio: 'inherit' });
  }

  const port = await freePort();
  const server = spawn('python3', ['-m', 'http.server', '-d', serveDir, String(port)],
                       { cwd: repoRoot, stdio: 'pipe' });
  try {
    await waitForReady(port);
  } catch (e) {
    server.kill();
    throw e;
  }
  return {
    baseUrl: `http://127.0.0.1:${port}`,
    stop: () => server.kill(),
  };
}

module.exports = { buildAndServe };
