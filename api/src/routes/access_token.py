from ..db import DatabaseManager

def access_token():
    db = DatabaseManager.get_instance().get_db(os.getenv("AUTH_DB"))

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("")
            res = cur.fetchone()
    
