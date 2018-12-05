from tkinter import *
import sqlite3

db_name = 'students.db'


def main():
    init_db()

    root = Tk()
    root.geometry("500x350")

    App(root)
    root.mainloop()


def init_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE students (
            date TEXT, 
            student_name TEXT,
            group_name TEXT, 
            faculty_name TEXT,
            year INTEGER
        )''')
        conn.commit()
        conn.close()
    except:
        pass


class App:
    def __init__(self, root):
        frame = Frame(root, bg="green")
        frame.pack(fill=BOTH)

        self.root = root

        self.quit_button = Button(frame, text="QUIT", fg="red", command=self.exit)
        self.quit_button.pack(side=LEFT)

        self.select_button = Button(frame, text="Select", fg="blue", command=self.select_name)
        self.select_button.pack(side=LEFT)

        self.select_button = Button(frame, text="Find", fg="gray", command=self.fetch)
        self.select_button.pack(side=LEFT)

        self.name_field = Text(frame, height=1, width=35, font='Arial 10', wrap=WORD)
        self.name_field.pack(side=RIGHT)

        self.students_info = Message(root, width=300)
        self.students_info.place(x=150, y=150)

        self.names = ['Sergey', 'Ansony', 'Lodi', 'Olber', 'Rauf']
        self.listbox = Listbox(root)  # Create 2 listbox widgets

        for item in self.names:
            self.listbox.insert(0, item)

        self.listbox.place(x=5, y=120)

        self.fields = self.build_fields()

        insert_button = Button(root, text='Insert', command=self.insert_record)
        insert_button.place(x=45, y=280)

    def build_fields(self):
        field_names = 'Group', 'Faculty', 'Year'
        fields = []
        for field_name in field_names:
            row = Frame(self.root)
            row.pack(side=TOP, fill=X, padx=5, pady=5)

            entry = Entry(row)
            entry.pack(side=LEFT)

            label = Label(row, width=20, text=field_name, anchor='w')
            label.pack(side=LEFT)

            fields.append((field_name, entry))
        return fields

    def insert_record(self):
        selection = self.listbox.curselection()

        if len(selection) is 0:
            return

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        name = self.listbox.get(self.listbox.curselection())

        now = sqlite3.datetime.datetime.now()

        fields = self.fields
        record = (now.strftime("%Y-%m-%d"),
                  name,
                  fields[0][1].get(),
                  fields[1][1].get(),
                  fields[2][1].get())

        c.execute('''INSERT INTO students (
                        date, 
                        student_name, 
                        group_name, 
                        faculty_name, 
                        year
                    ) VALUES (?, ?, ?, ?, ?)''', record)
        conn.commit()
        conn.close()

        self.fetch()

    def select_name(self):
        selection = self.listbox.curselection()
        if len(selection) is 0:
            return
        self.name_field.delete('1.0', END)
        self.name_field.insert(1.0, self.listbox.get(self.listbox.curselection()))

    def exit(self):
        self.root.destroy()

    def fetch(self):
        selection = self.listbox.curselection()
        if len(selection) is 0:
            return

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        name = self.listbox.get(self.listbox.curselection())

        students = c.execute('SELECT * FROM students WHERE student_name = ?', (name,))

        result = ''
        for student in students:
            result += str(student) + '\n'

        if result == '':
            result = 'No data found.'

        self.students_info.configure(text=result)


if __name__ == '__main__':
    main()
