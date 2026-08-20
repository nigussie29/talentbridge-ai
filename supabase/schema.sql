-- TalentBridge AI authentication foundation
-- Run this entire script in the Supabase SQL Editor once.

create table if not exists public.profiles (
    user_id uuid primary key references auth.users(id) on delete cascade,
    email text not null,
    display_name text not null,
    role text not null default 'Job Seeker'
        check (role in ('Admin', 'Job Seeker', 'HR / Recruiter', 'Training Center')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

drop policy if exists "Users can read their own profile" on public.profiles;
create policy "Users can read their own profile"
on public.profiles
for select
to authenticated
using ((select auth.uid()) = user_id);

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
    insert into public.profiles (user_id, email, display_name, role)
    values (
        new.id,
        coalesce(new.email, ''),
        coalesce(new.raw_user_meta_data ->> 'display_name', split_part(coalesce(new.email, ''), '@', 1)),
        'Job Seeker'
    )
    on conflict (user_id) do nothing;
    return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();
