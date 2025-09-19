PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS publications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  authors TEXT, year INTEGER, venue TEXT, doi TEXT UNIQUE, url TEXT, abstract TEXT,
  pdf_path TEXT, pdf_sha256 TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS eligibility (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  publication_id INTEGER NOT NULL,
  decision_stage TEXT, include_flag INTEGER, reason_code TEXT, notes TEXT,
  FOREIGN KEY(publication_id) REFERENCES publications(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS rq_map (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  publication_id INTEGER NOT NULL,
  rq_code TEXT NOT NULL CHECK (rq_code IN ('RQ1','RQ2','RQ3','RQ4','RQ5','RQ6')),
  FOREIGN KEY(publication_id) REFERENCES publications(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS data_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  publication_id INTEGER NOT NULL,
  dsp_technique TEXT, system_arch TEXT, metrics TEXT, setup TEXT, limitations TEXT, future_work TEXT, source TEXT,
  FOREIGN KEY(publication_id) REFERENCES publications(id) ON DELETE CASCADE
);
