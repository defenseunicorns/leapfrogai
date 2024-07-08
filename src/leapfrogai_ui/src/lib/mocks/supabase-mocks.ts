import { faker } from '@faker-js/faker';
import type { PostgrestError, Session, User } from '@supabase/supabase-js';

const internalPostgresError: PostgrestError = {
  code: '500',
  message: 'Internal Error',
  details: '',
  hint: ''
};

export const sessionMock = vi.fn(() => {
  const id = faker.string.uuid();
  const email = faker.internet.email();
  const full_name = faker.person.fullName();
  const currentDate = new Date();
  const yesterday = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    currentDate.getDate() - 1
  );
  const user: User = {
    id,
    aud: 'authenticated',
    role: 'authenticated',
    email,
    app_metadata: { provider: 'keycloak', providers: ['keycloak'] },
    user_metadata: {
      email,
      email_verified: true,
      full_name,
      iss: 'https://keycloak.admin.uds.dev/realms/uds',
      name: full_name,
      phone_verified: false,
      provider_id: faker.string.uuid(),
      sub: faker.string.uuid()
    },
    created_at: yesterday.toISOString()
  };
  return Promise.resolve<{ session: Session | null; user: User | null }>({
    session: {
      access_token: 'abc',
      refresh_token: 'abc',
      expires_in: 3600,
      token_type: 'bearer',
      user
    },
    user
  });
});
export const sessionNullMock = vi.fn(() => Promise.resolve({ session: null, user: null }));

/* ----- Re-usable mock components ----- */

export const selectSingleReturnsMockError = () => ({
  select: vi.fn(() => ({
    eq: vi.fn(() => ({
      returns: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ error: internalPostgresError, data: null }))
      }))
    }))
  }))
});

export const updateSingleReturnsMock = () => ({
  update: vi.fn(() => ({
    eq: vi.fn(() => ({
      returns: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ error: null }))
      }))
    }))
  }))
});

export const supabaseSelectSingleByIdMock = <T>(itemToReturn: T) => ({
  select: vi.fn(() => ({
    eq: vi.fn(() => ({
      returns: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ error: null, data: itemToReturn }))
      }))
    }))
  }))
});

export const supabaseUpdateErrorMock = () => ({
  update: vi.fn(() => ({
    eq: vi.fn(() => Promise.resolve({ error: internalPostgresError }))
  }))
});

export const storageRemoveMock = () => ({
  ...supabaseFromMockWrapper({ remove: vi.fn(() => Promise.resolve({ error: null })) })
});
/* ----- end re-usable mock components */

/* --- Standalone mocks ----- */

export const supabaseFromMockWrapper = (mock: object) => ({
  from: vi.fn(() => ({
    ...mock
  }))
});

export const supabaseStorageMockWrapper = (mock: object) => ({
  storage: {
    ...mock
  }
});

export const supabaseInsertMock = <T>(itemToReturn: T) => ({
  from: vi.fn(() => ({
    insert: vi.fn(() => ({
      select: vi.fn(() => ({
        returns: vi.fn(() => Promise.resolve({ error: null, data: itemToReturn }))
      }))
    }))
  }))
});
export const supabaseInsertSingleMock = <T>(itemToReturn: T) => ({
  from: vi.fn(() => ({
    insert: vi.fn(() => ({
      select: vi.fn(() => ({
        returns: vi.fn(() => ({
          single: vi.fn(() => Promise.resolve({ error: null, data: itemToReturn }))
        }))
      }))
    }))
  }))
});

export const supabaseInsertSingleErrorMock = () => ({
  from: vi.fn(() => ({
    insert: vi.fn(() => ({
      select: vi.fn(() => ({
        returns: vi.fn(() => ({
          single: vi.fn(() => Promise.resolve({ error: internalPostgresError, data: {} }))
        }))
      }))
    }))
  }))
});

/* ----- end standalone mocks ----- */
