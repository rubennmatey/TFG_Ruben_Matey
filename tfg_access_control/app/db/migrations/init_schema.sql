CREATE TABLE IF NOT EXISTS credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL UNIQUE,
    alias TEXT,
    role TEXT DEFAULT 'user',
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS access_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    result TEXT NOT NULL,
    reason TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    batched INTEGER NOT NULL DEFAULT 0,
    batch_id INTEGER
);

CREATE TABLE IF NOT EXISTS admin_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,
    target_uid TEXT,
    timestamp TEXT NOT NULL,
    synced_to_blockchain INTEGER NOT NULL DEFAULT 0,
    tx_hash TEXT
);

CREATE TABLE IF NOT EXISTS log_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    synced_to_blockchain INTEGER NOT NULL DEFAULT 0,
    tx_hash TEXT
);