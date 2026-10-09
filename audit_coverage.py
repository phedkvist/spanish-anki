#!/usr/bin/env python3
"""Check whether words are really covered by the decks.

Two rules learned the hard way:

  * look at the Spanish side only - a word that appears in an English gloss
    is not a word the deck teaches
  * match whole words and their inflections, never a character prefix:
    "pantalla" is not covered by "pantalones", nor "descargar" by "descanso"

    python3 audit_coverage.py triste árbol "tener ganas"
"""
import glob, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def spanish_words():
    out = []
    for f in glob.glob(os.path.join(HERE, "decks", "*.tsv")):
        comp = "Comprehension" in open(f, encoding="utf-8").read(400)
        for line in open(f, encoding="utf-8"):
            if line.startswith("#") or "\t" not in line:
                continue
            front, back, note, tags = line.rstrip("\n").split("\t")
            out.append(front if comp else back)       # the Spanish half
    text = re.sub(r"<[^>]+>", " ", html.unescape(" ".join(out))).lower()
    return set(re.findall(r"[a-záéíóúñü]+", text))


def forms(word):
    """the word plus the inflections it could reasonably appear as"""
    w = word.lower()
    c = {w, w + "s", w + "es"}
    if w.endswith("o"):
        c |= {w[:-1] + x for x in ("a", "os", "as")}
    if w[-2:] in ("ar", "er", "ir"):
        stem = w[:-2]
        c |= {stem + x for x in ("o", "as", "a", "amos", "áis", "an",
                                 "es", "e", "emos", "en", "imos", "ís", "é", "ó")}
    return c


def check(items, vocab=None):
    vocab = vocab or spanish_words()
    result = {}
    for item in items:
        words = [w for w in re.findall(r"[a-záéíóúñü]+", item.lower())
                 if w not in {"el", "la", "los", "las", "un", "una", "de", "en", "a", "me", "se"}]
        hits = sorted({f for w in words for f in forms(w) & vocab})
        result[item] = hits
    return result


if __name__ == "__main__":
    for item, hits in check(sys.argv[1:] or ["triste", "árbol", "pantalla"]).items():
        print(f"{item:<22} {', '.join(hits) if hits else '-  ABSENT'}")
