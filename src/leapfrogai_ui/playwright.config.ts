import type { PlaywrightTestConfig } from '@playwright/test';
import { devices } from '@playwright/test';
import * as dotenv from 'dotenv';

dotenv.config();

const PORT = 4173;
process.env.ORIGIN = `http://localhost:${PORT}`;

const chromeConfig = {
  name: 'chromium',
  use: {
    ...devices['Desktop Chrome'],
    // Use prepared auth state.
    storageState: 'playwright/.auth/user.json'
  },
  dependencies: ['setup']
};

// LEAVE THIS COMMENTED OUT CODE FOR DEVELOPMENT PURPOSES/TESTING
// const firefoxConfig = {
//   name: 'firefox',
//   use: {
//     ...devices['Desktop Firefox'],
//     // Use prepared auth state.
//     storageState: 'playwright/.auth/user.json'
//   },
//   dependencies: ['setup']
// };
// const webkitConfig = {
//   name: 'webkit',
//   use: { ...devices['Desktop Safari'], storageState: 'playwright/.auth/user.json' },
//   dependencies: ['setup']
// };
// const edgeConfig = {
//   name: 'Edge',
//   use: {
//     ...devices['Desktop Edge'],
//     channel: 'msedge',
//     storageState: 'playwright/.auth/user.json'
//   },
//   dependencies: ['setup']
// };

const defaultConfig: PlaywrightTestConfig = {
  // running more than 1 worker can cause flakiness due to test files being run at the same time in different browsers
  // (e.x. navigation history is incorrect)
  // Additionally, LeapfrogAI API is slow when attaching files to assistants, resulting in flaky tests
  // We can attempt in increase number of browser and workers in the pipeline when the API is faster
  workers: 1,
  timeout: 60000,
  projects: [
    { name: 'setup', testMatch: /global\.setup\.ts/, teardown: 'cleanup' },
    {
      name: 'cleanup',
      testMatch: /global\.teardown\.ts/
    },
    { ...chromeConfig }
  ]
};

// when in dev, create a local webserver
const devConfig: PlaywrightTestConfig = {
  webServer: {
    command: 'npm run build && npm run preview',
    port: PORT,
    stderr: 'pipe'
  },
  testDir: 'tests',
  testMatch: /(.+\.)?(test|spec)\.[jt]s/,
  use: {
    baseURL: 'http://localhost:4173'
  }
};

// when e2e testing, use the deployed instance
const CI_Config: PlaywrightTestConfig = {
  use: {
    baseURL: 'https://ai.uds.dev',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  reporter: [['html', { outputFolder: 'e2e-report' }]]
};

// get the environment type from command line. If none, set it to dev
const environment = process.env.TEST_ENV || 'development';

// config object with default configuration and environment specific configuration
const config: PlaywrightTestConfig = {
  ...defaultConfig,
  ...(environment === 'CI' ? CI_Config : devConfig)
};

export default config;
