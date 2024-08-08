-- Disable the foreign key constraint
ALTER TABLE extensions
DROP CONSTRAINT extensions_tenant_external_id_fkey;

-- Update the external_id and name for the realtime tenant
UPDATE tenants
SET external_id = 'supabase-realtime',
    name = 'supabase-realtime'
WHERE external_id = 'realtime-dev'
  AND name = 'realtime-dev';

-- Update the tenant_external_id for the realtime extension
UPDATE extensions
SET tenant_external_id = 'supabase-realtime'
WHERE tenant_external_id = 'realtime-dev';

-- Re-enable the foreign key constraint
ALTER TABLE extensions
ADD CONSTRAINT extensions_tenant_external_id_fkey
FOREIGN KEY (tenant_external_id)
REFERENCES tenants(external_id)
ON DELETE CASCADE;