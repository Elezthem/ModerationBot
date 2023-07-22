import sqlite3

def tablecreate():
    with sqlite3.connect("server.db") as db:
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS admins(
            id INT,
            verefy INT DEFAULT 0,
            points INT DEFAULT 0
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INT,
            rebuke INT DEFAULT 0,
            reports INT DEFAULT 0,
            vetifBan INT DEFAULT 0,
            verefy INT DEFAULT 0,
            mutes INT DEFAULT 0,
            warns INT DEFAULT 0,
            bans INT DEFAULT 0,
            points INT DEFAULT 0
            
            
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS warn(
            id INT,
            adm INT,
            reason TEXT,
            type,
            date TEXT
        )""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS pred(
            id INT,
            adm INT,
            reason TEXT,
            date TEXT
        )""")