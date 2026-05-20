import { expect, test } from '@playwright/test';

const BASE = '/the-invisible-college';

test.describe('archive page', () => {
  test('renders heading, year groups, and links to every post', async ({ page }) => {
    const response = await page.goto(`${BASE}/archive`);
    expect(response?.status(), 'GET /archive status').toBe(200);
    await expect(page).toHaveTitle(/Archive/);
    await expect(
      page.getByRole('heading', { name: 'Archive', level: 1 }),
    ).toBeVisible();

    // At least one year-group heading must be visible. Years render as
    // smallcaps h2s above each list of posts.
    const yearHeadings = page.locator('section h2');
    const yearCount = await yearHeadings.count();
    expect(yearCount, 'archive year groups').toBeGreaterThan(0);
    await expect(yearHeadings.first()).toBeVisible();

    // Every list item should be a post link rooted at /posts/.
    const postLinks = page.locator('section ul li > a[href*="/posts/"]');
    const postCount = await postLinks.count();
    expect(postCount, 'archive post links').toBeGreaterThan(0);

    // Click the first post link and confirm the destination is a real
    // publication page (heading + Publication running head).
    const href = await postLinks.first().getAttribute('href');
    expect(href, 'first post href').toBeTruthy();
    const postResponse = await page.goto(href!);
    expect(postResponse?.status(), `GET ${href} status`).toBe(200);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await expect(page.locator('article .runninghead').first()).toContainText(
      'Publication',
    );
  });

  test('lists posts in reverse chronological order within a year', async ({ page }) => {
    await page.goto(`${BASE}/archive`);
    // Pull every date label rendered inside the first year's <ul> and
    // verify it is non-increasing. Date format is "Mon DD, YYYY".
    const firstYearDates = await page
      .locator('section')
      .first()
      .locator('ul li .meta .tabular')
      .allInnerTexts();
    const parsed = firstYearDates.map((text) => Date.parse(text)).filter((n) => !Number.isNaN(n));
    expect(parsed.length, 'parseable dates in first year').toBeGreaterThan(0);
    for (let i = 1; i < parsed.length; i += 1) {
      expect(parsed[i - 1], `dates not monotonic at index ${i}`).toBeGreaterThanOrEqual(parsed[i]);
    }
  });
});
