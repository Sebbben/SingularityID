CREATE DATABASE auth;

\c auth

CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    secret VARCHAR(255) NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    access_token_lifetime INTEGER NOT NULL DEFAULT 3600,
    refresh_token_lifetime INTEGER NOT NULL DEFAULT 1209600
);

CREATE TABLE client_scope (
    client_id UUID NOT NULL,
    scope VARCHAR(255) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE client_redirect_uris (
    client_id UUID NOT NULL,
    redirect_uri TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE client_grants (
    client_id UUID NOT NULL,
    grant_type VARCHAR(255) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);


CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE authorization_codes (
    code VARCHAR(255) PRIMARY KEY,
    client_id UUID NOT NULL,
    user_id INTEGER NOT NULL,
    redirect_uri TEXT NOT NULL,
    scope TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE access_tokens (
    token VARCHAR(255) PRIMARY KEY,
    client_id UUID NOT NULL,
    user_id INTEGER NOT NULL,
    scope TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE refresh_tokens (
    token VARCHAR(255) PRIMARY KEY,
    client_id UUID NOT NULL,
    user_id INTEGER NOT NULL,
    scope TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);