drop table if exists public.subjects;

create table public.subjects (
    id int NOT NULL primary key,
    subject_data jsonb NOT NULL
);