import { deleteAllGeneratedFixtureFiles, deleteAllTestFilesWithApi } from './fileHelpers';
import { deleteAllAssistants, deleteAssistantAvatars } from './assistantHelpers';
import { deleteAllTestThreadsWithApi } from './threadHelpers';
import type OpenAI from 'openai';
import { deleteAllTestAPIKeys } from './apiHelpers';
import { createClient } from '@supabase/supabase-js';
import { supabaseUsername } from '../constants';

export const cleanup = async (openAIClient: OpenAI) => {
  deleteAllGeneratedFixtureFiles();
  await deleteAllTestFilesWithApi(openAIClient);
  await deleteAllAssistants(openAIClient);
  await deleteAllTestThreadsWithApi(openAIClient);
  await deleteAssistantAvatars();
  await deleteAllTestAPIKeys();
  if (process.env.PUBLIC_DISABLE_KEYCLOAK === 'true') {
    const supabase = createClient(process.env.PUBLIC_SUPABASE_URL!, process.env.SERVICE_ROLE_KEY!, {
      auth: {
        autoRefreshToken: false,
        persistSession: false
      }
    });
    const {
      data: { users }
    } = await supabase.auth.admin.listUsers();
    let userId = '';
    for (const user of users) {
      if (user.email === supabaseUsername) {
        userId = user.id;
      }
    }
    if (userId) {
      await supabase.from('profiles').delete().eq('id', userId);
      const { error } = await supabase.auth.admin.deleteUser(userId);
      if (error) console.error('Error deleting test user', error);
    }
  }
};
