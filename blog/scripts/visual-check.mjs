import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';

const BASE = 'http://localhost:4321/the-invisible-college';
const OUT = 'screenshots';

await mkdir(OUT, { recursive: true });

const browser = await chromium.launch();

async function shoot(viewport, suffix) {
  const ctx = await browser.newContext({
    viewport,
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();

  for (const [name, path] of [
    ['home', ''],
    ['about', '/about'],
    ['post', '/posts/first-light'],
  ]) {
    await page.goto(BASE + path, { waitUntil: 'networkidle' });
    await page.screenshot({
      path: `${OUT}/${name}-${suffix}.png`,
      fullPage: true,
    });
    console.log(`saved ${OUT}/${name}-${suffix}.png`);
  }
  await ctx.close();
}

await shoot({ width: 1280, height: 800 }, 'desktop');
await shoot({ width: 390, height: 844 }, 'mobile');

await browser.close();
