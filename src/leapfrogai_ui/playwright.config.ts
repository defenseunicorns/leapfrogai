import { devices } from '@playwright/test';
import type { PlaywrightTestConfig } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

const config: PlaywrightTestConfig = {
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
  webServer: {
    command: 'npm run build && npm run preview',
    port: 4173,
    stderr: 'pipe'
  },
  testDir: 'tests',
  testMatch: /(.+\.)?(test|spec)\.[jt]s/
};

export default config;
