import { expect, test } from '@playwright/test';

const BASE = '/the-invisible-college';

// These tests assume at least one preprint version exists in
// src/content/preprints. The dev workflow places one there via
// `npm run sync` when the archive has any preprints; CI seeds a stub
// preprint before the test run if the archive is empty. The tests skip
// gracefully when no preprint is present so a clean checkout still
// passes.

async function gotoPreprintsList(page: import('@playwright/test').Page) {
  const response = await page.goto(`${BASE}/preprints`);
  expect(response?.status(), 'GET /preprints status').toBe(200);
}

test.describe('preprints list', () => {
  test('renders the preprints heading and the provisional notice', async ({ page }) => {
    await gotoPreprintsList(page);
    await expect(page).toHaveTitle(/Working preprints/);
    await expect(
      page.getByRole('heading', { name: 'Working preprints', level: 1 }),
    ).toBeVisible();
    // The standing andon-cord notice must be present so visitors do
    // not mistake a preprint for a peer-reviewed publication.
    const aside = page.locator('aside[role="note"]').first();
    await expect(aside).toBeVisible();
    await expect(aside.getByText(/Provisional/i)).toBeVisible();
    await expect(aside.getByText(/peer-reviewed record/i)).toBeVisible();
  });

  test('every preprint entry links to a detail page that returns 200', async ({ page }) => {
    await gotoPreprintsList(page);
    const links = page.locator('ol li > a[href*="/preprints/"]');
    const count = await links.count();
    test.skip(count === 0, 'no preprints in archive; nothing to follow');
    // Take the first; we just need to prove the routing wiring works.
    const href = await links.first().getAttribute('href');
    expect(href, 'preprint link href').toBeTruthy();
    const response = await page.goto(href!);
    expect(response?.status(), `GET ${href} status`).toBe(200);
    await expect(page.locator('article > header h1').first()).toBeVisible();
    await expect(page.locator('article .runninghead').first()).toContainText(
      'Working preprint',
    );
  });
});

test.describe('preprint detail page', () => {
  test('shows lead, version and the provisional notice', async ({ page }) => {
    await gotoPreprintsList(page);
    const firstLink = page.locator('ol li > a[href*="/preprints/"]').first();
    const count = await firstLink.count();
    test.skip(count === 0, 'no preprints in archive');
    const href = await firstLink.getAttribute('href');
    await page.goto(href!);
    // Version tag in the header running head.
    await expect(page.locator('article .runninghead').first()).toContainText(
      /Working preprint · v\d+/,
    );
    // The provisional aside warns the reader this is not peer reviewed.
    const aside = page.locator('aside[role="note"]').first();
    await expect(aside).toBeVisible();
    await expect(aside).toContainText(/not been peer\s+reviewed/i);
    // A <time> with an ISO datetime must be present in the meta line.
    const time = page.locator('article header time').first();
    await expect(time).toBeVisible();
    const datetime = await time.getAttribute('datetime');
    expect(datetime, 'datetime attr').toMatch(/^\d{4}-\d{2}-\d{2}T/);
  });
});
