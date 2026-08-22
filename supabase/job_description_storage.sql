-- TalentBridge AI private reusable job-description library
-- Run this entire script once in the Supabase SQL Editor.

create extension if not exists pgcrypto;

create table if not exists public.job_descriptions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles(user_id) on delete cascade,
    job_title text not null check (
        length(trim(job_title)) between 1 and 160
    ),
    company_name text not null default '' check (
        length(company_name) <= 160
    ),
    source_url text not null default '' check (
        length(source_url) <= 2048
    ),
    description_text text not null check (
        length(trim(description_text)) between 1 and 50000
    ),
    content_sha256 text not null check (length(content_sha256) = 64),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (user_id, content_sha256)
);

create index if not exists job_descriptions_user_updated_idx
on public.job_descriptions (user_id, updated_at desc);

alter table public.job_descriptions enable row level security;

drop policy if exists "Users can read their own job descriptions"
on public.job_descriptions;
create policy "Users can read their own job descriptions"
on public.job_descriptions for select to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users can insert their own job descriptions"
on public.job_descriptions;
create policy "Users can insert their own job descriptions"
on public.job_descriptions for insert to authenticated
with check ((select auth.uid()) = user_id);

drop policy if exists "Users can update their own job descriptions"
on public.job_descriptions;
create policy "Users can update their own job descriptions"
on public.job_descriptions for update to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

drop policy if exists "Users can delete their own job descriptions"
on public.job_descriptions;
create policy "Users can delete their own job descriptions"
on public.job_descriptions for delete to authenticated
using ((select auth.uid()) = user_id);

create or replace function public.set_job_description_updated_at()
returns trigger
language plpgsql
security invoker
set search_path = ''
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists set_job_descriptions_updated_at
on public.job_descriptions;
create trigger set_job_descriptions_updated_at
before update on public.job_descriptions
for each row execute function public.set_job_description_updated_at();
