import sqlite3

def connect_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor

def create_database(conn, cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        startXp INTEGER,
        startStreak INTEGER,
        totalScore INTEGER
    );
    """
    cursor.execute(create_table_query)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS score_evolution (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        date TEXT,
        xpDay INTEGER,
        streakerDia INTEGER,
        xpScore INTEGER,
        streakerScore INTEGER,
        totalScore INTEGER
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
