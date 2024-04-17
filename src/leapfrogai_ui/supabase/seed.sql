-- create test users
INSERT INTO
    auth.users (
        instance_id,
        id,
        aud,
        role,
        email,
        encrypted_password,
        email_confirmed_at,
        recovery_sent_at,
        last_sign_in_at,
        raw_app_meta_data,
        raw_user_meta_data,
        created_at,
        updated_at,
        confirmation_token,
        email_change,
        email_change_token_new,
        recovery_token
    ) (
        select
            '00000000-0000-0000-0000-000000000000',
            uuid_generate_v4 (),
            'authenticated',
            'authenticated',
            'user' || (ROW_NUMBER() OVER ()) || '@test.com',
            crypt ('password123', gen_salt ('bf')),
            current_timestamp,
            current_timestamp,
            current_timestamp,
            '{"provider":"email","providers":["email"]}',
            '{}',
            current_timestamp,
            current_timestamp,
            '',
            '',
            '',
            ''
        FROM
            generate_series(1, 3)
    );

-- test user email identities
INSERT INTO
    auth.identities (
        id,
        user_id,
        identity_data,
        provider_id,
        provider,
        last_sign_in_at,
        created_at,
        updated_at
    ) (
        select
            uuid_generate_v4 (),
            id,
            format('{"sub":"%s","email":"%s"}', id::text, email)::jsonb,
            id,
            'email',
            current_timestamp,
            current_timestamp,
            current_timestamp
        from
            auth.users
    );

-- seed conversations
insert into public.conversations (user_id, label)
values(
     (SELECT user_id FROM auth.identities WHERE email = 'user1@test.com'),
     'conversation 1'
);
insert into public.conversations (user_id, label)
values(
     (SELECT user_id FROM auth.identities WHERE email = 'user1@test.com'),
     'conversation 2'
);

-- seed messages
WITH user1 AS (
    SELECT user_id FROM auth.identities WHERE email = 'user1@test.com'
), conversation1 AS (
    SELECT id FROM public.conversations WHERE label = 'conversation 1'
)
INSERT INTO public.messages (user_id, conversation_id, role, content)
VALUES (
    (SELECT user_id FROM user1),
    (SELECT id FROM conversation1),
    'user',
    'What is AI?'
), (
    (SELECT user_id FROM user1),
    (SELECT id FROM conversation1),
    'system',
    'AI is the simulation of human intelligence processes by machines, especially computer systems.'
);

WITH user1 AS (
    SELECT user_id FROM auth.identities WHERE email = 'user1@test.com'
), conversation2 AS (
    SELECT id FROM public.conversations WHERE label = 'conversation 2'
)
INSERT INTO public.messages (user_id, conversation_id, role, content)
VALUES (
    (SELECT user_id FROM user1),
    (SELECT id FROM conversation2),
    'user',
    'What is RAG?'
), (
    (SELECT user_id FROM user1),
    (SELECT id FROM conversation2),
    'system',
    'Retrieval-augmented generation (RAG) is a technique for enhancing the accuracy and reliability of generative AI models with facts fetched from external sources.'
);