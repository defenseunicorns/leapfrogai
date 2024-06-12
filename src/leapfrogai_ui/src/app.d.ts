// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import { Session, SupabaseClient, User } from '@supabase/supabase-js';
import type { LFAssistant } from '$lib/types/assistants';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import type { FileObject } from 'openai/resources/files';

declare global {
  namespace App {
    // interface Error {}
    interface Locals {
      supabase: SupabaseClient;
      safeGetSession(): Promise<{ session: Session | null; user: User | null }>;
    }
    interface PageData {
      title?: string | null;
      session?: Session | null;
      user?: User | null;
      profile?: Profile;
      threads?: LFThread[];
      assistants?: LFAssistant[];
      assistant?: LFAssistant;
      files?: FileObject[];
    }

    // interface PageState {}
    // interface Platform {}
  }
}

export {};
