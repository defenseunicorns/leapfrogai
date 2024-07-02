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

export type APIKeysForm = SuperValidated<
  { name: string; expires_at: number },
  any,
  { name: string; expires_at: number }
>;
