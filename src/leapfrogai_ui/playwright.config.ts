import { devices } from '@playwright/test';
import type { PlaywrightTestConfig } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

// TODO - see if we can get all browsers working
const config: PlaywrightTestConfig = {
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Use prepared auth state.
        storageState: 'playwright/.auth/user.json'
      },
      dependencies: ['setup']
    }
    // Leapfrog API currently has too many timeout issues resulting in flaky tests right now due to slow response times
    // We can re-enable other browsers when the API is faster
    // {
    //   name: 'firefox',
    //   use: {
    //     ...devices['Desktop Firefox'],
    //     // Use prepared auth state.
    //     storageState: 'playwright/.auth/user.json'
    //   },
    //   dependencies: ['setup']
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'], storageState: 'playwright/.auth/user.json' },
    //   dependencies: ['setup']
    // },
    // {
    //   name: 'Edge',
    //   use: {
    //     ...devices['Desktop Edge'],
    //     channel: 'msedge',
    //     storageState: 'playwright/.auth/user.json'
    //   },
    //   dependencies: ['setup']
    // }
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
