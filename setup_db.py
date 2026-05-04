import sqlite3

DB_PATH = 'online_course.db'
SCHEMA_FILE = 'schema.sql'
SEED_FILE = 'seed_data.sql'

with sqlite3.connect(DB_PATH) as conn:
    conn.execute('PRAGMA foreign_keys = ON;')
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as schema:
        conn.executescript(schema.read())
    with open(SEED_FILE, 'r', encoding='utf-8') as seed:
        conn.executescript(seed.read())

print(f'Database initialized at {DB_PATH}')
