-- SQL statements to create the 'user' table
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- SQL statements to create the 'message' table
CREATE TABLE "message" (
    message_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(user_id),
    content TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
