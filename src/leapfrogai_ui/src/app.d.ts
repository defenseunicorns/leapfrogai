// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import { SupabaseClient, Session } from '@supabase/supabase-js';

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			supabase: SupabaseClient;
			getSession(): Promise<Session | null>;
		}
		interface PageData {
			title?: string | null;
			session: Session | null;
			// TODO - add profile type
			// profile?: any;
			conversations?: Conversation[];
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
