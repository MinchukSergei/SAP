import sqlite3
import random


def init():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS st_group (
        group_id INTEGER PRIMARY KEY ASC,
        group_name TEXT,
        UNIQUE(group_name)
    )''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS st_specialty (
        specialty_id INTEGER PRIMARY KEY ASC,
        specialty_name TEXT,
        UNIQUE(specialty_name)
    )''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS st_student (
        student_name TEXT PRIMARY KEY ASC, 
        group_id INTEGER, 
        specialty_id INTEGER,
        FOREIGN KEY(group_id) REFERENCES st_group(group_id),
        FOREIGN KEY(specialty_id) REFERENCES st_specialty(specialty_id)
    )''')

    groups = [('1a',), ('1b',), ('1c',), ('2a',), ('2b',), ('2c',), ('3a',), ('3b',), ('3c',)]
    specialties = [('Mechanic',), ('Diver',), ('Surveyor',), ('Sound engineer',), ('Mason',), ('Cartographer',)]
    students_names = ['Petrov', 'Ivanov', 'Sidorov', 'Mihailov', 'Lavochkin']

    c.execute('SELECT COUNT(*) FROM st_group')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO st_group (group_name) VALUES(?)', groups)

    c.execute('SELECT COUNT(*) FROM st_specialty')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO st_specialty (specialty_name) VALUES(?)', specialties)

    c.execute('SELECT COUNT(*) FROM st_student')
    if c.fetchone()[0] == 0:
        students = []
        for s in students_names:
            g = groups[random.randrange(len(groups))]
            sp = specialties[random.randrange(len(specialties))]
            students.append((s, g[0], sp[0]))

        c.executemany('''INSERT INTO st_student (student_name, group_id, specialty_id) VALUES(
            ?,
            (SELECT g.group_id FROM st_group g WHERE g.group_name = ?),
            (SELECT sp.specialty_id FROM st_specialty sp WHERE sp.specialty_name = ?)
        )''', students)

    conn.commit()
    conn.close()
