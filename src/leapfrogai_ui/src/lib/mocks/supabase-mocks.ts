import { faker } from '@faker-js/faker';

export const sessionMock = vi.fn(() => Promise.resolve({ user: { id: faker.string.uuid() } }));
export const sessionNullMock = vi.fn(() => Promise.resolve(null));

export const supabaseInsertMock = (itemToReturn: any) => ({
	from: vi.fn(() => ({
		insert: vi.fn(() => ({
			select: vi.fn(() => ({
				returns: vi.fn(() => Promise.resolve({ error: null, data: itemToReturn }))
			}))
		}))
	}))
});

export const supabaseUpdateMock = () => ({
	from: vi.fn(() => ({
		update: vi.fn(() => ({
			eq: vi.fn(() => Promise.resolve({ error: null }))
		}))
	}))
});

export const supabaseDeleteMock = () => ({
	from: vi.fn(() => ({
		delete: vi.fn(() => ({ eq: vi.fn(() => Promise.resolve({ error: null })) }))
	}))
});
