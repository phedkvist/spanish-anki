#!/usr/bin/env python3
"""Migrate a live Anki collection to the two Spanish note types, via AnkiConnect.

What it does, in order:

  1. creates "Spanish Production" and "Spanish Comprehension" if missing,
     with a Note field and {{tts}} on whichever side the Spanish is
  2. converts existing Basic notes to the right one of those two
  3. writes Back and Note from decks/*.tsv into the notes already in the
     collection, so the gloss moves out of Back

Scheduling is never touched: notes are matched by their first field, and
note ids are preserved throughout. Cards from the .tsv files that are not in
the collection yet are only reported - importing those needs a target deck,
which is a separate decision.

Usage:
    python3 migrate_anki.py --dry-run     # show what would change
    python3 migrate_anki.py               # do it

Requires Anki running with the AnkiConnect add-on (code 2055492159).
"""
import argparse
import glob
import html
import json
import os
import sys
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8765"
HERE = os.path.dirname(os.path.abspath(__file__))

PRODUCTION = "Spanish Production"
COMPREHENSION = "Spanish Comprehension"
VOICE = "es_ES voices=Apple_Mónica,Apple_Monica"  # first installed one wins

CSS = """.card {
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
"""

MODELS = {
    PRODUCTION: {
        "Front": "{{Front}}",
        "Back": (
            "{{FrontSide}}\n\n<hr id=answer>\n\n"
            '<div class="es">{{Back}}</div>\n'
            "{{tts " + VOICE + ":Back}}\n\n"
            '<div class="note">{{Note}}</div>'
        ),
    },
    COMPREHENSION: {
        "Front": '<div class="es">{{Front}}</div>\n{{tts ' + VOICE + ":Front}}",
        "Back": (
            "{{FrontSide}}\n\n<hr id=answer>\n\n"
            "{{Back}}\n\n"
            '<div class="note">{{Note}}</div>'
        ),
    },
}


def call(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(URL, payload, {"Content-Type": "application/json"})
    try:
        res = json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.URLError as e:
        sys.exit(f"cannot reach AnkiConnect at {URL} ({e}).\n"
                 "Is Anki running with the AnkiConnect add-on installed?")
    if res.get("error"):
        sys.exit(f"AnkiConnect error on {action}: {res['error']}")
    return res["result"]


def key(front):
    """Match on the front with entities decoded.

    Editing a note in Anki rewrites &rarr; as a literal arrow, so a card
    edited during review would otherwise stop matching its row and be added
    a second time.
    """
    return html.unescape(front).strip()


def read_decks():
    """Every row of every .tsv, keyed by Front."""
    cards = {}
    for path in sorted(glob.glob(os.path.join(HERE, "decks", "*.tsv"))):
        notetype = PRODUCTION
        for line in open(path, encoding="utf-8"):
            if line.startswith("#notetype:"):
                notetype = line.split(":", 1)[1].strip()
            if line.startswith("#") or "\t" not in line:
                continue
            front, back, note, tags = line.rstrip("\n").split("\t")
            cards[key(front)] = {"front": front, "back": back, "note": note,
                            "tags": tags.split(), "notetype": notetype,
                            "file": os.path.basename(path)}
    return cards


def ensure_models(dry):
    existing = call("modelNames")
    for name, tpl in MODELS.items():
        if name in existing:
            print(f"  {name}: exists")
            if not dry:
                call("updateModelTemplates",
                     model={"name": name, "templates": {"Card 1": tpl}})
                call("updateModelStyling", model={"name": name, "css": CSS})
                print(f"    templates + styling refreshed (tts on "
                      f"{'Front' if name == COMPREHENSION else 'Back'})")
            continue
        print(f"  {name}: creating")
        if not dry:
            call("createModel", modelName=name,
                 inOrderFields=["Front", "Back", "Note"],
                 css=CSS,
                 cardTemplates=[{"Name": "Card 1",
                                 "Front": tpl["Front"], "Back": tpl["Back"]}])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--add-missing", metavar="DECK",
                    help="also add cards that aren't in the collection yet, "
                         "into this deck")
    ap.add_argument("--skip-level", default="A2,video",
                    help="comma-separated tag prefixes not to add "
                         "(default: A2,video - those go in their own decks; "
                         "pass none to add everything)")
    args = ap.parse_args()
    dry = args.dry_run
    if dry:
        print("DRY RUN - nothing will be written\n")

    print("AnkiConnect version:", call("version"))
    cards = read_decks()
    print(f"{len(cards)} cards in decks/\n")

    print("note types:")
    ensure_models(dry)

    print("\nnotes in the collection:")
    ids = call("findNotes", query="*")
    info = call("notesInfo", notes=ids)
    by_front = {}
    for n in info:
        fields = n["fields"]
        first = fields.get("Front", next(iter(fields.values())))["value"]
        by_front[key(first)] = n
    print(f"  {len(info)} notes, {len(by_front)} distinct first fields")

    convert, update, missing = [], [], []
    for front, row in cards.items():
        n = by_front.get(front)
        if not n:
            missing.append(front)
            continue
        if n["modelName"] != row["notetype"]:
            convert.append((n, row))
        update.append((n, row))

    print(f"  {len(convert)} to convert to the new note types")
    print(f"  {len(update)} to have Back/Note rewritten")
    print(f"  {len(missing)} cards in decks/ are not in the collection yet")
    extra = set(by_front) - set(cards)
    if extra:
        print(f"  {len(extra)} notes in the collection are not in decks/:")
        for f in list(extra)[:10]:
            print("     ", f)

    if dry:
        print("\nnothing written (dry run)")
        return

    for n, row in convert:
        call("updateNoteModel", note={
            "id": n["noteId"],
            "modelName": row["notetype"],
            "fields": {"Front": next(iter(n["fields"].values()))["value"],
                       "Back": "", "Note": ""},
            "tags": n["tags"],
        })
    print(f"\nconverted {len(convert)} notes")

    for n, row in update:
        call("updateNoteFields", note={
            "id": n["noteId"],
            "fields": {"Back": row["back"], "Note": row["note"]},
        })
    print(f"rewrote {len(update)} notes' fields")

    if missing and not args.add_missing:
        print(f"\n{len(missing)} cards are not in the collection - pass "
              "--add-missing DECK to add them.")
    elif missing:
        skips = [] if args.skip_level == "none" else args.skip_level.split(",")
        to_add = [f for f in missing
                  if not any(t.startswith(p + "::") for p in skips
                             for t in cards[f]["tags"])]
        held = len(missing) - len(to_add)
        notes = [{"deckName": args.add_missing,
                  "modelName": cards[f]["notetype"],
                  "fields": {"Front": cards[f]["front"], "Back": cards[f]["back"],
                             "Note": cards[f]["note"]},
                  "tags": cards[f]["tags"],
                  "options": {"allowDuplicate": False}}
                 for f in to_add]
        added = call("addNotes", notes=notes)
        ok = sum(1 for a in added if a)
        print(f"\nadded {ok} cards to '{args.add_missing}'"
              + (f", held back {held} tagged {'/'.join(skips)}" if held else ""))
        if ok != len(notes):
            print(f"  {len(notes) - ok} were refused (duplicate first field)")


if __name__ == "__main__":
    main()
