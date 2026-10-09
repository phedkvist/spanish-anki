# Spanish A1 — Anki deck system

`CONTENT.MD` tracks what's covered and what to add when your course reaches it.

```
CLAUDE.md            house style for writing cards (read by Claude Code)
build_anki.py        one source of truth for every card; run it to rebuild
CONTENT.MD           what's covered, and what to add when the course gets there
LANGUAGE_TRANSFER.MD checklist for the 90-track Complete Spanish audio course
WORDBANK.MD          words the collection is missing, to pull from when adding cards
decks/               the .tsv files you import into Anki
notetypes/           the two note types: fields, templates, styling
posters/             wall charts: .html source next to its .pdf and .png
render_posters.sh    re-renders the posters and checks they still fit A4
backups/             point-in-time Anki collection exports (scheduling)
```

Six `.tsv` files in `decks/`, four columns each:

```
Front <TAB> Back <TAB> Note <TAB> Tags
```

`Note` is the grey gloss under the answer — a translation, then the rule. It
sits in its own field so `{{tts}}` can read the Spanish without reading the
English explanation after it. See `notetypes/`.

| File | Cards | Card type | Direction |
|---|---|---|---|
| `spanish_A1_verbs_anki.tsv` | 188 | 2. Verb drills | fill-in-the-blank + EN→ES |
| `spanish_A1_vocab_anki.tsv` | 201 | 1. Core vocabulary | **EN → ES** (production) |
| `spanish_A1_grammar_anki.tsv` | 162 | 3. Transformations | instruction → ES |
| `spanish_A1_sentences_anki.tsv` | 152 | 4. Understand the sentence | **ES → EN** + breakdown |
| `spanish_A1_topics_anki.tsv` | 184 | 1. Core vocabulary (topic sets) | **EN → ES** (production) |
| `spanish_A2_pasado_anki.tsv` | 79 | 2. Verb drills (pretérito) | fill-in-the-blank + EN→ES |
| `video_leones_anki.tsv` | 25 | 5. Pre-watch vocabulary | **ES → EN** (comprehension) |
| | **1013** | | |

`spanish_A1_topics_anki.tsv` is fourteen themed blocks, meant to be
imported as one batch: `A1::clima` (weather), `A1::numeros-100` (0–100),
`A1::numeros-grandes` (100–1,000,000), `A1::hora` (time of day), `A1::cafe` (ordering at a cafe or restaurant),
`A1::expresiones-tiempo` (now, soon, always, never...), `A1::asignaturas`
(school subjects), `A1::gustar-personas` (a mis amigos les gusta...),
`A1::fechas` (years and dates), `A1::pronombres-objeto` (lo veo, las tengo),
`A1::lugar` (encima de, al lado de...), `A1::salud` (me duele la cabeza) and
`A1::colores` and `A1::horario` (the school timetable).

Every card follows the production-first rule: the three generated decks are
English-prompt → Spanish-answer, except the sentence deck, which is
deliberately Spanish → English because its job is building comprehension.

## Importing

The files carry `#separator:tab`, `#html:true`, `#notetype:` and
`#tags column:4` headers, so recent Anki versions need nothing set by hand.

1. Create the two note types first — see `notetypes/README.md`.
2. **File → Import**, pick a `.tsv` from `decks/`, choose the deck.
3. Leave **Existing notes: Update** selected. Anki matches on the first field,
   so re-importing updates cards in place and never touches their scheduling.

Columns map positionally: 1 → Front, 2 → Back, 3 → Note, 4 → Tags.

## Tags

Hierarchical, extending the `A1::` convention from the verb deck:

```
A1::vocab      A1::numeros A1::tiempo A1::familia A1::comida A1::casa
               A1::trabajo A1::viajes A1::ocio A1::adjetivos A1::verbos
A1::grammar    A1::persona A1::negacion A1::preguntas A1::genero
               A1::ser-estar A1::hay-estar A1::gustar A1::perifrasis
               A1::determinantes A1::reflexivos A1::cantidad A1::perfecto
A1::topics     A1::clima A1::numeros-100 A1::numeros-grandes
               A1::hora A1::cafe A1::expresiones-tiempo
               A1::asignaturas A1::gustar-personas A1::fechas
               A1::pronombres-objeto A1::lugar A1::salud A1::colores
               A1::horario A1::coloquial
A1::sentences  A1::saludos A1::opiniones A1::rutina A1::compras
               A1::restaurante A1::viajes A1::salud A1::clase
               A1::planes A1::practico A1::movil A1::expresiones

A2::verbs      A2::pasado + one tag per verb (A2::tener, A2::ser ...)
A2::translation
```

Level lives in the tag and the filename, not in a separate deck: A2 cards are
imported into the same subdecks as their A1 counterparts, so reviews stay
mixed. `tag:A2::pasado` pulls the whole past tense into a filtered deck.

This lets you build filtered decks like `tag:A1::ser-estar` when one topic
refuses to stick.

## Audio

No recordings and no media files: Anki speaks the Spanish with the system
voice, through the `{{tts}}` tag already in the templates in `notetypes/`.

```
{{tts es_ES voices=Apple_Mónica:Back}}     production cards - Spanish is the answer
{{tts es_ES voices=Apple_Mónica:Front}}    sentence cards - Spanish is the question
```

macOS ships Mónica (Spain) and Paulina (Mexico) under System Settings →
Accessibility → Spoken Content → System Voice → Manage Voices. AnkiMobile and
AnkiDroid use their own voices with the same tag.

## Pacing

10–15 new cards/day, mixing all four decks, is the intended rate — roughly
six weeks to work through what's here. Don't unlock everything at once:
set **Deck options → New cards/day** per subdeck.

## Adding cards

Edit `build_anki.py` and re-run:

```bash
python3 build_anki.py
```

It regenerates all seven files in `decks/`, the verb deck included. The verb deck
is written first, and any later card whose Front repeats one of its Fronts is skipped, so
the decks can't collide.
The posters live in `posters/` and are rendered by `./render_posters.sh`.

`CONTENT.MD` is the running inventory: every block that exists, with its tag and
card count, and the blocks queued up for when the course reaches them. Update it
whenever cards are added.

## Posters

Five wall charts. The four verb charts carry the same 50 verbs in the same grid
order, so they read as a set: rows 1–4 are the 20 core A1 verbs, rows 5–6 ten
more high-frequency ones, row 7 the stem-changers (volver, empezar, jugar,
pensar, pedir), rows 8–9 ten everyday verbs (correr, nadar, llamar, llegar,
mirar, creer, aprender, oír, seguir, leer) and row 10 the five most frequent
verbs the collection was missing (pasar, dejar, quedar, parecer, deber).

Each verb chart prints as **two A4 pages** of five rows — one page of 50 verbs
meant 5.9pt tables, which is too small to read off a wall:

| File | Tense | Structure |
|---|---|---|
| `posters/poster.pdf` / `.png` | present indicative | 50 conjugation tables, 2 pages |
| `posters/poster-futuro.pdf` / `.png` | futuro simple | 50 conjugation tables + a worked build-up, 2 pages |
| `posters/poster-futuro-proximo.pdf` / `.png` | futuro próximo | `ir` conjugated once + 50 example sentences, 2 pages |
| `posters/poster-pasado.pdf` / `.png` | pretérito indefinido | 50 conjugation tables + a worked -ar/-er/-ir example, 2 pages |
| `posters/poster-pronombres.pdf` / `.png` | — | articles and pronouns: el/los, me/nos/le, lo/la, se |

The near-future poster is deliberately shaped differently: that tense has no
per-verb conjugation to learn (only `ir` changes), so the page spends its
space on usage examples instead of thirty near-identical tables.

Re-render after editing a `.html`:

```bash
./render_posters.sh                # all of them
./render_posters.sh poster-pasado  # just one
```

The script writes the `.pdf` and `.png` next to the source and checks two
things: the page count matches the number of `<section class="page">` blocks in
the file, and the grid actually rendered. The second check exists because the
grids are built by JavaScript — a thrown exception leaves pages that are the
right size and completely empty.

Each page is sized to fill A4 exactly with no slack — add a verb or lengthen
a gloss and it spills to a second page. Pull it back by reducing `.verb`
padding or the table `line-height`.
