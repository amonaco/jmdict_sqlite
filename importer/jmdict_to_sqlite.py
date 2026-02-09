import sqlite3
import xml.etree.ElementTree as ET
import sys
from pathlib import Path

DB_SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS entry (
    id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS kanji (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER,
    keb TEXT,
    priority TEXT,
    FOREIGN KEY(entry_id) REFERENCES entry(id)
);

CREATE TABLE IF NOT EXISTS reading (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER,
    reb TEXT,
    no_kanji INTEGER,
    FOREIGN KEY(entry_id) REFERENCES entry(id)
);

CREATE TABLE IF NOT EXISTS sense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER,
    sense_index INTEGER,
    FOREIGN KEY(entry_id) REFERENCES entry(id)
);

CREATE TABLE IF NOT EXISTS gloss (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sense_id INTEGER,
    lang TEXT,
    text TEXT,
    FOREIGN KEY(sense_id) REFERENCES sense(id)
);

CREATE TABLE IF NOT EXISTS pos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sense_id INTEGER,
    tag TEXT,
    FOREIGN KEY(sense_id) REFERENCES sense(id)
);
"""

def get_text(elem, tag):
    t = elem.find(tag)
    return t.text if t is not None else None

def parse_jmdict(xml_path, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(DB_SCHEMA)
    conn.commit()

    context = ET.iterparse(xml_path, events=("end",))
    _, root = next(context)

    for event, elem in context:
        if elem.tag == "entry":
            ent_seq = int(elem.find("ent_seq").text)
            cur.execute("INSERT OR IGNORE INTO entry(id) VALUES (?)", (ent_seq,))

            # --- Kanji Elements ---
            for k_ele in elem.findall("k_ele"):
                keb = get_text(k_ele, "keb")
                pris = [p.text for p in k_ele.findall("ke_pri")]
                pri_str = ",".join(pris) if pris else None

                cur.execute(
                    "INSERT INTO kanji(entry_id, keb, priority) VALUES (?, ?, ?)",
                    (ent_seq, keb, pri_str)
                )

            # --- Reading Elements ---
            for r_ele in elem.findall("r_ele"):
                reb = get_text(r_ele, "reb")
                no_kanji = 1 if r_ele.find("re_nokanji") is not None else 0

                cur.execute(
                    "INSERT INTO reading(entry_id, reb, no_kanji) VALUES (?, ?, ?)",
                    (ent_seq, reb, no_kanji)
                )

            # --- Senses ---
            for idx, sense in enumerate(elem.findall("sense")):
                cur.execute(
                    "INSERT INTO sense(entry_id, sense_index) VALUES (?, ?)",
                    (ent_seq, idx)
                )
                sense_id = cur.lastrowid

                # POS
                for pos in sense.findall("pos"):
                    cur.execute(
                        "INSERT INTO pos(sense_id, tag) VALUES (?, ?)",
                        (sense_id, pos.text)
                    )

                # Glosses
                for gloss in sense.findall("gloss"):
                    lang = gloss.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", "eng")
                    cur.execute(
                        "INSERT INTO gloss(sense_id, lang, text) VALUES (?, ?, ?)",
                        (sense_id, lang, gloss.text)
                    )

            conn.commit()

            # free memory
            root.clear()

    conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python jmdict_to_sqlite.py JMdict.xml output.db")
        sys.exit(1)

    xml_file = Path(sys.argv[1])
    db_file = Path(sys.argv[2])

    parse_jmdict(xml_file, db_file)
    print("Done.")

