CREATE TABLE IF NOT EXISTS dining_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    cuisine TEXT,
    dietary TEXT,
    description TEXT
);
