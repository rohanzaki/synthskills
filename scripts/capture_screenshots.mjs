// Capture the site's key pages in light mode with headless Chrome (puppeteer-core).
//   PUPPETEER_CORE=/path/to/node_modules/puppeteer-core CHROME=/usr/bin/google-chrome \
//     node scripts/capture_screenshots.mjs [https://skills.synthlabs.pk]
// Writes assets/screens/{home,work,skills,connect}.png at 1440 x 900.
import { pathToFileURL } from 'node:url';
import { join, resolve } from 'node:path';
import { mkdirSync } from 'node:fs';

const base = process.argv[2] || 'https://skills.synthlabs.pk';
const core = process.env.PUPPETEER_CORE || 'puppeteer-core';
const mod = await import(core.startsWith('/') ? pathToFileURL(join(core, 'lib/esm/puppeteer/puppeteer-core.js')).href : core);
const puppeteer = mod.default || mod;
const out = resolve(new URL('..', import.meta.url).pathname, 'assets/screens');
mkdirSync(out, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || '/usr/bin/google-chrome',
  headless: 'new',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars', '--force-color-profile=srgb'],
});
for (const [name, route] of [['home', '/'], ['work', '/work'], ['skills', '/skills'], ['connect', '/connect']]) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
  await page.goto(base + route, { waitUntil: 'networkidle0', timeout: 45000 });
  await new Promise((r) => setTimeout(r, 1500));
  await page.screenshot({ path: join(out, name + '.png') });
  console.log(name + '.png captured from ' + base + route);
  await page.close();
}
await browser.close();
