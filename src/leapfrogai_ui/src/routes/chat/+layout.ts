import { browser } from '$app/environment';
import { threadsStore } from '$stores';

// Load the store with the threads fetched by the +layout.server.ts (set store on the client side only)
// This only runs when the app is first loaded (because it's a higher level layout)
// After this load, the app keeps the store in sync with data changes and we don't
// re-fetch all that data from the server
export const load = async ({ data }) => {
  if (browser) {
    threadsStore.setThreads(data?.threads || []);
  }
};
