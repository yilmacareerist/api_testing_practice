const { chromium } = require('playwright');

async function validateHackerNewsSorting() {
  // Launch Chromium browser (set headless: false to watch it run)
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('Navigating to Hacker News /newest...');
  await page.goto('https://news.ycombinator.com/newest');

  const timestamps = [];

  while (timestamps.length < 100) {
    // Wait for the subline age elements to render
    await page.waitForSelector('.subline .age');

    // Extract timestamps from the current page
    const pageTimestamps = await page.$$eval('.subline .age', (elements) =>
      elements.map((el) => {
        // Hacker News provides the full ISO timestamp inside the title attribute
        return el.getAttribute('title') || el.innerText;
      })
    );

    // Collect timestamps up to exactly 100
    for (const time of pageTimestamps) {
      if (timestamps.length < 100) {
        timestamps.push(time);
      }
    }

    console.log(`Collected ${timestamps.length} of 100 article timestamps...`);

    // If we need more articles, click the 'More' button
    if (timestamps.length < 100) {
      const moreLink = page.locator('a.morelink');
      if (await moreLink.isVisible()) {
        await moreLink.click();
        await page.waitForLoadState('domcontentloaded');
      } else {
        console.warn('No more link found before reaching 100 articles.');
        break;
      }
    }
  }

  // Validate sorting: every item must be newer than or equal to the next item
  let isSorted = true;
  for (let i = 0; i < timestamps.length - 1; i++) {
    const currentTime = new Date(timestamps[i]).getTime();
    const nextTime = new Date(timestamps[i + 1]).getTime();

    if (currentTime < nextTime) {
      console.error(`Sort validation failed at index ${i}:`);
      console.error(`  Item ${i}:   ${timestamps[i]}`);
      console.error(`  Item ${i + 1}: ${timestamps[i + 1]}`);
      isSorted = false;
      break;
    }
  }

  if (isSorted && timestamps.length === 100) {
    console.log('\n SUCCESS: The first 100 articles are strictly sorted from newest to oldest!');
  } else {
    throw new Error(' Validation Failed: Articles are not properly sorted or 100 items were not collected.');
  }

  await browser.close();
}

validateHackerNewsSorting().catch((err) => {
  console.error(err);
  process.exit(1);
});