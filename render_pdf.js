// Render learn-korean-v3.html → learn-korean-v3.pdf via Puppeteer (avoids Korean path issues in Edge)
const puppeteer = require('puppeteer');
const path = require('path');

const HTML = path.join(__dirname, 'learn-korean-v3.html');
const PDF  = path.join(__dirname, 'learn-korean-v3.pdf');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu'],
  });
  try {
    const page = await browser.newPage();
    const url = 'file:///' + HTML.replace(/\\/g, '/');
    console.log('Loading:', url);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 180000 });
    // small fixed delay to let fonts/CSS settle
    await new Promise(r => setTimeout(r, 1500));

    console.log('Rendering PDF...');
    await page.pdf({
      path: PDF,
      format: 'A4',
      margin: { top: '16mm', right: '18mm', bottom: '18mm', left: '18mm' },
      printBackground: true,
      displayHeaderFooter: true,
      footerTemplate: '<div style="width:100%;text-align:center;font-size:9px;color:#888;"><span class="pageNumber"></span></div>',
      headerTemplate: '<div></div>',
      preferCSSPageSize: false,
      timeout: 180000,
    });
    console.log('PDF saved:', PDF);
  } finally {
    await browser.close();
  }
})();
