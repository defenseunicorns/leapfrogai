import { test as base } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

type MyFixtures = {
  clearDbData: () => Promise<void>;
};
export const test = base.extend<MyFixtures>({
  // eslint-disable-next-line  no-empty-pattern
  clearDbData: async ({}, use) => {
    const clearDbData = async () => {
      const supabase = createClient(
        process.env.PUBLIC_SUPABASE_URL!,
        process.env.SERVICE_ROLE_KEY!
      );

      await supabase.from('conversations').delete().neq('label', 'delete_all');
      await supabase.from('assistants').delete().neq('name', 'delete_all');
    };

    await use(clearDbData);
  }
});

export { expect, type Page } from '@playwright/test';
