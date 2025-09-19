import argparse, sqlite3, yaml, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
def cfg(): return yaml.safe_load(open(ROOT/'src'/'config.yaml','r',encoding='utf-8'))
def conn():
    c = sqlite3.connect(str(ROOT / cfg()['db_path'])); c.execute("PRAGMA foreign_keys=ON;"); return c
def init_db():
    with open(ROOT/'src'/'schema.sql','r',encoding='utf-8') as f: schema=f.read()
    with conn() as c: c.executescript(schema)
    print("[OK] DB inicializado")
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--init',action='store_true'); a=p.parse_args()
    if a.init: init_db()
