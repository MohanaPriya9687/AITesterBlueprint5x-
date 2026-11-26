import { defineConfig } from '@playwright/test';
import { resolve } from 'node:path';
import { loadEnvFile } from 'node:process';

loadEnvFile(resolve(__dirname, '.env'));

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  workers: 1,
  timeout: 60_000,
  expect: {
    timeout: 20_000,
  },
  reporter: [
    ['list'],
    ['allure-playwright', { resultsDir: 'allure-results' }],
  ],
  outputDir: 'test-results',
  use: {
    browserName: 'chromium',
    channel: 'chrome',
    headless: false,
    viewport: null,
    actionTimeout: 15_000,
    navigationTimeout: 30_000,
    screenshot: 'off',
    trace: 'off',
  },
});
