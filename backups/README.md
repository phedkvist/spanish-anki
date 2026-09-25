# Backups

Anki collection exports live here and are **gitignored** — they hold your review
history and scheduling, which is personal and not worth publishing.

Before anything that rewrites notes in bulk (a note type change, a large
import), take one:

**File → Export → Anki Collection Package**, tick *Include media*, save here.

`build_anki.py` can rebuild every card in the collection from scratch. What it
cannot rebuild is your scheduling — that only exists in these files and in
Anki's own automatic backups under
`~/Library/Application Support/Anki2/<profile>/backups/`.
