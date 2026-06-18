import sqlite3

conn = sqlite3.connect(
    "database/database.db",
    check_same_thread=False
)

cursor = conn.cursor()

# Chat history
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory(
    user_id INTEGER,
    content TEXT
)
""")

# Long-term memory
cursor.execute("""
CREATE TABLE IF NOT EXISTS memories(
    user_id INTEGER,
    memory TEXT
)
""")

conn.commit()

def save_memory(user_id, content):

    cursor.execute(
        "INSERT INTO memory VALUES (?, ?)",
        (user_id, content)
    )

    conn.commit()

def get_memory(user_id):

    cursor.execute(
        "SELECT content FROM memory WHERE user_id=? ORDER BY rowid DESC LIMIT 15",
        (user_id,)
    )

    rows = cursor.fetchall()

    return "\n".join([row[0] for row in rows])

# NEW FUNCTIONS

def save_long_memory(user_id, memory):

    cursor.execute(
        "INSERT INTO memories VALUES (?, ?)",
        (user_id, memory)
    )

    conn.commit()

def get_long_memory(user_id):

    cursor.execute(
        """
        SELECT memory
        FROM memories
        WHERE user_id=?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    return "\n".join(
        [row[0] for row in rows]
    )