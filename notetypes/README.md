# Note types

Two note types, three fields each: **Front**, **Back**, **Note**.

| Note type | Front | Back | Used by |
|---|---|---|---|
| `Spanish Production` | English prompt | Spanish answer | verbs, vocab, grammar, topics, A2 pretérito |
| `Spanish Comprehension` | Spanish sentence | English meaning | sentences |

Two of them rather than one, because the speaker belongs on whichever side the
Spanish is: `{{tts}}` reads a whole field, so a single note type would have
Mónica reading English half the time.

The `.tsv` files carry `#notetype:` and `#tags column:4` headers, so the import
dialog picks the right one on its own.

---

## Fields

**Tools → Manage Note Types → Add → Basic**, name it `Spanish Production`, then
**Fields…** and add a third field called `Note`. Repeat for
`Spanish Comprehension`.

Field order matters — it's how the columns map on import:

```
1 Front   2 Back   3 Note   (4th column is tags)
```

## Spanish Production — Cards…

**Front template**

```html
{{Front}}
```

**Back template**

```html
{{FrontSide}}

<hr id=answer>

<div class="es">{{Back}}</div>
{{tts es_ES voices=Apple_Mónica,Apple_Monica:Back}}

<div class="note">{{Note}}</div>
```

## Spanish Comprehension — Cards…

The Spanish is the question here, so the speaker moves to the front.

**Front template**

```html
<div class="es">{{Front}}</div>
{{tts es_ES voices=Apple_Mónica,Apple_Monica:Front}}
```

**Back template**

```html
{{FrontSide}}

<hr id=answer>

{{Back}}

<div class="note">{{Note}}</div>
```

## Styling (paste into both)

```css
.card {
  font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
  font-size: 20px;
  text-align: center;
}

.es {
  font-size: 24px;
  font-weight: 600;
}

.note {
  margin-top: 0.9em;
  font-size: 0.8em;
  line-height: 1.45;
  color: #888;
}

.nightMode .note { color: #9aa0ad; }
```

The grey gloss is now one CSS rule instead of an inline `<span>` on 873 cards.

## Variations worth knowing

**Hide the gloss until you ask for it** — replace the note div with:

```html
<details class="note"><summary>why</summary>{{Note}}</details>
```

**Two spellings on purpose.** Anki tries the `voices=` list in order and takes
the first that exists, so the accentless spelling is there as a fallback. Drop
`voices=` entirely and Anki picks any installed `es_ES` voice — which ignores
your macOS System Voice setting, and is usually not the one you wanted.

**A different voice** — `Apple_Paulina` for Mexico. `say -v '?' | grep es_`
lists what is installed. On AnkiMobile and AnkiDroid
the same tag works with their own voices.

**Replay** — the speaker icon replays; `R` does it from the keyboard.

---

## Migrating the cards you've already studied

Order matters: **convert first, import second.** Anki's duplicate check is per
note type, so importing before the conversion would create 873 brand-new notes
alongside your existing ones instead of updating them.

**0. Back up.** File → Export → Anki Collection Package. One is already in
`backups/`.

**1. Create both note types** as described above, with all three fields and the
templates in place.

**2. Convert the existing notes.** In the Browse window, two passes:

| Search | Change Note Type to |
|---|---|
| `note:Basic tag:A1::sentences` | `Spanish Comprehension` |
| `note:Basic -tag:A1::sentences` | `Spanish Production` |

Select all (⌘A), then **Notes → Change Note Type**. Map **Front → Front**,
**Back → Back**, leave **Note** as *(Nothing)*, and keep **Card 1 → Card 1**.

Never map a template to *(Nothing)* — that deletes those cards and their
scheduling with them. Field mappings are safe; template mappings are the
dangerous half of that dialog.

If your notes aren't on the stock `Basic` type, check the Note column in the
browser and search for that name instead.

**3. Import each file** from `decks/` (File → Import), with
**Existing notes: Update**. The headers do the rest. Back loses its inline
`<span>`, Note gets filled in.

**4. Check.** Total card count is unchanged, a mature card still shows its old
due date, and any card now shows a speaker icon plus a grey gloss underneath.

Between steps 2 and 3 the cards keep their old inline gloss and have an empty
Note field. That looks slightly off but breaks nothing — the import fixes it.
