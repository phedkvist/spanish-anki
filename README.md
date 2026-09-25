# Spanish A1 — Anki deck system

Four `.tsv` files, all the same shape as the original verb deck:

```
Front <TAB> Back <TAB> Tags
```

| File | Cards | Card type | Direction |
|---|---|---|---|
| `spanish_A1_verbs_anki.tsv` | 169 | 2. Verb drills | fill-in-the-blank + EN→ES |
| `spanish_A1_vocab_anki.tsv` | 201 | 1. Core vocabulary | **EN → ES** (production) |
| `spanish_A1_grammar_anki.tsv` | 135 | 3. Transformations | instruction → ES |
| `spanish_A1_sentences_anki.tsv` | 152 | 4. Understand the sentence | **ES → EN** + breakdown |
| `spanish_A1_topics_anki.tsv` | 80 | 1. Core vocabulary (topic sets) | **EN → ES** (production) |
| `spanish_A2_pasado_anki.tsv` | 79 | 2. Verb drills (pretérito) | fill-in-the-blank + EN→ES |
| | **816** | | |

`spanish_A1_topics_anki.tsv` is eight themed blocks of ten, meant to be
imported as one batch: `A1::clima` (weather), `A1::numeros-100` (0–100),
`A1::numeros-grandes` (100–1,000,000), `A1::hora` (time of day), `A1::cafe` (ordering at a cafe or restaurant),
`A1::expresiones-tiempo` (now, soon, always, never...), `A1::asignaturas`
(school subjects) and `A1::gustar-personas` (a mis amigos les gusta...).

Every card follows the production-first rule: the three generated decks are
English-prompt → Spanish-answer, except the sentence deck, which is
deliberately Spanish → English because its job is building comprehension.

## Importing

1. **Tools → Manage Note Types → Add → Basic**, name it whatever you like
   (the stock `Basic` works fine — these files use only Front/Back).
2. **File → Import**, pick a `.tsv`.
3. Set **Type** to Basic and **Deck** to the subdeck you want, e.g.
   `Spanish A1::Vocabulary`.
4. Field mapping is positional: Field 1 → Front, Field 2 → Back, Field 3 → Tags.
5. Leave **Allow HTML in fields** ticked — the grey hint line under each
   answer uses `<br>` and `<span>`.

The files carry `#separator:tab` and `#html:true` headers, so recent Anki
versions get the parsing right without you touching the dialog.

## Tags

Hierarchical, extending the `A1::` convention from the verb deck:

```
A1::vocab      A1::numeros A1::tiempo A1::familia A1::comida A1::casa
               A1::trabajo A1::viajes A1::ocio A1::adjetivos A1::verbos
A1::grammar    A1::persona A1::negacion A1::preguntas A1::genero
               A1::ser-estar A1::hay-estar A1::gustar A1::perifrasis
               A1::determinantes A1::reflexivos A1::cantidad
A1::topics     A1::clima A1::numeros-100 A1::numeros-grandes
               A1::hora A1::cafe A1::expresiones-tiempo
               A1::asignaturas A1::gustar-personas
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

Don't record anything — use Anki's built-in TTS. Edit the card template
(**Cards…** on the note type) and add to the back template:

```
{{Back}}
{{tts es_ES voices=Apple_Mónica:Front}}
```

On the sentence deck the Spanish is on the *front*, so put the tag in the
front template there instead. Run **Tools → Check Media** if a voice is
missing; macOS ships Mónica (Spain) and Paulina (Mexico) under
System Settings → Accessibility → Spoken Content → System Voice → Manage.

## Pacing

10–15 new cards/day, mixing all four decks, is the intended rate — roughly
six weeks to work through what's here. Don't unlock everything at once:
set **Deck options → New cards/day** per subdeck.

## Adding cards

Edit `build_anki.py` and re-run:

```bash
python3 build_anki.py
```

It regenerates all six files, the verb deck included. The verb deck is written
first, and any later card whose Front repeats one of its Fronts is skipped, so
the decks can't collide.
`poster.html` / `poster.pdf` are separate and built by hand.

## Posters

Five A4 wall charts. The four verb charts carry the same 45 verbs in the same
grid order, so they read as a set: rows 1–4 are the 20 core A1 verbs, rows 5–6
ten more high-frequency ones, row 7 the stem-changers (volver, empezar, jugar,
pensar, pedir) and rows 8–9 ten everyday verbs (correr, nadar, llamar, llegar,
mirar, creer, aprender, oír, seguir, leer):

| File | Tense | Structure |
|---|---|---|
| `poster.pdf` / `.png` | present indicative | 45 conjugation tables |
| `poster-futuro.pdf` / `.png` | futuro simple | 45 conjugation tables |
| `poster-futuro-proximo.pdf` / `.png` | futuro próximo | `ir` conjugated once + 45 example sentences |
| `poster-pasado.pdf` / `.png` | pretérito indefinido | 45 conjugation tables |
| `poster-pronombres.pdf` / `.png` | — | articles and pronouns: el/los, me/nos/le, lo/la, se |

The near-future poster is deliberately shaped differently: that tense has no
per-verb conjugation to learn (only `ir` changes), so the page spends its
space on usage examples instead of thirty near-identical tables.

Re-render either after editing its `.html`:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf=poster-futuro.pdf poster-futuro.html
```

Each page is sized to fill A4 exactly with no slack — add a verb or lengthen
a gloss and it spills to a second page. Pull it back by reducing `.verb`
padding or the table `line-height`. To check a page still fits, re-render and
compare `document.body.scrollHeight` with `clientHeight`, and make sure the
footer's own bounding box ends above 1123px.
