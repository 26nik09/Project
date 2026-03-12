CREATE TABLE IF NOT EXISTS master_profiles (
    id INTEGER PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    city VARCHAR(120) NOT NULL,
    district VARCHAR(120) NOT NULL,
    bio TEXT,
    online_status BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS master_categories (
    id INTEGER PRIMARY KEY,
    master_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    CONSTRAINT uq_master_category UNIQUE (master_id, category_id),
    FOREIGN KEY(master_id) REFERENCES master_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS master_services (
    id INTEGER PRIMARY KEY,
    master_id INTEGER NOT NULL,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    price_amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    FOREIGN KEY(master_id) REFERENCES master_profiles(id) ON DELETE CASCADE
);
