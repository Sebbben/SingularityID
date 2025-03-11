import argparse
import json
import psycopg
import os

def create_client(secret, name, access_token_lifetime, refresh_token_lifetime, redirect_uris=None, scopes=None, grant_types=None):
    try:
        connection = psycopg.connect(
            dbname=os.getenv("AUTH_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO clients (secret, name, access_token_lifetime, refresh_token_lifetime)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (secret, name, access_token_lifetime, refresh_token_lifetime))

        client_id = cursor.fetchone()[0]

        if redirect_uris:
            for uri in redirect_uris:
                cursor.execute("""
                    INSERT INTO client_redirect_uris (client_id, redirect_uri)
                    VALUES (%s, %s);
                """, (client_id, uri))

        if scopes:
            for scope in scopes:
                cursor.execute("""
                    INSERT INTO client_scope (client_id, scope)
                    VALUES (%s, %s);
                """, (client_id, scope))

        if grant_types:
            for grant in grant_types:
                cursor.execute("""
                    INSERT INTO client_grants (client_id, grant_type)
                    VALUES (%s, %s);
                """, (client_id, grant))

        connection.commit()
        return {"id": str(client_id), "secret": secret, "name": name, "access_token_lifetime": access_token_lifetime, "refresh_token_lifetime": refresh_token_lifetime}

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a new client to the auth database.")
    parser.add_argument("--secret", required=True, help="Client secret")
    parser.add_argument("--name", required=True, help="Client name")
    parser.add_argument("--access_token_lifetime", type=int, default=3600, help="Access token lifetime in seconds")
    parser.add_argument("--refresh_token_lifetime", type=int, default=1209600, help="Refresh token lifetime in seconds")
    parser.add_argument("--redirect_uris", nargs='*', help="List of redirect URIs")
    parser.add_argument("--scopes", nargs='*', help="List of client scopes")
    parser.add_argument("--grant_types", nargs='*', help="List of client grant types")

    args = parser.parse_args()

    new_client = create_client(args.secret, args.name, args.access_token_lifetime, args.refresh_token_lifetime, args.redirect_uris, args.scopes, args.grant_types)
    if new_client:
        print(json.dumps(new_client, indent=4))