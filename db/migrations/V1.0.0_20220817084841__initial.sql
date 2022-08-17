DO language plpgsql $$BEGIN RAISE NOTICE 'Creating public.subjects...';END$$;
CREATE TABLE public.subjects (
    id integer NOT NULL,
    subject_data jsonb NOT NULL
);
ALTER TABLE public.subjects ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


DO language plpgsql $$BEGIN RAISE NOTICE 'Creating public.example_sentences...';END$$;
CREATE MATERIALIZED VIEW public.example_sentences (level, subject, english, japanese) AS WITH data(level, chars, sentence) AS (
         SELECT ((subjects.subject_data -> 'level'::text))::integer AS int4,
            (subjects.subject_data #>> '{characters}'::text[]),
            jsonb_array_elements((subjects.subject_data #> '{context_sentences}'::text[])) AS jsonb_array_elements
           FROM public.subjects
        )
 SELECT data.level,
    data.chars AS subject,
    (data.sentence ->> 'en'::text) AS english,
    (data.sentence ->> 'ja'::text) AS japanese
   FROM data
  ORDER BY data.level, data.chars;
