# Language islands

A **language island** is a short monologue — 45 to 90 seconds — about a topic
that comes up every single time you speak Spanish to a stranger. You rehearse it
until it needs no construction effort, and then it is simply *there*.

The idea is Boris Shekhtman's (*How to Improve Your Foreign Language
Immediately*). Its value is not that you sound fluent for ninety seconds. It is
that while an island is running, **your working memory is free** — you are not
assembling the sentence you are saying, so you can listen, read the room, and
plan what comes next. That is the whole trick.

## The one rule that decides whether this works

**An island must be built from Spanish you already control.**

It is tempting to write a beautiful paragraph, have it corrected into native-
sounding Spanish, and memorise that. Don't. An island pitched above your level
is worse than no island: you deliver ninety polished seconds, your listener
answers at the level you just advertised, and you collapse. The mismatch costs
you more than halting A1 speech would have.

So the test for every sentence is not *is this good Spanish?* but **could I have
said this myself, and can I answer a follow-up question in the same register?**

That is why the drafts below were checked word by word against `decks/*.tsv`.
Of the 96 distinct words in them, **92 already have cards**. The four that don't
are noted where they appear.

## What goes in `[brackets]`

Islands have to be *true*, or you cannot sustain them. Anywhere below that says
`[like this]` is a guess I made — replace it with the real thing before you
rehearse it, and delete anything that isn't you.

---

## Island 1 — ¿A qué te dedicas?

The one that is guaranteed to come up, every time, forever.

> Soy programador. Trabajo en una empresa tecnológica en Estocolmo.
>
> Empiezo a trabajar a las nueve y trabajo de lunes a viernes. [Voy al trabajo
> en metro], pero a veces trabajo desde casa.
>
> Escribo correos todos los días y tengo muchas reuniones. Mis compañeros
> hablan inglés, pero yo quiero hablar español.
>
> Tengo mucho trabajo, pero me gusta.

*reuniones* is the only word here without its own card — the singular
*una reunión* has one.

**Follow-ups you must survive:** *¿Y te gusta?* · *¿Cuántas horas trabajas?* ·
*¿Trabajas con españoles?* · *¿Es una empresa grande?*

---

## Island 2 — ¿De dónde eres?

For a Swede in Spain this is really a weather island, because the second
question is always about the cold and the dark.

> Soy sueco. Soy de Estocolmo, en Suecia.
>
> En [invierno] hace mucho frío. Hace diez grados bajo cero y está nublado.
> No me gusta el frío, pero me gusta cuando nieva.
>
> En verano hace buen tiempo y los días son muy largos.
>
> Mi familia vive en Suecia. [Mis padres viven cerca.]

*invierno* has no card yet — it is already queued in `WORDBANK.MD` under the
seasons gap, and this is a second reason to add it.

**Follow-ups:** *¿Hace mucho frío?* · *¿Cuánto dura el invierno?* ·
*¿Prefieres España?* · *¿Vienes mucho a España?*

---

## Island 3 — ¿Por qué estudias español?

> Estoy aprendiendo español. Voy a clase dos veces por semana.
>
> Estudio en casa todos los días con una aplicación. Es difícil, pero me gusta
> mucho.
>
> Quiero hablar español porque [me gusta España].
>
> Los fines de semana juego al pádel con mis amigos. También me gusta leer y
> ver [documentales] en español.

*documentales* has no card; the `video::leones` deck is full of the vocabulary
but not the word itself.

**Follow-ups:** *¿Cuánto tiempo llevas estudiando?* · *¿Es difícil?* ·
*¿Dónde estudias?* · *¿Has estado en España?*

---

## The queue — islands still to write

In the order they are likely to be needed:

- [ ] **Tu familia** — who they are, where they live, what they do
- [ ] **Un día normal** — your routine start to finish · `A1::rutina` already
      covers almost all of it
- [ ] **El fin de semana** — padel, reading, what you did last weekend
      · needs the *pretérito perfecto*, which your course has now covered
- [ ] **Tu piso / dónde vives** — the flat, the area, how long you've been there
- [ ] **La comida** — what you eat, what you cook, what you think of Spanish food
- [ ] **Por qué estás aquí** — holiday, work, a course. Changes per trip, so
      write it fresh each time
- [ ] **El pádel** — your own sport, the one topic where you will out-talk the
      textbook

## How to build one — the recording loop

1. **Answer the question cold.** Phone voice memo, no notes, no preparation.
   Keep going even when it falls apart — the falling apart is the data.
2. **Transcribe it.** Type what you actually said, hesitations included, or run
   the audio through Whisper.
3. **Bring it here for correction.** The instruction that matters: *correct this
   without raising the level.* A correction that introduces the subjunctive is
   not a correction, it is a different island you cannot hold.
4. **Rewrite at A1**, with the fixes folded in, and cut it to 45–90 seconds.
5. **Re-record until it needs no thinking.** Out loud, standing up, several
   times across several days. This is the part that is actually the work.
6. **Card the errors, not the island.** See below.

## Where this meets the deck

An island and a flashcard are different objects and should not be confused:

| | Island | Card |
|---|---|---|
| Size | a connected monologue | one teaching point |
| Practised by | saying it out loud | spaced review |
| Goal | automaticity under pressure | recall |
| Lives in | this file, and your mouth | `decks/*.tsv` |

**So islands do not become cards.** What becomes a card is each *error* the
recording exposed — in a new sentence, following the house rules in
`CLAUDE.md`. The island is where you find out which words you cannot reach
under pressure; the deck is where you fix that.

The reverse direction matters too: an island is the first honest test of
whether the deck is working. Anything you cannot say in a monologue, you do not
really have yet, however green the card looks in Anki.
