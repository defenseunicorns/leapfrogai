DO $$
BEGIN
    BEGIN
        DROP TABLE IF EXISTS messages;
    END;

    BEGIN
        DROP TABLE IF EXISTS conversations;
    END;
END $$;

-- Drop the existing trigger
drop trigger if exists on_auth_user_created on auth.users;

-- Drop the existing function
drop function if exists public.handle_new_user();

-- Create the new function without the avatar_url field
create function public.handle_new_user()
    returns trigger as $$
begin
insert into public.profiles (id, full_name)
values (new.id, new.raw_user_meta_data->>'full_name');
return new;
end;
$$ language plpgsql security definer;

-- Recreate the trigger
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();