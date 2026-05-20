import { expect, test } from '@playwright/test';

const BASE = '/the-invisible-college';

test.describe('research agenda page', () => {
  test('renders the heading, lede, and the markdown-imported prose', async ({ page }) => {
    const response = await page.goto(`${BASE}/agenda`);
    expect(response?.status(), 'GET /agenda status').toBe(200);
    await expect(page).toHaveTitle(/Research Agenda/);

    await expect(
      page.getByRole('heading', { name: 'Research Agenda', level: 1 }),
    ).toBeVisible();
    // The lede is the institutional framing line above the markdown.
    await expect(
      page.getByText(/standing intellectual priorities/i).first(),
    ).toBeVisible();

    // The page imports docs/research-agenda.md and renders its body
    // inside <article class="prose">. The imported markdown is expected
    // to contain at least one <h2> section heading.
    const sectionHeadings = page.locator('article.prose h2');
    const headingCount = await sectionHeadings.count();
    expect(headingCount, 'agenda h2 sections').toBeGreaterThan(0);
    await expect(sectionHeadings.first()).toBeVisible();

    // The page suppresses the imported markdown's leading h1 ("# Research
    // Agenda") so the document does not present two competing titles.
    // The h1 still exists in the DOM (the markdown file owns it); the
    // page CSS hides it via :first-of-type. Only the page-header h1
    // (inside the <header>) should be visible.
    const visibleH1s = page.locator('h1:visible');
    await expect(visibleH1s).toHaveCount(1);
    await expect(visibleH1s).toHaveText('Research Agenda');
    // And the markdown's hidden h1 must still exist in the DOM.
    const hiddenAgendaH1 = page.locator('article.prose > h1#research-agenda');
    await expect(hiddenAgendaH1).toBeHidden();
  });
});
