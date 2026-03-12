CREATE TABLE IF NOT EXISTS booking_requests (
    id INTEGER PRIMARY KEY,
    client_user_id INTEGER NOT NULL,
    master_id INTEGER NOT NULL,
    service_name VARCHAR(120) NOT NULL,
    scheduled_for DATETIME NOT NULL,
    notes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    created_at DATETIME NOT NULL,
    FOREIGN KEY(client_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(master_id) REFERENCES master_profiles(id) ON DELETE CASCADE
);
