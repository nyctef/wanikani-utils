drop table if exists public.subjects;

create table public.subjects (
    id int generated always as identity primary key,
    subject_data jsonb
)