import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def current_date():
    """Returns the current date in YYYY-MM-DD format."""
    return sqlite3.datetime.datetime.now().strftime('%Y-%m-%d')

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracked_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracked_date DATE NOT NULL,
				is_holiday BOOLEAN NOT NULL,
                office_location TEXT,
                office_entry_time TEXT,
                office_exit_time TEXT,
                office_minutes INTEGER NOT NULL,
				other_minutes INTEGER NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def is_current_day_tracked(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM tracked_days WHERE tracked_date = DATE('now')
    ''')
    count = cursor.fetchone()[0]
    return count > 0

def insert_default_tracked_day(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tracked_days (tracked_date, is_holiday, office_location, office_entry_time, office_exit_time, office_minutes, other_minutes)
            VALUES (DATE('now'), 0, NULL, NULL, NULL, 0, 0)
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def increment_office_minutes(conn, minutes):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tracked_days
            SET office_minutes = office_minutes + ?
            WHERE tracked_date = DATE('now')
        ''', (minutes,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def increment_other_minutes(conn, minutes):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tracked_days
            SET other_minutes = other_minutes + ?
            WHERE tracked_date = DATE('now')
        ''', (minutes,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def is_current_day_office_set(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT office_location FROM tracked_days WHERE tracked_date = DATE('now')
    ''')
    result = cursor.fetchone()
    return result is not None and result[0] is not None

def is_office_entry_time_set(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT office_entry_time FROM tracked_days WHERE tracked_date = DATE('now')
    ''')
    result = cursor.fetchone()
    return result is not None and result[0] is not None

def set_current_day_office(conn, office_location):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tracked_days
            SET office_location = ?
            WHERE tracked_date = DATE('now')
        ''', (office_location,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def update_current_day_office_entry_time(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tracked_days
            SET office_entry_time = CURRENT_TIMESTAMP
            WHERE tracked_date = DATE('now')
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def update_current_day_office_exit_time(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tracked_days
            SET office_exit_time = CURRENT_TIMESTAMP
            WHERE tracked_date = DATE('now')
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        
