import { defineConfig, devices } from '@playwright/test';

// Astro serves the site under a `base` path. baseURL includes the base
// so each `page.goto('/')` resolves to the site root; tests use absolute
// paths that already include `/the-invisible-college`.
const BASE_PATH = '/the-invisible-college';
const SERVER_URL = 'http://localhost:4321';
const BASE_URL = `${SERVER_URL}${BASE_PATH}`;

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? 'github' : 'list',
  use: {
    baseURL: SERVER_URL,
    trace: 'on-first-retry',
    extraHTTPHeaders: {},
  },
  projects: [
    {
      name: 'desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 800 },
      },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 14'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});

export { BASE_PATH };
