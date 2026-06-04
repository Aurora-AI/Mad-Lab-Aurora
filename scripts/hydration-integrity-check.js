import puppeteer from 'puppeteer';

const url = process.argv[2] || 'http://localhost:4321/';

console.log('=========================================');
console.log('Running Hydration Integrity Gate');
console.log(`Target URL: ${url}`);
console.log('=========================================');

(async () => {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    const hydrationErrors = [];
    const uncaughtExceptions = [];
    const failedRequests = [];
    
    // Intercept console errors/warnings
    page.on('console', (msg) => {
      const text = msg.text();
      const type = msg.type();
      
      if (type === 'error' || type === 'warning') {
        const lowerText = text.toLowerCase();
        if (
          lowerText.includes('hydration') ||
          lowerText.includes('mismatch') ||
          lowerText.includes('did not match') ||
          lowerText.includes('extra attributes') ||
          lowerText.includes('server html')
        ) {
          hydrationErrors.push(`[${type.toUpperCase()}] ${text}`);
        }
      }
    });

    // Capture uncaught exceptions
    page.on('pageerror', (err) => {
      uncaughtExceptions.push(err.toString());
    });

    // Capture resource load failures
    page.on('requestfailed', (request) => {
      const failure = request.failure();
      failedRequests.push(`${request.url()} - Reason: ${failure ? failure.errorText : 'Unknown'}`);
    });

    console.log('Navigating to target page...');
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
    
    // Extra grace period to allow client-side hydration scripts to run
    console.log('Waiting for hydration checks...');
    await new Promise((resolve) => setTimeout(resolve, 5000));
    
    console.log('=========================================');
    let hasFailed = false;

    if (hydrationErrors.length > 0) {
      console.error('\x1b[31m%s\x1b[0m', `FAIL: ${hydrationErrors.length} Hydration errors detected:`);
      hydrationErrors.forEach((err) => console.error(`  > ${err}`));
      hasFailed = true;
    } else {
      console.log('\x1b[32m%s\x1b[0m', 'PASS: No hydration errors detected.');
    }

    if (uncaughtExceptions.length > 0) {
      console.error('\x1b[31m%s\x1b[0m', `FAIL: ${uncaughtExceptions.length} Uncaught page exceptions detected:`);
      uncaughtExceptions.forEach((err) => console.error(`  > ${err}`));
      hasFailed = true;
    } else {
      console.log('\x1b[32m%s\x1b[0m', 'PASS: No uncaught page exceptions.');
    }

    if (failedRequests.length > 0) {
      console.error('\x1b[31m%s\x1b[0m', `FAIL: ${failedRequests.length} Resource request failures detected:`);
      failedRequests.forEach((req) => console.error(`  > ${req}`));
      hasFailed = true;
    } else {
      console.log('\x1b[32m%s\x1b[0m', 'PASS: No failed asset requests.');
    }

    await browser.close();
    console.log('=========================================');

    if (hasFailed) {
      console.error('\x1b[31m%s\x1b[0m', 'Hydration Integrity Check: FAILED');
      process.exit(1);
    } else {
      console.log('\x1b[32m%s\x1b[0m', 'Hydration Integrity Check: PASSED');
      process.exit(0);
    }
  } catch (error) {
    console.error('An error occurred during verification:', error);
    if (browser) await browser.close();
    process.exit(1);
  }
})();
