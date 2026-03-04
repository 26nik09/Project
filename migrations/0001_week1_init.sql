CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'client',
    language VARCHAR(2) NOT NULL DEFAULT 'en',
    is_banned BOOLEAN NOT NULL DEFAULT 0,
    is_adult_confirmed BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS admin_roles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    role_type VARCHAR(30) NOT NULL,
    CONSTRAINT uq_user_admin_role UNIQUE (user_id, role_type),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    slug VARCHAR(100) NOT NULL UNIQUE,
    name_en VARCHAR(120) NOT NULL,
    name_hi VARCHAR(120) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    slug VARCHAR(100) NOT NULL UNIQUE,
    name_en VARCHAR(120) NOT NULL,
    name_hi VARCHAR(120) NOT NULL
);
