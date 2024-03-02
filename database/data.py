import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()


def init_db(force: bool = False):
    if force:
        cursor.execute('DROP TABLE IF EXISTS user_data')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            language TEXT DEFAULT 'eng',
            pomodoro_activation INTEGER DEFAULT 0,
            pomodoro_duration INTEGER DEFAULT NULL,
            pomodoro_end_time TEXT DEFAULT NULL
        )
    ''')


async def add_user(user_id: int):
    if cursor.execute("SELECT user_id FROM user_data WHERE user_id = ?", (user_id,)).fetchone() is None:
        cursor.execute("INSERT INTO user_data (user_id) VALUES (?)", (user_id,))
        conn.commit()


async def get_language(user_id: int):
    return cursor.execute("SELECT language FROM user_data WHERE user_id = ?", (user_id,)).fetchone()[0]


async def change_language(user_id: int, language: str):
    cursor.execute("UPDATE user_data SET language = ? WHERE user_id = ?", (language, user_id))
    conn.commit()


async def set_timer(user_id: int, activation: bool, time=None):
    cursor.execute("UPDATE user_data SET pomodoro_activation = ? WHERE user_id = ?",
                   (int(activation == True), user_id))
    if activation and time:
        cursor.execute("UPDATE user_data SET pomodoro_duration = ? WHERE user_id = ?",
                       (time, user_id))
        cursor.execute("UPDATE user_data SET pomodoro_end_time = ? WHERE user_id = ?",
                       ((datetime.now()+timedelta(minutes=time)).strftime("%H:%M:%S"), user_id))
    conn.commit()


async def get_last_timer_duration(user_id: int):
    return cursor.execute("SELECT pomodoro_duration FROM user_data WHERE user_id = ?", (user_id,)).fetchone()[0]


async def show_time_left(user_id: int):
    user_time = cursor.execute("SELECT pomodoro_end_time FROM user_data WHERE user_id = ?",(user_id,)).fetchone()[0]

    duration = datetime.strptime(user_time, "%H:%M:%S")-datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
    seconds = duration.seconds

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


async def check_activate_user_timer(user_id: int):
    return cursor.execute("SELECT pomodoro_activation FROM user_data WHERE user_id = ?",
                          (user_id,)).fetchone()[0]


async def end_all_users_active_timers():
    max_id = cursor.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
    users_id_list = []
    if max_id:
        for i in range(1, max_id + 1):
            user_id = cursor.execute("SELECT user_id FROM user_data WHERE id = ?",(i,)).fetchone()[0]
            if await check_activate_user_timer(user_id):
                pomodoro_end_time = cursor.execute("SELECT pomodoro_end_time FROM user_data WHERE id = ?",
                                                   (i,)).fetchone()[0]
                if (datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S") ==
                        datetime.strptime(pomodoro_end_time, "%H:%M:%S")):
                    await set_timer(user_id, activation=False)
                    users_id_list.append(user_id)
    return users_id_list



