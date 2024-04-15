import { faker } from '@faker-js/faker';
import type { PostgrestError } from '@supabase/supabase-js';

const internalPostgresError: PostgrestError = {
	code: '500',
	message: 'Internal Error',
	details: '',
	hint: ''
};

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

export const supabaseInsertErrorMock = () => ({
	from: vi.fn(() => ({
		insert: vi.fn(() => ({
			select: vi.fn(() => ({
				returns: vi.fn(() => Promise.resolve({ error: internalPostgresError, data: {} }))
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

export const supabaseUpdateErrorMock = () => ({
	from: vi.fn(() => ({
		update: vi.fn(() => ({
			eq: vi.fn(() => Promise.resolve({ error: internalPostgresError }))
		}))
	}))
});

export const supabaseDeleteMock = () => ({
	from: vi.fn(() => ({
		delete: vi.fn(() => ({ eq: vi.fn(() => Promise.resolve({ error: null })) }))
	}))
});

export const supabaseDeleteErrorMock = () => ({
	from: vi.fn(() => ({
		delete: vi.fn(() => ({ eq: vi.fn(() => Promise.resolve({ error: internalPostgresError })) }))
	}))
});
