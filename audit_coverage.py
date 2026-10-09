#!/usr/bin/env python3
"""Check what the decks actually cover, per level and topic.

    python3 audit_coverage.py                 # report on every level
    python3 audit_coverage.py --level a2      # one level
    python3 audit_coverage.py --gaps          # only what is missing
    python3 audit_coverage.py triste árbol    # ad-hoc: are these words covered?

The checklists live in syllabus/<level>.json, one file per level, so A2 and B1
are a matter of adding a file rather than changing this script.

Two rules learned the hard way, both worth keeping:

  * Look at the Spanish side of a card only. A word that appears in an English
    gloss is not a word the deck teaches. On the comprehension deck, and on any
    drill whose question is itself Spanish, that side is the front.
  * Match whole words and their inflections, never a character prefix.
    "pantalla" is not covered by "pantalones", nor "descargar" by "descanso",
    but "el ojo" is covered by "los ojos".
"""
import argparse
import glob
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {"el", "la", "los", "las", "un", "una", "de", "en", "a", "me", "se", "lo",
        "qué", "cómo", "cuánto", "y", "no", "que", "por"}


def spanish_vocabulary():
    """every Spanish word form the decks put in front of you"""
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "decks", "*.tsv"))):
        comp = "Comprehension" in open(f, encoding="utf-8").read(400)
        for line in open(f, encoding="utf-8"):
            if line.startswith("#") or "\t" not in line:
                continue
            front, back, note, tags = line.rstrip("\n").split("\t")
            spanish_front = comp or "___" in front or "&rarr;" in front
            out.append(front if spanish_front else back)
            if spanish_front and not comp:
                out.append(back)          # the answer to a fill-in is Spanish too
    text = re.sub(r"<[^>]+>", " ", html.unescape(" ".join(out))).lower()
    return set(re.findall(r"[a-záéíóúñü]+", text))


def unaccent(w):
    for a, b in zip("áéíóú", "aeiou"):
        w = w.replace(a, b)
    return w


def forms(word):
    """the inflections a word could reasonably show up as"""
    w = word.lower()
    if w.endswith("se") and w[:-2][-2:] in ("ar", "er", "ir"):
        w = w[:-2]                           # reflexive: ponerse -> poner
    c = {w, w + "s", w + "es"}
    if w.endswith("o"):
        c |= {w[:-1] + x for x in ("a", "os", "as")}
    if w[-2:] in ("ar", "er", "ir"):
        stem = w[:-2]
        c |= {stem + x for x in ("o", "as", "a", "amos", "áis", "an", "es", "e",
                                 "emos", "en", "imos", "ís", "é", "ó", "ando", "iendo")}
    return c


def covered(item, vocab):
    words = [w for w in re.findall(r"[a-záéíóúñü]+", item.lower()) if w not in SKIP]
    if not words:
        return True
    flat = {unaccent(v) for v in vocab}
    for w in words:
        if forms(w) & vocab:
            continue
        # a reflexive infinitive also turns up with its pronouns attached:
        # probarse -> probármelo, vestirse -> vestirme
        base = unaccent(w[:-2] if w.endswith("se") and w[:-2][-2:] in ("ar","er","ir") else w)
        if base[-2:] in ("ar", "er", "ir") and any(v.startswith(base) for v in flat):
            continue
        return False
    return True


def report(level, topics, vocab, gaps_only=False):
    scored = []
    for topic, items in topics.items():
        missing = [i for i in items if not covered(i, vocab)]
        scored.append((len(items) - len(missing), len(items), topic, missing))
    total_ok = sum(s for s, _, _, _ in scored)
    total = sum(n for _, n, _, _ in scored)
    print(f"\n{level.upper()}  —  {total_ok}/{total} items covered ({100*total_ok//total}%)")
    print("-" * 78)
    for ok, n, topic, missing in sorted(scored, key=lambda r: r[0] / r[1]):
        pct = 100 * ok // n
        mark = "✓" if pct == 100 else ("·" if pct >= 85 else "!")
        print(f" {mark} {topic:<32} {ok:>3}/{n:<3} {pct:>3}%")
        if missing and (gaps_only or pct < 100):
            print(f"      missing: {' · '.join(missing)}")
    return total_ok, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="*", help="check these words instead of a syllabus")
    ap.add_argument("--level", help="a1, a2 … (default: all files in syllabus/)")
    ap.add_argument("--gaps", action="store_true", help="list missing items only")
    args = ap.parse_args()

    vocab = spanish_vocabulary()

    if args.words:
        for w in args.words:
            hits = sorted(forms(w) & vocab)
            print(f"{w:<22} {', '.join(hits) if hits else '-  ABSENT'}")
        return

    files = sorted(glob.glob(os.path.join(HERE, "syllabus", "*.json")))
    if args.level:
        files = [f for f in files if os.path.basename(f).startswith(args.level.lower())]
        if not files:
            sys.exit(f"no syllabus file for level {args.level}")

    print(f"{len(vocab)} distinct Spanish word forms in the decks")
    for f in files:
        level = os.path.splitext(os.path.basename(f))[0]
        report(level, json.load(open(f, encoding="utf-8")), vocab, args.gaps)
    print("\n  ✓ complete   · 85%+   ! below 85%")


if __name__ == "__main__":
    main()
