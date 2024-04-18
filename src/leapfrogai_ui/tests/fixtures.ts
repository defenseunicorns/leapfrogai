import { test as base } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

type MyFixtures = {
	clearDb: () => Promise<void>;
};
export const test = base.extend<MyFixtures>({
	clearDb: async ({ page }, use) => {
		console.log('Resetting database...');
		const clearDb = async () => {
			const supabase = createClient(
				process.env.PUBLIC_SUPABASE_URL!,
				process.env.SERVICE_ROLE_KEY!
			);

			await supabase.from('conversations').delete().neq('label', 'delete_all');
			await supabase.from('messages').delete().neq('label', 'delete_all');
		};

		await use(clearDb);
	}
});

export { expect, type Page } from '@playwright/test';
