/**
 * test_playwright.js
 * Quick smoke test to confirm Playwright is installed and working.
 * Run: node scripts/test_playwright.js
 */

const { chromium } = require("playwright");

(async () => {
  console.log("Testing Playwright installation...");
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto("https://example.com", { timeout: 10000 });
    const title = await page.title();
    console.log(`✓ Playwright working. Test page title: "${title}"`);
  } catch (err) {
    console.error("✗ Playwright test failed:", err.message);
    console.error("\nFix: npm install && npx playwright install chromium");
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
})();
