// Render 3 Gumroad images: cover, features, chapters — all at 1280×720 PNG.
const puppeteer = require('puppeteer');
const path = require('path');

const PAIRS = [
  ['gumroad-cover.html',    'gumroad-cover.png',    600, 600],   // square thumbnail
  ['gumroad-features.html', 'gumroad-features.png', 1280, 720],  // 16:9 preview
  ['gumroad-chapters.html', 'gumroad-chapters.png', 1280, 720],  // 16:9 preview
];

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu'],
  });
  try {
    for (const [htmlFile, pngFile, w, h] of PAIRS) {
      const htmlPath = path.join(__dirname, htmlFile);
      const pngPath  = path.join(__dirname, pngFile);
      const url = 'file:///' + htmlPath.replace(/\\/g, '/');

      const page = await browser.newPage();
      await page.setViewport({ width: w, height: h, deviceScaleFactor: 2 });
      console.log(`Loading: ${url}  (${w}x${h})`);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await new Promise(r => setTimeout(r, 500));

      await page.screenshot({
        path: pngPath,
        type: 'png',
        clip: { x: 0, y: 0, width: w, height: h },
      });
      console.log(`Saved: ${pngFile}`);
      await page.close();
    }
  } finally {
    await browser.close();
  }
})();
