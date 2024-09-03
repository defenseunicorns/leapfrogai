/*
    avatars and assistant_avatars are different entities
    avatars were never used, but we are keeping assistant_avatars
 */
DELETE FROM storage.buckets
WHERE id = 'avatars';

DROP POLICY IF EXISTS "Avatar images are publicly accessible."
ON storage.objects;

DROP POLICY IF EXISTS "Anyone can update their own avatar."
ON storage.objects;

/*
    Fix assistant_avatars policies
 */

DROP POLICY IF EXISTS "Anyone can update their own assistant avatars."
ON storage.objects;

DO $$
BEGIN

    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Anyone can update their own assistant avatars.')
        THEN create policy "Anyone can update their own assistant avatars." on storage.objects
          for update using (owner = auth.uid() AND bucket_id = 'assistant_avatars');
    END IF;


    IF NOT EXISTS(SELECT 1 FROM pg_policies WHERE schemaname = 'storage'
      AND tablename  = 'objects'
      AND policyname = 'Anyone can delete their own assistant avatars.')
        THEN create policy "Anyone can delete their own assistant avatars." on storage.objects
            for delete using (owner = auth.uid() AND bucket_id = 'assistant_avatars');
    END IF;

END $$;

/*
    Delete any assistant avatars that are no longer attached to assistants.
    First checks for assistants with metadata.avatar fields that are null or empty string, and deletes avatars
    associated with that assistant.
    Second, it looks for any avatar images that don't have assistants in the assistant_objects table.
 */

DO $$
DECLARE
    assistant RECORD;
    orphaned_avatar RECORD;
BEGIN
    FOR assistant IN
        SELECT id, metadata FROM assistant_objects
        WHERE (metadata->>'avatar') IS NULL OR (metadata->>'avatar') = ''
    LOOP
        DELETE FROM storage.objects
        WHERE bucket_id = 'assistant_avatars'
          AND name = assistant.id::text;
    END LOOP;


    FOR orphaned_avatar IN
        SELECT name
        FROM storage.objects
        WHERE bucket_id = 'assistant_avatars'
          AND name NOT IN (SELECT id::text FROM assistant_objects)
    LOOP
        DELETE FROM storage.objects
        WHERE bucket_id = 'assistant_avatars'
          AND name = orphaned_avatar.name;
    END LOOP;
END $$;
