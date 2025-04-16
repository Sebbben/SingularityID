-- Init for IDP_DB
CREATE DATABASE singularity_id;

\c singularity_id
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    secret VARCHAR(255) NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    owner_id UUID NOT NULL REFERENCES users(id),
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



CREATE TABLE authorization_codes (
    code VARCHAR(255) PRIMARY KEY,
    client_id UUID NOT NULL,
    user_id UUID NOT NULL,
    redirect_uri TEXT NOT NULL,
    scope TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE access_tokens (
    token VARCHAR(255) PRIMARY KEY,
    client_id UUID NOT NULL,
    user_id UUID NOT NULL,
    scope TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE refresh_tokens (
    token VARCHAR(255) PRIMARY KEY,
    client_id UUID NOT NULL,
    user_id UUID NOT NULL,
    scope TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Init for APP_DB
CREATE DATABASE frontend_db;

\c frontend_db

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

CREATE TABLE token_pairs (
    session_token VARCHAR(255) PRIMARY KEY DEFAULT gen_random_uuid(),
    refresh_token VARCHAR(255) NOT NULL,
    user_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);