// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import { Session, SupabaseClient, User } from '@supabase/supabase-js';
import type { LFAssistant } from '$lib/types/assistants';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import type { FileObject } from 'openai/resources/files';
import type { APIKeyRow } from '$lib/types/apiKeys';

declare global {
  namespace App {
    // interface Error {}
    interface Locals {
      supabase: SupabaseClient;
      safeGetSession: () => Promise<{ session: Session | null; user: User | null }>;
      session: Session | null;
      user: User | null;
      isUsingOpenAI: boolean;
    }
    interface PageData {
      session: Session | null;
      title?: string | null;
      profile?: Profile;
      threads?: LFThread[];
      assistants?: LFAssistant[];
      files?: FileObject[];
      keys?: APIKeyRow[];
    }

    // interface PageState {}
    // interface Platform {}
  }
}

export {};
