import sqlite3, yaml, pathlib, os, csv
ROOT = pathlib.Path(__file__).resolve().parents[1]
cfg = yaml.safe_load(open(ROOT/'src'/'config.yaml','r',encoding='utf-8'))
con = sqlite3.connect(str(ROOT/cfg['db_path'])); con.execute('PRAGMA foreign_keys=ON;')
cur = con.cursor()
os.makedirs(ROOT/'exports', exist_ok=True)
for rq in cfg['rqs']:
    cur.execute("""SELECT p.title,p.authors,p.year,p.venue,p.doi
                   FROM rq_map r JOIN publications p ON p.id=r.publication_id
                   WHERE r.rq_code=? ORDER BY p.year DESC, p.title""",(rq,))
    rows=cur.fetchall()
    with open(ROOT/'exports'/f"{rq}_publications.csv",'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['title','authors','year','venue','doi'])
        for row in rows: w.writerow(row)
print("[OK] rq_report gerado")
