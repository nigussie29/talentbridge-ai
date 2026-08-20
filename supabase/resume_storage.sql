-- TalentBridge AI private PDF resume storage
-- Run this entire script once in the Supabase SQL Editor.

create extension if not exists pgcrypto;

create table if not exists public.resume_documents (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles(user_id) on delete cascade,
    original_name text not null,
    storage_path text not null unique,
    byte_size bigint not null check (byte_size > 0 and byte_size <= 5242880),
    content_sha256 text not null check (length(content_sha256) = 64),
    created_at timestamptz not null default now(),
    unique (user_id, content_sha256)
);

create index if not exists resume_documents_user_created_idx
on public.resume_documents (user_id, created_at desc);

alter table public.resume_documents enable row level security;

drop policy if exists "Users can read their own resume metadata"
on public.resume_documents;
create policy "Users can read their own resume metadata"
on public.resume_documents for select to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users can insert their own resume metadata"
on public.resume_documents;
create policy "Users can insert their own resume metadata"
on public.resume_documents for insert to authenticated
with check (
    (select auth.uid()) = user_id
    and split_part(storage_path, '/', 1) = (select auth.uid()::text)
);

drop policy if exists "Users can delete their own resume metadata"
on public.resume_documents;
create policy "Users can delete their own resume metadata"
on public.resume_documents for delete to authenticated
using ((select auth.uid()) = user_id);

insert into storage.buckets (
    id,
    name,
    public,
    file_size_limit,
    allowed_mime_types
)
values (
    'resumes',
    'resumes',
    false,
    5242880,
    array['application/pdf']::text[]
)
on conflict (id) do update set
    public = false,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "Users can upload their own resume files"
on storage.objects;
create policy "Users can upload their own resume files"
on storage.objects for insert to authenticated
with check (
    bucket_id = 'resumes'
    and (storage.foldername(name))[1] = (select auth.uid()::text)
);

drop policy if exists "Users can read their own resume files"
on storage.objects;
create policy "Users can read their own resume files"
on storage.objects for select to authenticated
using (
    bucket_id = 'resumes'
    and (storage.foldername(name))[1] = (select auth.uid()::text)
);

drop policy if exists "Users can delete their own resume files"
on storage.objects;
create policy "Users can delete their own resume files"
on storage.objects for delete to authenticated
using (
    bucket_id = 'resumes'
    and (storage.foldername(name))[1] = (select auth.uid()::text)
);
