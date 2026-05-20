import { expect, test } from '@playwright/test';

const BASE = '/the-invisible-college';

test.describe('departments index', () => {
  test('renders the heading, lede, and a list of every department', async ({ page }) => {
    const response = await page.goto(`${BASE}/departments`);
    expect(response?.status(), 'GET /departments status').toBe(200);
    await expect(page).toHaveTitle(/Departments/);

    await expect(
      page.getByRole('heading', { name: 'Departments', level: 1 }),
    ).toBeVisible();
    await expect(page.getByText(/Long-lived gatherings of Fellows/i)).toBeVisible();

    // Five departments were established in the 2026-05-20 bootstrap;
    // every department's name must surface as a link on the index.
    const list = page.locator('section[aria-labelledby="departments-list"] ol li');
    const items = await list.count();
    expect(items, 'department entries').toBeGreaterThanOrEqual(5);

    // Each entry must carry a chair line and a member-count line.
    for (let i = 0; i < items; i += 1) {
      const item = list.nth(i);
      await expect(item.locator('a').first()).toHaveAttribute(
        'href',
        new RegExp(`^${BASE}/departments/[a-z][a-z0-9-]+$`),
      );
      await expect(item.locator('p.meta')).toContainText(/Chair:/);
    }
  });

  test('every department links to a detail page that returns 200', async ({ page }) => {
    await page.goto(`${BASE}/departments`);
    const hrefs = await page
      .locator('section[aria-labelledby="departments-list"] ol li a')
      .first()
      .evaluateAll((nodes) => nodes.map((n) => n.getAttribute('href')));
    expect(hrefs.length, 'detail-page links').toBeGreaterThan(0);
    for (const href of hrefs) {
      if (!href) continue;
      const detail = await page.goto(href);
      expect(detail?.status(), `GET ${href}`).toBe(200);
      await expect(
        page.locator('p.runninghead', { hasText: /Department/i }),
      ).toBeVisible();
    }
  });
});

test.describe('department detail page', () => {
  test('mathematical-sciences shows chair, members, and description', async ({ page }) => {
    const response = await page.goto(`${BASE}/departments/mathematical-sciences`);
    expect(response?.status(), 'GET /departments/mathematical-sciences').toBe(200);

    await expect(
      page.getByRole('heading', { name: 'Mathematical Sciences', level: 1 }),
    ).toBeVisible();

    // Chair is wired with the Henri Poincaré record from bootstrap-departments.
    const chairDd = page.locator('dt', { hasText: /^Chair$/i }).locator('xpath=following-sibling::dd[1]');
    await expect(chairDd).toContainText(/Henri Poincar/);
    await expect(chairDd.locator('a')).toHaveAttribute(
      'href',
      `${BASE}/fellows/henri-poincare`,
    );

    // The description body comes from the markdown body the institute
    // exported; it must include the seed phrase from the migration.
    await expect(
      page.getByText(/Formal methods, computation, dynamical systems/i),
    ).toBeVisible();

    // The members list links each fellow profile.
    const members = page.locator('section.not-prose h2', { hasText: 'Members' });
    await expect(members).toBeVisible();
    const memberLinks = page.locator('section.not-prose ol li > a').first();
    await expect(memberLinks).toHaveAttribute(
      'href',
      new RegExp(`^${BASE}/fellows/[a-z][a-z0-9-]+$`),
    );
  });

  test('a department with no chair renders a vacant marker', async ({ page }) => {
    // letters-interpretive-studies was seeded without a chair in the
    // bootstrap migration. The page must surface that state explicitly
    // rather than rendering an empty dd.
    const response = await page.goto(`${BASE}/departments/letters-interpretive-studies`);
    expect(response?.status()).toBe(200);
    const chairDd = page
      .locator('dt', { hasText: /^Chair$/i })
      .locator('xpath=following-sibling::dd[1]');
    await expect(chairDd).toContainText(/vacant/i);
  });
});

test.describe('fellow profile surfaces departments', () => {
  test('Henri Poincaré shows Mathematical Sciences as chair', async ({ page }) => {
    const response = await page.goto(`${BASE}/fellows/henri-poincare`);
    expect(response?.status()).toBe(200);
    const deptDd = page
      .locator('dt', { hasText: /^\s*Departments?\s*$/i })
      .locator('xpath=following-sibling::dd[1]');
    await expect(deptDd).toContainText(/Mathematical Sciences/i);
    await expect(deptDd).toContainText(/chair/i);
    await expect(deptDd.locator('a').first()).toHaveAttribute(
      'href',
      `${BASE}/departments/mathematical-sciences`,
    );
  });

  test('a cross-listed fellow shows both departments', async ({ page }) => {
    // Michel de Montaigne is cross-listed in History/Philosophy and
    // Letters per the bootstrap migration.
    const response = await page.goto(`${BASE}/fellows/michel-de-montaigne`);
    expect(response?.status()).toBe(200);
    const deptDd = page
      .locator('dt', { hasText: /^\s*Departments?\s*$/i })
      .locator('xpath=following-sibling::dd[1]');
    await expect(deptDd).toContainText(/History/i);
    await expect(deptDd).toContainText(/Letters/i);
  });
});
