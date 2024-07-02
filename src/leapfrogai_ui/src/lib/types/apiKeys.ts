export enum PERMISSIONS {
  ALL = 'ALL',
  READ = 'READ',
  WRITE = 'WRITE',
  READ_WRITE = 'READ AND WRITE'
}

export type APIKeyRow = {
  id: string;
  name: string;
  key: string;
  created_at: number;
  expiration: number;
  permissions: PERMISSIONS;
};
