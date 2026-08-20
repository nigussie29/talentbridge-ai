-- TalentBridge AI saved analyses and skill progress
-- Run this entire script once in the Supabase SQL Editor.

create extension if not exists pgcrypto;

create table if not exists public.job_analyses (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles(user_id) on delete cascade,
    target_career text not null,
    user_mode text not null
        check (user_mode in ('Admin', 'Job Seeker', 'HR / Recruiter', 'Training Center')),
    match_score numeric(5, 2) not null check (match_score between 0 and 100),
    semantic_match_score numeric(5, 2) not null
        check (semantic_match_score between 0 and 100),
    result_data jsonb not null,
    created_at timestamptz not null default now()
);

create index if not exists job_analyses_user_created_idx
on public.job_analyses (user_id, created_at desc);

alter table public.job_analyses enable row level security;

drop policy if exists "Users can read their own analyses" on public.job_analyses;
create policy "Users can read their own analyses"
on public.job_analyses for select to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users can insert their own analyses" on public.job_analyses;
create policy "Users can insert their own analyses"
on public.job_analyses for insert to authenticated
with check ((select auth.uid()) = user_id);

drop policy if exists "Users can delete their own analyses" on public.job_analyses;
create policy "Users can delete their own analyses"
on public.job_analyses for delete to authenticated
using ((select auth.uid()) = user_id);

create table if not exists public.skill_progress (
    id uuid primary key default gen_random_uuid(),
    analysis_id uuid not null references public.job_analyses(id) on delete cascade,
    user_id uuid not null references public.profiles(user_id) on delete cascade,
    skill text not null,
    evidence_url text not null default '',
    status text not null default 'Not Started'
        check (status in ('Not Started', 'In Progress', 'Completed')),
    updated_at timestamptz not null default now(),
    unique (analysis_id, skill)
);

create index if not exists skill_progress_user_analysis_idx
on public.skill_progress (user_id, analysis_id);

alter table public.skill_progress enable row level security;

drop policy if exists "Users can read their own progress" on public.skill_progress;
create policy "Users can read their own progress"
on public.skill_progress for select to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users can insert their own progress" on public.skill_progress;
create policy "Users can insert their own progress"
on public.skill_progress for insert to authenticated
with check (
    (select auth.uid()) = user_id
    and exists (
        select 1 from public.job_analyses
        where job_analyses.id = analysis_id
          and job_analyses.user_id = (select auth.uid())
    )
);

drop policy if exists "Users can update their own progress" on public.skill_progress;
create policy "Users can update their own progress"
on public.skill_progress for update to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);
