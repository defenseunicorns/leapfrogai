import { env } from '$env/dynamic/public';

export const getAssistantAvatarUrl = (file_path: string) =>
  `${env.PUBLIC_SUPABASE_URL}/storage/v1/object/public/assistant_avatars/${file_path}?v=${new Date().getTime()}`;
