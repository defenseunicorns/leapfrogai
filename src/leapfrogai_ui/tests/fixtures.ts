import { test as base } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

type MyFixtures = {
	clearAllConversations: () => Promise<void>;
};
export const test = base.extend<MyFixtures>({
	clearAllConversations: async (_, use) => {
		const clearAllConversations = async () => {
			const supabase = createClient(
				process.env.PUBLIC_SUPABASE_URL!,
				process.env.SERVICE_ROLE_KEY!
			);

			await supabase.from('conversations').delete().neq('label', 'delete_all');
		};

		await use(clearAllConversations);
	}
});

export { expect, type Page } from '@playwright/test';
