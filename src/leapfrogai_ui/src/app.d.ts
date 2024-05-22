// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import { Session, SupabaseClient } from '@supabase/supabase-js';
import type { LFAssistant } from '$lib/types/assistants';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';

declare global {
  namespace App {
    // interface Error {}
    interface Locals {
      supabase: SupabaseClient;
      getSession(): Promise<Session | null>;
    }
    interface PageData {
      title?: string | null;
      session?: Session | null;
      profile?: Profile;
      threads?: LFThread[];
      assistants?: LFAssistant[];
      assistant?: LFAssistant;
    }
    // interface PageState {}
    // interface Platform {}
  }
}

export {};
