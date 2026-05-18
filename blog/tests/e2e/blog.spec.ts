import { expect, test } from '@playwright/test';

const BASE = '/the-invisible-college';

test.describe('home page', () => {
  test('renders the institutional title and running head', async ({ page }) => {
    await page.goto(BASE);
    await expect(page).toHaveTitle(/The Invisible College/);
    await expect(
      page.getByRole('heading', { name: 'The Invisible College', level: 1 }),
    ).toBeVisible();
    await expect(page.locator('.runninghead').first()).toContainText(
      'The Invisible College',
    );
  });

  test('lists at least one post', async ({ page }) => {
    await page.goto(BASE);
    const list = page.locator('ol li');
    await expect(list.first()).toBeVisible();
  });

  test('post links navigate to a rendered post page', async ({ page }) => {
    await page.goto(BASE);
    const firstLink = page.locator('ol li a').first();
    const href = await firstLink.getAttribute('href');
    expect(href).toBeTruthy();
    await firstLink.click();
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    // Each post page tags itself as a "Publication" above the title.
    await expect(page.locator('article .runninghead').first()).toContainText(
      'Publication',
    );
  });
});

test.describe('about page', () => {
  test('renders prose content', async ({ page }) => {
    await page.goto(`${BASE}/about`);
    await expect(
      page.getByRole('heading', { name: 'About the College', level: 1 }),
    ).toBeVisible();
    await expect(page.getByText(/research institution/i).first()).toBeVisible();
  });
});

test.describe('a posted piece', () => {
  test('shows author and date in the byline', async ({ page }) => {
    await page.goto(`${BASE}/posts/first-light`);
    await expect(
      page.getByRole('heading', { name: 'First light', level: 1 }),
    ).toBeVisible();
    await expect(page.locator('.meta').first()).toContainText('The Founder');
    await expect(page.locator('time').first()).toBeVisible();
  });
});

test.describe('fellows', () => {
  test('index lists the founding cohort', async ({ page }) => {
    await page.goto(`${BASE}/fellows`);
    await expect(
      page.getByRole('heading', { name: 'The Fellows', level: 1 }),
    ).toBeVisible();
    // The founding cohort should be present.
    for (const name of [
      'Ada Lovelace',
      'Henri Poincar',
      'Michel de Montaigne',
      'Pierre Bayle',
    ]) {
      await expect(page.getByText(name).first()).toBeVisible();
    }
  });

  test('individual profile renders identity and at least one section', async ({
    page,
  }) => {
    await page.goto(`${BASE}/fellows/ada-lovelace`);
    await expect(
      page.getByRole('heading', { name: 'Ada Lovelace', level: 1 }),
    ).toBeVisible();
    await expect(page.locator('article .runninghead').first()).toContainText(
      'Fellow',
    );
    // The "Approach" section is always present (sourced from the genome).
    await expect(page.getByRole('heading', { name: 'Approach' })).toBeVisible();
  });

  test('post bylines link to the author profile', async ({ page }) => {
    await page.goto(
      `${BASE}/posts/2026-05-17-when-the-same-sum-gives-different-answer-4da4`,
    );
    const bylineLink = page.locator('article header a', {
      hasText: 'Ada Lovelace',
    });
    await expect(bylineLink).toBeVisible();
    const href = await bylineLink.getAttribute('href');
    expect(href).toContain('/fellows/ada-lovelace');
  });
});

test.describe('layout', () => {
  test('uses serif typography for body content', async ({ page }) => {
    await page.goto(BASE);
    const bodyFont = await page.evaluate(() => {
      return window.getComputedStyle(document.body).fontFamily;
    });
    expect(bodyFont.toLowerCase()).toMatch(
      /charter|iowan|source serif|cambria|georgia|serif/,
    );
  });

  test('renders on a mobile viewport without overflow', async ({
    page,
    viewport,
  }) => {
    test.skip(!viewport || viewport.width > 500, 'desktop-only viewport');
    await page.goto(BASE);
    const main = page.locator('main');
    const box = await main.boundingBox();
    expect(box).not.toBeNull();
    if (box && viewport) {
      // Allow a small slack for scrollbars or sub-pixel rounding.
      expect(box.width).toBeLessThanOrEqual(viewport.width + 2);
    }
  });
});
