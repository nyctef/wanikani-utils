DO language plpgsql $$BEGIN RAISE NOTICE 'Creating public.radical_from_id(integer)...';END$$;
CREATE FUNCTION public.radical_from_id(IN id integer)
RETURNS text
LANGUAGE sql
AS $_$
    select subject_data ->> 'slug'
    from subjects
    where id = $1
$_$;


DO language plpgsql $$BEGIN RAISE NOTICE 'Creating public.kanji_by_wk_radicals...';END$$;
CREATE MATERIALIZED VIEW public.kanji_by_wk_radicals (id, characters, components) AS SELECT x.id,
    x.characters,
    x.components
   FROM ( SELECT subjects.id,
            (subjects.subject_data ->> 'characters'::text),
            ARRAY( SELECT public.radical_from_id((x_1.value)::integer) AS radical_from_id
                   FROM jsonb_array_elements((subjects.subject_data -> 'component_subject_ids'::text)) x_1(value)) AS "array"
           FROM public.subjects
          WHERE ((subjects.subject_data -> 'visually_similar_subject_ids'::text) <> 'null'::jsonb)) x(id, characters, components)
  WHERE (array_length(x.components, 1) <> 0)
  ORDER BY x.id;

DO language plpgsql $$BEGIN RAISE NOTICE 'Creating public.idx_kanji_by_wk_radicals_components...';END$$;
CREATE INDEX idx_kanji_by_wk_radicals_components ON public.kanji_by_wk_radicals USING gin (components);

