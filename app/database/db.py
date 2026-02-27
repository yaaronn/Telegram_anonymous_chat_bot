import aiosqlite

DB_PATH = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            country TEXT             
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reported_user INTEGER
        )
        """)

        await db.commit()

    print("Database ready")

async def add_user(user_id, name):

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        await db.commit() 

async def update_gender(user_id, gender):

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET gender=? WHERE user_id=?",
            (gender, user_id)
        )
        await db.commit()


async def get_user(user_id):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            "SELECT user_id, name, gender FROM users WHERE user_id=?",
            (user_id,)
        )

        user = await cursor.fetchone()

        return user    

async def update_country(user_id, country):

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET country=? WHERE user_id=?",
            (country, user_id)
        )
        await db.commit()           
        
async def add_report(user_id):

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO reports (reported_user) VALUES (?)",
            (user_id,)
        )
        await db.commit()
