import sqlite3, yaml, pathlib, pandas as pd, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
cfg = yaml.safe_load(open(ROOT/'src'/'config.yaml','r',encoding='utf-8'))
def guess(df, aliases):
    cols = {c.lower(): c for c in df.columns.astype(str)}
    for a in aliases:
        a=a.lower()
        if a in cols: return cols[a]
        for k,v in cols.items():
            if a in k: return v
    return None
def norm(x): return re.sub(r'\s+',' ',str(x or '')).strip()
df = pd.read_excel(ROOT/cfg['excel_path'], sheet_name=cfg.get('excel_sheet'))
df.columns = df.columns.astype(str)
col = {k:guess(df,v) for k,v in cfg['column_map'].items()}
con = sqlite3.connect(str(ROOT/cfg['db_path'])); con.execute('PRAGMA foreign_keys=ON;')
cur = con.cursor()
inserted=0
for _,r in df.iterrows():
    title = norm(r.get(col['title'])) if col['title'] else None
    if not title: continue
    authors = norm(r.get(col['authors'])) if col['authors'] else None
    venue = norm(r.get(col['venue'])) if col['venue'] else None
    doi = norm(r.get(col['doi'])) if col['doi'] else None
    url = norm(r.get(col['url'])) if col['url'] else None
    abstract = norm(r.get(col['abstract'])) if col['abstract'] else None
    year = None
    if col['year'] and pd.notna(r.get(col['year'])):
        try: year = int(str(r.get(col['year'])).split('.')[0])
        except: year=None
    if doi:
        cur.execute("SELECT id FROM publications WHERE doi=?", (doi,)); row=cur.fetchone()
    else:
        cur.execute("SELECT id FROM publications WHERE lower(title)=lower(?)", (title,)); row=cur.fetchone()
    if row:
        pid=row[0]
        cur.execute("UPDATE publications SET authors=?,year=?,venue=?,url=?,abstract=? WHERE id=?",(authors,year,venue,url,abstract,pid))
    else:
        cur.execute("INSERT INTO publications(title,authors,year,venue,doi,url,abstract) VALUES (?,?,?,?,?,?,?)",(title,authors,year,venue,doi,url,abstract)); pid=cur.lastrowid; inserted+=1
    # eligibility
    stage = norm(r.get(col['decision_stage'])) if col['decision_stage'] else None
    inc_raw = str(r.get(col['include_flag'])).strip().lower() if col['include_flag'] else ''
    include_flag = 1 if inc_raw in ('1','true','yes','sim','include','included') else 0 if inc_raw in ('0','false','no','nao','não','exclude','excluded') else None
    notes = norm(r.get(col['notes'])) if col['notes'] else None
    if stage or include_flag is not None or notes:
        cur.execute("INSERT INTO eligibility(publication_id,decision_stage,include_flag,reason_code,notes) VALUES (?,?,?,?,?)",(pid,stage,include_flag,None,notes))
    # rq_map
    rq_cell = norm(r.get(col['rq_list'])) if col['rq_list'] else ''
    for part in re.split(r'[;,|/ ]+', rq_cell.upper()):
        if part in cfg['rqs']:
            cur.execute("INSERT INTO rq_map(publication_id,rq_code) VALUES (?,?)",(pid,part))
con.commit()
print(f"[OK] import_excel: {inserted} novos/atualizados")
