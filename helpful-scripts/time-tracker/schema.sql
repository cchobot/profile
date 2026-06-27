CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    business TEXT NOT NULL,
    comment TEXT,
    start_time TEXT,
    end_time TEXT,
    duration_seconds INTEGER,
    entry_type TEXT NOT NULL CHECK (entry_type IN ('session', 'correction')),
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_active
ON sessions (business, entry_type, end_time);

CREATE INDEX IF NOT EXISTS idx_sessions_report
ON sessions (entry_type, end_time, created_at);
