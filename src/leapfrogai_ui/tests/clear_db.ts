import { test as setup } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

setup('clear db', async () => {
  console.log('Resetting database...');
  const supabase = createClient(process.env.PUBLIC_SUPABASE_URL!, process.env.SERVICE_ROLE_KEY!);

  await supabase.from('conversations').delete().neq('label', 'delete_all');
  await supabase.from('messages').delete().neq('label', 'delete_all');
});
