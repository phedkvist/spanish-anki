# What's covered, and what's next

A running inventory of the collection, so neither of us has to re-derive it.
Update it whenever cards are added. Card counts come from `python3 build_anki.py`.

**Rule of thumb:** add a block when the course reaches it. Cards for grammar you
haven't met yet are the least efficient cards in the collection — you end up
learning the card rather than the rule, and the daily review count grows for
nothing.

Levels follow the Instituto Cervantes syllabus (Spain). Level lives in the tag
and the filename, never in a separate deck, so reviews stay mixed.

---

## Covered — A1

### Grammar

| Structure | Where | Cards |
|---|---|---|
| Present indicative, regular and irregular | `A1::verbs`, poster | 129 |
| Person swaps (yo → él → nosotros …) | `A1::persona` | 20 |
| Negation, incl. nunca / nada / nadie / tampoco | `A1::negacion` | 15 |
| Questions and question words | `A1::preguntas` | 15 |
| Gender and number agreement | `A1::genero` | 12 |
| ser vs estar | `A1::ser-estar` | 15 |
| hay vs está | `A1::hay-estar` | 8 |
| gustar, incl. *a mis amigos les gusta* | `A1::gustar`, `A1::gustar-personas` | 20 |
| ir a + infinitive, tener que, poder, querer | `A1::perifrasis` | 12 |
| Articles, possessives, demonstratives, al / del | `A1::determinantes` | 10 |
| Reflexive verbs | `A1::reflexivos` | 8 |
| muy / mucho, comparatives | `A1::cantidad` | 10 |
| Object pronouns lo / la / los / las / me / te / le / nos / les | `A1::pronombres-objeto` | 21 |
| **Pretérito perfecto** (he comido, ¿has visto?) | `A1::perfecto` | 26 |

### Vocabulary and topics

| Topic | Tag | Cards |
|---|---|---|
| Weather | `A1::clima` | 10 |
| Numbers 0–100 | `A1::numeros-100` | 10 |
| Numbers 100–1,000,000 | `A1::numeros-grandes` | 10 |
| Telling the time | `A1::hora` | 10 |
| Café and restaurant | `A1::cafe` | 10 |
| Time expressions (ahora mismo, siempre, a veces …) | `A1::expresiones-tiempo` | 10 |
| School subjects | `A1::asignaturas` | 10 |
| Years and dates | `A1::fechas` | 10 |
| Where things are (encima de, al lado de …) | `A1::lugar` | 12 |
| Health (me duele …) | `A1::salud` | 10 |
| Colours | `A1::colores` | 10 |
| School timetable (asking and answering) | `A1::horario` | 12 |

Plus the broader vocabulary deck (201 cards): family, house, food, clothes,
transport, places in town, work, travel, shopping, hobbies, adjectives — and
152 Spanish → English sentences for comprehension.

## Covered — A2

| Structure | Where | Cards |
|---|---|---|
| Pretérito indefinido (the finished past) | `A2::pasado`, poster | 79 |

Added ahead of the course. If it feels heavy, search `tag:A2::pasado`, select
all and **Suspend** — scheduling is kept, and it comes back when you're ready.

---

## Add when the course gets there — A1

Ordered by how soon they're likely to come up.

| # | Block | Tag | Cards | What it covers |
|---|---|---|---|---|
| 1 | **estar + gerundio** | `A1::gerundio` | ~10 | *estoy trabajando*, and the trap: Spanish uses the plain present where English uses -ing (*mañana voy*, not *estoy yendo*). |
| 2 | **Imperative (affirmative tú)** | `A1::imperativo` | ~10 | *perdona, oye, mira, dime, toma, ven* — the handful of forms you need to get someone's attention politely. |
| 3 | **por vs para** | `A1::por-para` | ~15 | Only incidental coverage now. A top-five confusion for English speakers. |
| 4 | **Noun gender drills** | `A1::genero-nombres` | ~30 | *la mesa, el problema, la mano* — only if agreement is still shaky. Currently gender is absorbed from sentences, which is slow. |

## Add when the course gets there — A2

| # | Block | Tag | Cards | What it covers |
|---|---|---|---|---|
| 5 | **Imperfecto** | `A2::imperfecto` | ~20 | *era, tenía, había, estaba* — only three irregulars in the whole tense (ser, ir, ver). |
| 6 | **Indefinido vs imperfecto** | `A2::pasados` | ~20 | *fue* vs *era*, *tuve* vs *tenía*. The central A2 decision, and it needs block 5 first. |
| 7 | **Futuro simple** | `A2::futuro` | ~15 | *hablaré, tendré, habrá*. The poster exists already; the cards don't. |
| 8 | **Condicional** | `A2::condicional` | ~10 | *me gustaría, ¿podrías?, querría* — mostly politeness, immediately usable. |

Later (B1): subjunctive, object pronoun combinations beyond *se lo*, passive
and impersonal *se*.

---

## Not needed

Well covered already — don't add more without a reason: family, house, food,
transport, places in town, clothes, days of the week, connectors (pero,
porque, también), numbers, telling the time, weather, questions, negation,
ser / estar / hay, gustar, possessives, reflexives, ir a + infinitive.

## Habits, not cards

1. **Audio is on** — `{{tts es_ES voices=Apple_Mónica…}}` on both note types
   since the migration, so every card speaks. Nothing to do here any more.
2. **Grade generously on production cards.** Several answers are often
   correct: *I have lived here since 2019* accepts both *Vivo aquí desde…* and
   *He vivido…*. If what you said was good Spanish, press **Good**, even when
   it isn't what's on the back.
