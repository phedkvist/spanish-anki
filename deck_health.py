#!/usr/bin/env python3
"""Checks and balances on the collection. Run before adding a block.

    python3 deck_health.py

Answers the question "should we be adding cards at all right now, and are the
ones we have any good?" - as opposed to audit_coverage.py, which answers "what
is missing". Exits non-zero if anything is an error rather than a warning.

The budgets are deliberate, not arbitrary: a level's worth of cards is bounded
by what can be reviewed daily, and by the point where more breadth stops paying.
"""
import collections
import glob
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

BUDGET = {"A1": 1000, "A2": 600}      # cards per level before we stop and think
COVERED_ENOUGH = 95                   # % of a syllabus after which new cards need a reason
MAX_UNSEEN = 350                      # unseen cards in Anki before adding more is unkind
MAX_ONCE_ONLY = 55                    # % of word forms allowed to appear on a single card

errors, warnings, notes = [], [], []


def rows():
    for f in sorted(glob.glob(os.path.join(HERE, "decks", "*.tsv"))):
        comp = "Comprehension" in open(f, encoding="utf-8").read(400)
        for n, line in enumerate(open(f, encoding="utf-8"), 1):
            if line.startswith("#") or "\t" not in line:
                continue
            front, back, note, tags = line.rstrip("\n").split("\t")
            yield os.path.basename(f), n, front, back, note, tags.split(), comp


ALL = list(rows())


def check_duplicates():
    seen = collections.defaultdict(list)
    for f, n, front, *_ in ALL:
        seen[front].append(f"{f}:{n}")
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    if dupes:
        for k, v in list(dupes.items())[:5]:
            errors.append(f"duplicate front {k!r} in {', '.join(v)}")
    else:
        notes.append(f"no duplicate fronts across {len(ALL)} cards")


def check_card_shape():
    missing_note = [f"{f}:{n}" for f, n, fr, bk, note, *_ in ALL if not note.strip()]
    if missing_note:
        errors.append(f"{len(missing_note)} cards have an empty Note: {missing_note[:3]}")
    thin = [fr for f, n, fr, bk, note, tags, comp in ALL
            if "___" in fr and "&middot;" not in note]
    if thin:
        warnings.append(f"{len(thin)} fill-in cards whose gloss has no rule after the "
                        f"translation, e.g. {thin[0]!r}")
    # a video deck carries one topical tag on purpose; everything else wants
    # a level::type tag plus a level::topic tag
    bad_tags = [f"{f}:{n}" for f, n, fr, bk, note, tags, comp in ALL
                if "::" not in tags[0]
                or (len(tags) < 2 and not tags[0].startswith("video::"))]
    if bad_tags:
        warnings.append(f"{len(bad_tags)} cards with thin or malformed tags: {bad_tags[:3]}")
    if not missing_note and not thin and not bad_tags:
        notes.append("every card has a gloss, a rule and at least two tags")


def check_budgets():
    per = collections.Counter()
    for f, n, fr, bk, note, tags, comp in ALL:
        level = tags[0].split("::")[0]
        per[level] += 1
    for level, count in sorted(per.items()):
        cap = BUDGET.get(level)
        if cap and count > cap:
            warnings.append(f"{level} is at {count} cards, over its budget of {cap} - "
                            f"prefer depth (a second card for a word that keeps lapsing) "
                            f"over new topics")
        else:
            notes.append(f"{level}: {count} cards" + (f" of {cap}" if cap else ""))


def check_coverage_gate():
    for f in sorted(glob.glob(os.path.join(HERE, "syllabus", "*.json"))):
        level = os.path.splitext(os.path.basename(f))[0].upper()
        try:
            sys.path.insert(0, HERE)
            from audit_coverage import spanish_vocabulary, covered
        except ImportError:
            return
        vocab = spanish_vocabulary()
        topics = json.load(open(f, encoding="utf-8"))
        items = [i for v in topics.values() for i in v]
        ok = sum(1 for i in items if covered(i, vocab))
        pct = 100 * ok // len(items)
        if pct >= COVERED_ENOUGH:
            warnings.append(f"{level} coverage is {pct}% ({ok}/{len(items)}) - the syllabus "
                            f"is satisfied, so a new {level} block needs a reason beyond "
                            f"'it was missing': a lesson that covered it, or a word that "
                            f"keeps failing")
        else:
            notes.append(f"{level} coverage {pct}% ({ok}/{len(items)})")


def check_reinforcement():
    spanish = []
    for f, n, fr, bk, note, tags, comp in ALL:
        es_front = comp or "___" in fr or "&rarr;" in fr
        spanish.append(fr if es_front else bk)
    text = re.sub(r"<[^>]+>", " ", html.unescape(" ".join(spanish))).lower()
    freq = collections.Counter(re.findall(r"[a-záéíóúñü]+", text))
    once = sum(1 for c in freq.values() if c == 1)
    pct = 100 * once // len(freq)
    line = (f"{pct}% of Spanish word forms appear on exactly one card "
            f"({once} of {len(freq)})")
    (warnings if pct > MAX_ONCE_ONLY else notes).append(
        line + (" - new blocks should reuse known words, not only introduce new ones"
                if pct > MAX_ONCE_ONLY else ""))


def check_backlog():
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8765",
            json.dumps({"action": "findCards", "version": 6,
                        "params": {"query": "is:new -is:suspended"}}).encode(),
            {"Content-Type": "application/json"})
        unseen = len(json.load(urllib.request.urlopen(req, timeout=10))["result"])
    except (urllib.error.URLError, KeyError, TimeoutError):
        notes.append("Anki not reachable, skipping the backlog check")
        return
    if unseen > MAX_UNSEEN:
        warnings.append(f"{unseen} cards in Anki have never been seen (limit {MAX_UNSEEN}) - "
                        f"clearing the queue beats adding to it")
    else:
        notes.append(f"{unseen} unseen cards in Anki")


for check in (check_duplicates, check_card_shape, check_budgets,
              check_coverage_gate, check_reinforcement, check_backlog):
    check()

for n in notes:
    print(f"  ok    {n}")
for w in warnings:
    print(f"  WARN  {w}")
for e in errors:
    print(f"  ERROR {e}")

print(f"\n{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
