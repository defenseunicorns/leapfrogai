import type { SuperValidated } from 'sveltekit-superforms';

export enum PERMISSIONS {
  ALL = 'ALL',
  READ = 'READ',
  WRITE = 'WRITE',
  READ_WRITE = 'READ AND WRITE'
}

export type APIKeyRow = {
  id: string;
  name: string;
  api_key: string;
  created_at: number;
  expires_at: number;
  permissions: PERMISSIONS;
};

export type NewApiKeyInput = {
  name?: string;
  expires_at: number;
};

// This type is taken from SuperValidated, leaving the any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type APIKeysForm = SuperValidated<NewApiKeyInput, any, NewApiKeyInput>;
