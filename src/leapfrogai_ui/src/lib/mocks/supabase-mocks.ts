import { faker } from '@faker-js/faker';
import type { PostgrestError, Session } from '@supabase/supabase-js';

const internalPostgresError: PostgrestError = {
  code: '500',
  message: 'Internal Error',
  details: '',
  hint: ''
};

const notFoundPostgresError: PostgrestError = {
  code: '404',
  message: 'Not Found',
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
  return Promise.resolve<Session>({
    access_token: 'abc',
    refresh_token: 'abc',
    expires_in: 3600,
    token_type: 'bearer',
    user: {
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
    }
  });
});
export const sessionNullMock = vi.fn(() => Promise.resolve(null));

/* ----- Re-usable mock components ----- */

export const selectSingleReturnsMock = <T>(itemToReturn: T) => ({
  select: vi.fn(() => ({
    eq: vi.fn(() => ({
      returns: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ error: null, data: itemToReturn }))
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

export const updateSingleErrorMock = () => ({
  update: vi.fn(() => ({
    eq: vi.fn(() => ({
      returns: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ error: internalPostgresError, data: null }))
      }))
    }))
  }))
});

export const selectErrorMock = () => ({
  select: vi.fn(() => ({
    eq: vi.fn(() => ({
      returns: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ error: notFoundPostgresError, data: {} }))
      }))
    }))
  }))
});


/* ----- end re-usable mock components */

/* --- Standalone mocks ----- */

export const supabaseFromMockWrapper = (mock: object) => ({
  from: vi.fn(() => ({
    ...mock
  }))
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

export const supabaseInsertErrorMock = () => ({
  from: vi.fn(() => ({
    insert: vi.fn(() => ({
      select: vi.fn(() => ({
        returns: vi.fn(() => Promise.resolve({ error: internalPostgresError, data: {} }))
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

export const supabaseSelectSingleByIdMock = <T>(itemToReturn: T) => ({
  from: vi.fn(() => ({
    select: vi.fn(() => ({
      eq: vi.fn(() => ({
        returns: vi.fn(() => ({
          single: vi.fn(() => Promise.resolve({ error: null, data: itemToReturn }))
        }))
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

export const supabaseUpdateSingleMock = () => ({
  from: vi.fn(() => ({
    update: vi.fn(() => ({
      eq: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ error: null }))
      }))
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
    delete: vi.fn(() => ({
      eq: vi.fn(() => Promise.resolve({ error: internalPostgresError }))
    }))
  }))
});

/* ----- end standalone mocks ----- */

/* ----- Test specific mocks ----- */

export const editAssistantSupabaseMock = <T>(itemToReturn: T) => ({
  ...supabaseFromMockWrapper({
    ...selectSingleReturnsMock(itemToReturn),
    ...updateSingleReturnsMock()
  }),
  storage: {
    ...supabaseFromMockWrapper({ remove: vi.fn(() => Promise.resolve({ error: null })) })
  }
});

export const editAssistantSupabaseInsertErrorMock = <T>(itemToReturn: T) => ({
  ...supabaseFromMockWrapper({
    ...selectSingleReturnsMock(itemToReturn),
    ...updateSingleErrorMock()
  }),
  storage: {
    ...supabaseFromMockWrapper({ remove: vi.fn(() => Promise.resolve({ error: null })) })
  }
});

/* ----- end test specific mocks */
