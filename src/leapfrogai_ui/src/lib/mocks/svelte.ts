import { type Readable, readable } from 'svelte/store';
import type { Navigation, Page } from '@sveltejs/kit';
import { fakeConversations } from '../../testUtils/fakeData';
import { faker } from '@faker-js/faker';

type GetStoresOverrides = {
	url: string;
	params: Record<string, string>;
};

export const getStores = (
	options: GetStoresOverrides = { url: 'http://localhost', params: {} }
) => {
	const navigating = readable<Navigation | null>(null);
	const page = readable<Page>({
		url: new URL(options.url),
		params: options.params,
		route: { id: null },
		status: 200,
		error: null,
		// TODO - the profile and session types are incompletely mocked out
		data: {
			conversations: fakeConversations,
			profile: {},
			session: { user: { id: faker.string.uuid() } }
		},
		state: {},
		form: null
	});
	const updated: Readable<boolean> & { check(): Promise<boolean> } = {
		subscribe: readable(false).subscribe,
		check: () => Promise.resolve(false)
	};

	return { navigating, page, updated };
};
