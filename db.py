import aiosqlite
from qs import OPTION_KEY
from numpy import bincount
# ----------------------------------------------------------------------------
DB_NAME = 'quizBot.db'
# ----------------------------------------------------------------------------
async def record_user(user_id, verdict):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS results 
                         (user_id INTEGER,
                         verdict TEXT);''')
        await db.execute('''INSERT OR IGNORE INTO results 
                            (user_id, verdict) 
                            VALUES (?, ?);''', 
                            (user_id, verdict))
        await db.commit()
# ----------------------------------------------------------------------------
async def get_results():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS results 
                         (user_id INTEGER,
                         verdict TEXT);''')
        await db.commit()

        async with db.execute('''SELECT *
                                FROM results;''') as cursor:
            records = await cursor.fetchall()

            return records
# ----------------------------------------------------------------------------
async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''DROP TABLE quiz_state;''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state 
                         (user_id INTEGER PRIMARY KEY, 
                         question_index INTEGER, 
                         choice TEXT DEFAULT '');''')
        await db.commit()
# ----------------------------------------------------------------------------
async def update_quiz_index(user_id, question_index, choice):
    async with aiosqlite.connect(DB_NAME) as db:
        if question_index != 0:
            async with db.execute('''SELECT choice
                                FROM quiz_state
                                WHERE user_id=user_id;''') as cursor:
                prev = await cursor.fetchone()

                if prev is not None:
                    choice = str(prev[0]) + choice         

        await db.execute('''INSERT OR REPLACE INTO quiz_state 
                            (user_id, question_index, choice) 
                            VALUES (?, ?, ?);''', 
                            (user_id, question_index, choice))
        await db.commit()
# ----------------------------------------------------------------------------
async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''SELECT question_index 
                              FROM quiz_state 
                              WHERE user_id=user_id;''') as cursor:
            results = await cursor.fetchone()

            if results is not None:
                return results[0]
            else:
                return 0
# ----------------------------------------------------------------------------
async def get_verdict(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''SELECT choice
                              FROM quiz_state
                              WHERE user_id=user_id;''') as cursor:
            results = await cursor.fetchone()

            if results is not None:
                verdict = bincount(list(map(int, results[0]))).argmax()
                await record_user(user_id, OPTION_KEY[verdict])
                return OPTION_KEY[verdict]
            else:
                return 'Something went wrong. Please try again later'