-- Disable the foreign key constraint
ALTER TABLE _realtime.extensions
DROP CONSTRAINT extensions_tenant_external_id_fkey;

-- Update the external_id and name for the realtime tenant
UPDATE _realtime.tenants
SET external_id = 'supabase-realtime',
    name = 'supabase-realtime'
WHERE external_id = 'realtime-dev'
  AND name = 'realtime-dev';

-- Update the tenant_external_id for the realtime extension
UPDATE _realtime.extensions
SET tenant_external_id = 'supabase-realtime'
WHERE tenant_external_id = 'realtime-dev';

-- Re-enable the foreign key constraint
ALTER TABLE _realtime.extensions
ADD CONSTRAINT extensions_tenant_external_id_fkey
FOREIGN KEY (tenant_external_id)
REFERENCES _realtime.tenants(external_id)
ON DELETE CASCADE;
