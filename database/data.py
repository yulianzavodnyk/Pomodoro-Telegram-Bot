import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('database/database.db')  # connect to database file
cursor = conn.cursor()


def init_db(force: bool = False):
    """ Creating database if not exists"""
    if force:
        cursor.execute('DROP TABLE IF EXISTS user_data')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            pomodoro_activation INTEGER DEFAULT 0,
            pomodoro_duration INTEGER DEFAULT NULL,
            pomodoro_end_time TEXT DEFAULT NULL
        )
    ''')


async def add_user(user_id: int):
    """
    Adding user to database
    :param user_id: user id
    """
    if cursor.execute("SELECT user_id FROM user_data WHERE user_id = ?", (user_id,)).fetchone() is None:
        cursor.execute("INSERT INTO user_data (user_id) VALUES (?)", (user_id,))
        conn.commit()


async def set_timer(user_id: int, activation: bool, time=None):
    """
    Setting user timer
    :param user_id: user id
    :param activation: True means timer will be activated, False means timer will be deactivated
    :param time: you need to specify this param if activation == True,
    write it with time you want set timer
    """
    cursor.execute("UPDATE user_data SET pomodoro_activation = ? WHERE user_id = ?",
                   (int(activation == True), user_id))
    if activation and time:
        cursor.execute("UPDATE user_data SET pomodoro_duration = ?, pomodoro_end_time = ? WHERE user_id = ?",
                       (time, (datetime.now()+timedelta(minutes=time)).strftime("%H:%M:%S"), user_id))
    conn.commit()


async def get_last_timer_duration(user_id: int):  #
    """
    Return duration of last active timer
    :param user_id: user id
    :return: int
    """
    return cursor.execute("SELECT pomodoro_duration FROM user_data WHERE user_id = ?",
                          (user_id,)).fetchone()[0]


async def calculate_time_left(user_id: int):
    """
    Calculate how much time is left till the end of the timer
    :param user_id: user id
    :return: Tuple[int, int, int]
    """
    user_time = cursor.execute("SELECT pomodoro_end_time FROM user_data WHERE user_id = ?",
                               (user_id,)).fetchone()[0]

    duration = datetime.strptime(user_time, "%H:%M:%S")-datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
    seconds = duration.seconds

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


async def check_activate_user_timer(user_id: int):
    """
    check if user have active timer
    :param user_id: user id
    :return: int
    """
    return cursor.execute("SELECT pomodoro_activation FROM user_data WHERE user_id = ?",
                          (user_id,)).fetchone()[0]


async def end_all_users_ended_timers():
    """
    Making a list of all users that have currently ended timer, and stop their timers
    :return: List[int]
    """
    max_id = cursor.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
    users_id_list = []
    if max_id:
        for i in range(1, max_id + 1):
            user_id, pomodoro_end_time = cursor.execute("SELECT user_id, pomodoro_end_time FROM user_data WHERE id = ?",(i,)).fetchone()
            if await check_activate_user_timer(user_id):
                if (datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S") ==
                        datetime.strptime(pomodoro_end_time, "%H:%M:%S")):
                    await set_timer(user_id, activation=False)
                    users_id_list.append(user_id)
    return users_id_list
