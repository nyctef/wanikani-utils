-- grab all example sentences per vocab item
with data(level, chars, sentence) as
(
    select 
        (subject_data -> 'level')::integer,
        subject_data #>> '{characters}',
        jsonb_array_elements(subject_data #> '{context_sentences}')
    from subjects
)
select
    level,
    chars,
    sentence ->> 'en',
    sentence ->> 'ja'
from data
order by level asc, chars asc;