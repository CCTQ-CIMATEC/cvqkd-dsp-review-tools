import sqlite3, pathlib, re, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
cfg = yaml.safe_load(open(ROOT/'src'/'config.yaml','r',encoding='utf-8'))
def con(): c=sqlite3.connect(str(ROOT/cfg['db_path'])); c.execute('PRAGMA foreign_keys=ON;'); return c
def norm(t):
    import re
    t=(t or '').lower().strip()
    t=re.sub(r'[^a-z0-9]+',' ',t); t=re.sub(r'\s+',' ',t)
    return t
c=con(); cur=c.cursor()
# DOI duplicates
cur.execute("SELECT doi, GROUP_CONCAT(id) FROM publications WHERE doi IS NOT NULL AND doi<>'' GROUP BY doi HAVING COUNT(*)>1")
for doi, ids in cur.fetchall():
    ids=[int(x) for x in ids.split(',')]; keep=min(ids)
    for drop in ids:
        if drop==keep: continue
        cur.execute("UPDATE OR IGNORE eligibility SET publication_id=? WHERE publication_id=?", (keep,drop))
        cur.execute("UPDATE OR IGNORE rq_map SET publication_id=? WHERE publication_id=?", (keep,drop))
        cur.execute("UPDATE OR IGNORE data_items SET publication_id=? WHERE publication_id=?", (keep,drop))
        cur.execute("DELETE FROM publications WHERE id=?", (drop,))
# Title+year duplicates
cur.execute("SELECT id,title,year FROM publications"); rows=cur.fetchall()
by_key={}
for pid,title,year in rows:
    key=(norm(title), year)
    by_key.setdefault(key, []).append(pid)
for key, ids in by_key.items():
    if len(ids)<=1: continue
    keep=min(ids)
    for drop in ids:
        if drop==keep: continue
        cur.execute("UPDATE OR IGNORE eligibility SET publication_id=? WHERE publication_id=?", (keep,drop))
        cur.execute("UPDATE OR IGNORE rq_map SET publication_id=? WHERE publication_id=?", (keep,drop))
        cur.execute("UPDATE OR IGNORE data_items SET publication_id=? WHERE publication_id=?", (keep,drop))
        cur.execute("DELETE FROM publications WHERE id=?", (drop,))
c.commit(); print("[OK] dedupe concluído")
