import { devices } from '@playwright/test';
import type { PlaywrightTestConfig } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

const defaultConfig: PlaywrightTestConfig = {
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    { name: 'clear_db', testMatch: /.*\clear_db\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Use prepared auth state.
        storageState: 'playwright/.auth/user.json'
      },
      dependencies: ['clear_db', 'setup']
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        // Use prepared auth state.
        storageState: 'playwright/.auth/user.json'
      },
      dependencies: ['clear_db', 'setup']
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['clear_db', 'setup']
    },
    {
      name: 'Edge',
      use: {
        ...devices['Desktop Edge'],
        channel: 'msedge',
        storageState: 'playwright/.auth/user.json'
      },
      dependencies: ['clear_db', 'setup']
    }
  ],
  testDir: 'tests',
  testMatch: /(.+\.)?(test|spec)\.[jt]s/
};

// when in dev, create a local webserver
const devConfig: PlaywrightTestConfig = {
  webServer: {
    command: 'npm run build && npm run preview',
    port: 4173,
    stderr: 'pipe'
  },
  use: {
    baseURL: 'http://localhost:4173'
  }
};

// when e2e testing, use the deployed instance
const CI_Config: PlaywrightTestConfig = {
  use: {
    baseURL: 'http://ai.uds.dev'
  }
};

// get the environment type from command line. If none, set it to dev
const environment = process.env.TEST_ENV || 'dev';

// config object with default configuration and environment specific configuration
const config: PlaywrightTestConfig = {
  ...defaultConfig,
  ...(environment === 'CI' ? CI_Config : devConfig)
};

export default config;
