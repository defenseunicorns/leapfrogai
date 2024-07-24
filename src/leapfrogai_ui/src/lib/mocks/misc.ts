import { faker } from '@faker-js/faker';
import type { Session, SupabaseClient, User } from '@supabase/supabase-js';

type GetLocalsMockParams<T = SupabaseClient> = {
  nullSession?: boolean;
  supabase?: T;
};
export const getLocalsMock = <T = SupabaseClient>(params: GetLocalsMockParams<T> = {}) => {
  const { nullSession = false, supabase = {} as unknown as SupabaseClient } = params;

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
      iss: process.env.SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL,
      name: full_name,
      phone_verified: false,
      provider_id: faker.string.uuid(),
      sub: faker.string.uuid()
    },
    created_at: yesterday.toISOString()
  };

  const session: Session | null = nullSession
    ? null
    : {
        access_token: 'abc',
        refresh_token: 'abc',
        expires_in: 3600,
        token_type: 'bearer',
        user
      };

  return {
    user,
    session,
    safeGetSession: () => Promise.resolve({ session, user }),
    supabase
  };
};
