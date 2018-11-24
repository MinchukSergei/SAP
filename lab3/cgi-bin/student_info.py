from pathlib import Path
import cgi
import html
import sqlite3

form = cgi.FieldStorage()
name = html.escape(form.getfirst('name', 'null'))

conn = sqlite3.connect(str(Path('.').parent / 'students.db'))
c = conn.cursor()
c.execute('''
    SELECT st.student_name, g.group_name, sp.specialty_name 
    FROM st_student st
    LEFT JOIN st_group g ON g.group_id = st.group_id
    LEFT JOIN st_specialty sp ON sp.specialty_id = st.specialty_id
    WHERE st.student_name = ?
''', (name,))

student_info_html = Path('.').parent / 'student_info.html'

with open(student_info_html, 'r') as f:
    sih = f.read().replace('\n', '')
    print("Content-type: text/html\n")
    student = c.fetchone()
    if student is None:
        student = (['Not found'] * 3)
    print(sih.format(student[0], student[1], student[2]))

conn.close()
