create policy "Individuals can CRUD storage.objects via API key."
    on storage.objects for all
    to anon
    using
    (
        exists (
            select 1
            from api_keys
            where api_keys.api_key_hash = crypt(current_setting('request.headers')::json->>'x-custom-api-key', api_keys.api_key_hash)
        )
    );
