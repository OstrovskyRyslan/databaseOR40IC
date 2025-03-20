import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-QQAOEK4;'
        'DATABASE=GameDB;'
        'Trusted_Connection=yes;'
        'Encrypt=yes;'
        'TrustServerCertificate=yes;'
    )

def save_progress(player_name, level, score, lives, time_spent):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        MERGE INTO player_progress AS target
        USING (SELECT ? AS player_name, ? AS level, ? AS score, ? AS lives, ? AS time_spent) AS source
        ON target.player_name = source.player_name
        WHEN MATCHED THEN
            UPDATE SET level = source.level, score = source.score, lives = source.lives, time_spent = source.time_spent
        WHEN NOT MATCHED THEN
            INSERT (player_name, level, score, lives, time_spent)
            VALUES (source.player_name, source.level, source.score, source.lives, source.time_spent);
        """,
        (player_name, level, score, lives, time_spent)
    )
    
    conn.commit()
    cursor.close()
    conn.close()

def load_progress(player_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT level, score, lives, time_spent FROM player_progress WHERE player_name = ?", (player_name,))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if row:
        return {
            "level": row[0],
            "score": row[1],
            "lives": row[2],
            "time_spent": row[3]
        }
    else:
        return None

if __name__ == "__main__":
    save_progress("Player1", 3, 1500, 5, 120.5)
    progress = load_progress("Player1")
    print("Збережений прогрес:", progress)
