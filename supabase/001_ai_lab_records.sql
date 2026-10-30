-- AI LAB 2.3: Run once in Supabase SQL Editor.
-- Each authenticated user can only access their own records.
create table if not exists public.ai_lab_records (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  category text not null check (category in ('projects','experiments','notes','tasks')),
  payload jsonb not null check (jsonb_typeof(payload) = 'object' and pg_column_size(payload) <= 32768),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists ai_lab_records_user_category_idx on public.ai_lab_records(user_id, category);
alter table public.ai_lab_records enable row level security;
alter table public.ai_lab_records force row level security;
revoke all on public.ai_lab_records from anon;
grant select, insert, update, delete on public.ai_lab_records to authenticated;
drop policy if exists "read own records" on public.ai_lab_records;
create policy "read own records" on public.ai_lab_records for select to authenticated using ((select auth.uid()) = user_id);
drop policy if exists "insert own records" on public.ai_lab_records;
create policy "insert own records" on public.ai_lab_records for insert to authenticated with check ((select auth.uid()) = user_id);
drop policy if exists "update own records" on public.ai_lab_records;
create policy "update own records" on public.ai_lab_records for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
drop policy if exists "delete own records" on public.ai_lab_records;
create policy "delete own records" on public.ai_lab_records for delete to authenticated using ((select auth.uid()) = user_id);
