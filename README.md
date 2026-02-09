# jmdict_sqlite

Gives a clean relational base ready for JLPT tagging, flashcards, or APIs.

API provides a clean backend skeleton that scales well. WIP for the time being

Import script creates an SQLite3 database (see schema below)

# DB Structure

```
entry
    id (ent_seq)
kanji
    keb
    priority
reading
    reb
    no_kanji
sense
    index per entry
gloss
    language
    text
pos
    noun, verb, etc.
```


# Notes
Uses iterparse → low RAM.
Safe for full JMdict (~200k entries).
Easy to extend:
    field
    dial
    misc
    stagk/stagr

# Todo
Add indexes later for search speed:

```
CREATE INDEX idx_kanji_keb ON kanji(keb);
CREATE INDEX idx_reading_reb ON reading(reb);
CREATE INDEX idx_gloss_text ON gloss(text);
```

