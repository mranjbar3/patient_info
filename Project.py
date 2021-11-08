# سيستم اطلاعات بيمار

import sqlite3
import tkinter
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk, Image

from tkcalendar import DateEntry

avatar_path = "user.jpg"
background_path = "2.png"
icon_path = "favicon.ico"
app_name = "سيستم مديريت بيمار"
button_background_color = '#f3b272'


class Database:
    def __init__(self):
        self.db_connection = sqlite3.connect("dbFile.db")
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute(
            "CREATE TABLE IF NOT EXISTS Bimar "
            "(id INTEGER NOT NULL, fName text, lName text, dob text, mob text, yob text, gender text, address text, "
            "phone text, email text, bloodGroup text, history text, doctor text, image text,time text, sn int,dn int )")
        self.db_cursor.execute(
            "CREATE TABLE IF NOT EXISTS Doctor(id INTEGER NOT NULL PRIMARY KEY, fName text, lName text, field text)")

    def __del__(self):
        self.db_cursor.close()
        self.db_connection.close()

    def insert(self, id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, image,
               time):
        self.db_cursor.execute(
            "INSERT INTO Bimar (id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, "
            "doctor, image, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, image, time))
        self.db_connection.commit()

    def insert_doctor(self, fName, lName, field):
        self.db_cursor.execute("INSERT INTO Doctor (fName, lName, field) VALUES (?, ?, ?)", (fName, lName, field))
        self.db_connection.commit()

    def update(self, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, image,
               time, id):
        self.db_cursor.execute(
            "UPDATE Bimar SET fName = ?, lName = ?, dob = ?, mob = ?, yob = ?, gender = ?, address = ?, phone = ?, "
            "email = ?, bloodGroup = ?, history = ?, doctor = ?, image = ?, time = ? WHERE id = ?",
            (fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, image, time, id))
        self.db_connection.commit()

    def search(self, fName, lName, type):
        if type == "search":
            self.db_cursor.execute(
                "SELECT id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, "
                "time FROM Bimar WHERE fName = ? and lName=?",
                (fName, lName))
        else:
            self.db_cursor.execute(
                "SELECT id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, "
                "image, time FROM Bimar WHERE fName = ? and lName",
                (fName, lName))
        searchResults = self.db_cursor.fetchall()
        return searchResults

    def get_doctors(self):
        self.db_cursor.execute("SELECT id, fName, lName, field FROM Doctor ")
        return self.db_cursor.fetchall()

    def search_by_id(self, id, type):
        if type == "search":
            self.db_cursor.execute(
                "SELECT id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, "
                "time FROM Bimar WHERE id = ?",
                (id,))
        else:
            self.db_cursor.execute(
                "SELECT id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, "
                "image, time FROM Bimar WHERE id = ?",
                (id,))
        searchResults = self.db_cursor.fetchall()
        return searchResults

    def delete(self, id):
        self.db_cursor.execute("DELETE FROM Bimar WHERE id = ?", (id,))
        self.db_connection.commit()

    def get_user_id(self):
        self.db_cursor.execute("SELECT id FROM Bimar ORDER BY 1 DESC LIMIT 1")
        id = self.db_cursor.fetchone()
        if id is None:
            return str(1000)
        return str(id[0] + 1)

    def display(self):
        self.db_cursor.execute(
            "SELECT id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, time "
            "FROM Bimar")
        records = self.db_cursor.fetchall()
        return records

    def search_nobat_by_doctor(self, name):
        self.db_cursor.execute(
            "SELECT id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, time "
            "FROM Bimar WHERE doctor = ? and LENGTH(time) > 0", (name,))
        records = self.db_cursor.fetchall()
        return records


class Values:
    @staticmethod
    def validate(id, first_name, last_name, phone, email, history):
        if not (id.isdigit()):
            return "id"
        elif not (first_name.isalpha()):
            return "fName"
        elif not (last_name.isalpha()):
            return "lName"
        elif not (phone.isdigit() and (len(phone) == 11)):
            return "phone"
        elif not (email.count("@") == 1 and email.count(".") > 0):
            return "email"
        elif not (history.isalpha()):
            return "history"
        else:
            return "SUCCESS"


class InsertWindow:
    def __init__(self, type):
        self.database = Database()
        self.window = Toplevel()
        self.window.resizable(False, False)
        self.window.configure(background='LightGrey')
        self.type = type

        tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="نام", bg="LightGrey",
                      width=20).grid(pady=2, column=1, row=2)
        tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="نام خانوادگي", bg="LightGrey",
                      width=20).grid(pady=2, column=1, row=3)
        self.fNameEntry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
        self.lNameEntry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))

        self.fNameEntry.grid(pady=5, column=2, row=2)
        self.lNameEntry.grid(pady=5, column=2, row=3)
        if type == "Doctor":
            self.window.wm_title("دکتر جديد")
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="تخصص", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=4)
            self.fieldEntry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
            self.fieldEntry.grid(pady=5, column=2, row=4)
        elif type == "Bimar":
            self.window.wm_title("درج اطلاعات بيمار")

            # متغيرها اوليه دهي مقدار
            self.id = Database().get_user_id()

            self.doctorList = []
            doctors = self.database.get_doctors()
            for doctor in doctors:
                self.doctorList.append(doctor[1] + " " + doctor[2] + " : " + doctor[3])

            self.genderList = ["مرد", "زن"]
            self.dateList = list(range(1, 32))
            self.monthList = ["فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي",
                              "بهمن",
                              "اسفند"]
            self.yearList = list(range(1300, 1400))
            self.bloodGroupList = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

            # Labels
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="شناسه بيمار", bg="LightGrey",
                          width=20).grid(
                pady=2, column=1, row=1)
            self.id_entry = tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text=self.id, bg="LightGrey",
                                          width=25)
            self.id_entry.grid(pady=5, column=2, row=1)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="روز تولد", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=4)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="ماه تولد", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=5)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="سال تولد", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=6)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="جنسيت", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=7)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="آدرس منزل", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=8)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="شماره تلفن", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=9)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="ايميل", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=10)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="گروه خوني", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=11)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="سابقه بيماري", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=12)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="پزشک", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=13)
            tkinter.Label(self.window, font=('B Nazanin', 14, 'bold'), text="نوبت", bg="LightGrey",
                          width=20).grid(pady=2, column=1, row=14)

            # Entry ويجت
            self.addressEntry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
            self.phoneEntry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
            self.emailEntry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
            self.historyEntry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))

            self.addressEntry.grid(pady=5, column=2, row=8)
            self.phoneEntry.grid(pady=5, column=2, row=9)
            self.emailEntry.grid(pady=5, column=2, row=10)
            self.historyEntry.grid(pady=5, column=2, row=12)

            # Combobox ويجت
            self.dobBox = tkinter.ttk.Combobox(self.window, values=self.dateList, width=23,
                                               font=('B Nazanin', 12, 'bold'))
            self.mobBox = tkinter.ttk.Combobox(self.window, values=self.monthList, width=23,
                                               font=('B Nazanin', 12, 'bold'))
            self.yobBox = tkinter.ttk.Combobox(self.window, values=self.yearList, width=23,
                                               font=('B Nazanin', 12, 'bold'))
            self.gender = "مرد"

            def set_gender_male():
                self.gender = "مرد"

            def set_gender_female():
                self.gender = "زن"

            self.gender_female = Radiobutton(self.window, text="زن", variable=self.gender, value="زن",
                                             command=set_gender_female).grid(pady=5, columnspan=4, row=7)
            self.gender_male = Radiobutton(self.window, text="مرد", variable=self.gender, value="مرد",
                                           command=set_gender_male).grid(pady=5, column=2, row=7)
            self.bloodGroupBox = tkinter.ttk.Combobox(self.window, values=self.bloodGroupList, width=23,
                                                      font=('B Nazanin', 12, 'bold'))
            self.doctorBox = tkinter.ttk.Combobox(self.window, values=self.doctorList, width=23,
                                                  font=('B Nazanin', 12, 'bold'))
            self.time = DateEntry(self.window, width=12, background='darkblue', foreground='white', borderwidth=2)

            self.dobBox.grid(pady=5, column=2, row=4)
            self.mobBox.grid(pady=5, column=2, row=5)
            self.yobBox.grid(pady=5, column=2, row=6)
            self.bloodGroupBox.grid(pady=5, column=2, row=11)
            self.doctorBox.grid(pady=5, column=2, row=13)
            self.time.grid(pady=5, column=2, row=14)

            tkinter.Button(self.window, width=20, text="انتخاب تصوير براي بيمار", relief=FLAT,
                           bg=button_background_color,
                           command=self.pick_file).grid(pady=15, column=3, row=1)

            # قبلي مقادير تنظيم
            self.image_file_name = avatar_path
            image = Image.open(self.image_file_name)
            a = image.width / 120
            image = image.resize((120, int(image.height / a)), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image)
            self.user_image = tkinter.Label(self.window, image=self.image, width=120, height=120)
            self.user_image.grid(pady=5, column=3, row=2, rowspan=5)

        # Button ويجت
        tkinter.Button(self.window, width=10, text="درج اطلاعات", font=('B Nazanin', 12, 'bold'), bd=3,
                       activeforeground='yellow', activebackground='peru', bg='tan', fg='darkred',
                       command=self.insert).grid(pady=10, padx=10, column=1, columnspan=2, row=15)
        tkinter.Button(self.window, width=10, text="تنظيم مجدد", font=('B Nazanin', 12, 'bold'), bd=3,
                       activeforeground='yellow', activebackground='peru', bg='tan', fg='darkred',
                       command=self.reset).grid(pady=10, padx=10, column=2, row=15)
        tkinter.Button(self.window, width=10, text="خروج", font=('B Nazanin', 12, 'bold'), bd=3,
                       activeforeground='yellow', activebackground='peru', bg='tan', fg='darkred',
                       command=self.window.destroy).grid(pady=10, padx=10, column=3, row=15)

        self.window.mainloop()

    def pick_file(self, address=None):
        if address is None:
            self.image_file_name = tkinter.filedialog.askopenfilename()
        else:
            self.image_file_name = address
        image = Image.open(self.image_file_name)
        a = image.width / 120
        image = image.resize((120, int(image.height / a)), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.user_image.configure(image=self.image)

    def insert(self):
        if self.type == "Bimar":
            self.test = Values().validate(self.id, self.fNameEntry.get(), self.lNameEntry.get(),
                                          self.phoneEntry.get(), self.emailEntry.get(), self.historyEntry.get())
            if self.test == "SUCCESS":
                self.database.insert(self.id, self.fNameEntry.get(), self.lNameEntry.get(), self.dobBox.get(),
                                     self.mobBox.get(), self.yobBox.get(), self.gender, self.addressEntry.get(),
                                     self.phoneEntry.get(), self.emailEntry.get(), self.bloodGroupBox.get(),
                                     self.historyEntry.get(), self.doctorBox.get(), self.image_file_name,
                                     self.time.get())
                tkinter.messagebox.showinfo("داده هاي درج شده", "داده هاي فوق را با موفقيت در پايگاه داده وارد کرديد")
                self.reset()
            else:
                self.value_error_message = "ورودي نامعتبر در قسمت " + self.test
                tkinter.messagebox.showerror("خطا ", self.value_error_message)
        else:
            self.database.insert_doctor(self.fNameEntry.get(), self.lNameEntry.get(), self.fieldEntry.get())
            tkinter.messagebox.showinfo("داده هاي درج شده", "داده هاي فوق را با موفقيت در پايگاه داده وارد کرديد")
            self.reset()

    def reset(self):
        self.fNameEntry.delete(0, tkinter.END)
        self.lNameEntry.delete(0, tkinter.END)
        if self.type == "Doctor":
            self.fieldEntry.delete(0, tkinter.END)
        else:
            self.id_entry.config(text=self.database.get_user_id())
            self.dobBox.set("")
            self.mobBox.set("")
            self.yobBox.set("")
            self.addressEntry.delete(0, tkinter.END)
            self.phoneEntry.delete(0, tkinter.END)
            self.emailEntry.delete(0, tkinter.END)
            self.bloodGroupBox.set("")
            self.historyEntry.delete(0, tkinter.END)
            self.doctorBox.delete(0, tkinter.END)
            self.pick_file(avatar_path)
            self.time.set_date(DateEntry().get_date().today())


class UpdateWindow:

    def __init__(self, user_id):
        self.database = Database()
        self.window = tkinter.Toplevel()
        self.window.wm_title("بروز رساني اطلاعات")
        self.window.resizable(False, False)
        self.window.configure(background='LightGrey')

        # متغيرها اوليه دهي مقدار
        self.id = user_id

        self.genderList = ["مرد", "زن"]
        self.doctorList = []
        doctors = self.database.get_doctors()
        for doctor in doctors:
            self.doctorList.append(doctor[1] + " " + doctor[2] + " : " + doctor[3])
        self.dateList = list(range(1, 32))
        self.monthList = ["فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن",
                          "اسفند"]
        self.yearList = list(range(1300, 1400))
        self.bloodGroupList = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        # Labels
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="شناسه", bg="LightGrey", width=25).grid(pady=5,
                                                                                                                column=1,
                                                                                                                row=1)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text=user_id, bg="LightGrey", width=25).grid(pady=5,
                                                                                                                column=2,
                                                                                                                row=1)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="نام", bg="LightGrey", width=25).grid(pady=5,
                                                                                                              column=1,
                                                                                                              row=2)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="نام خانوادگي", bg="LightGrey", width=25).grid(
            pady=5, column=1, row=3)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="روز تولد", bg="LightGrey", width=25).grid(
            pady=5,
            column=1,
            row=4)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="ماه تولد", bg="LightGrey", width=25).grid(
            pady=5,
            column=1,
            row=5)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="سال تولد", bg="LightGrey", width=25).grid(
            pady=5,
            column=1,
            row=6)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="جنسيت", bg="LightGrey", width=25).grid(pady=5,
                                                                                                                column=1,
                                                                                                                row=7)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="آدرس منزل", bg="LightGrey", width=25).grid(
            pady=5, column=1, row=8)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="تلفن منزل", bg="LightGrey", width=25).grid(
            pady=5, column=1, row=9)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="ايميل", bg="LightGrey", width=25).grid(pady=5,
                                                                                                                column=1,
                                                                                                                row=10)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="گروه خوني", bg="LightGrey", width=25).grid(
            pady=5, column=1, row=11)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="سابقه بيماري", bg="LightGrey", width=25).grid(
            pady=5, column=1, row=12)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="پزشک", bg="LightGrey", width=25).grid(pady=5,
                                                                                                               column=1,
                                                                                                               row=13)
        tkinter.Label(self.window, font=('B Nazanin', 12, 'bold'), text="نوبت", bg="LightGrey", width=25).grid(pady=5,
                                                                                                               column=1,
                                                                                                               row=14)
        tkinter.Button(self.window, width=17, font=('B Nazanin', 12, 'bold'), text="انتخاب تصوير براي بيمار",
                       relief=FLAT,
                       bg=button_background_color,
                       command=self.pick_file).grid(pady=15, column=3, row=1)

        # قبلي مقادير تنظيم
        self.search_results = self.database.search_by_id(user_id, "")

        try:
            image = Image.open(self.search_results[0][13])
            a = image.width / 120
            image = image.resize((120, int(image.height / a)), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image)
            self.filename = self.search_results[0][13]
        except:
            image = Image.open(avatar_path)
            a = image.width / 120
            image = image.resize((120, int(image.height / a)), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image)
            self.filename = ""
        self.user_image = tkinter.Label(self.window, image=self.image, width=120, height=120)
        self.user_image.grid(pady=5, column=3, row=2, rowspan=5)

        # ها فيلد
        # Entry ويجت
        self.first_name_entry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
        self.first_name_entry.insert(END, self.search_results[0][1])
        self.last_name_entry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
        self.last_name_entry.insert(END, self.search_results[0][2])
        self.address_entry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
        self.address_entry.insert(END, self.search_results[0][7])
        self.phone_entry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
        self.phone_entry.insert(END, self.search_results[0][8])
        self.email_entry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
        self.email_entry.insert(END, self.search_results[0][9])
        self.history_entry = tkinter.Entry(self.window, width=25, font=('B Nazanin', 12, 'bold'))
        self.history_entry.insert(END, self.search_results[0][11])

        self.first_name_entry.grid(pady=5, column=2, row=2)
        self.last_name_entry.grid(pady=5, column=2, row=3)
        self.address_entry.grid(pady=5, column=2, row=8)
        self.phone_entry.grid(pady=5, column=2, row=9)
        self.email_entry.grid(pady=5, column=2, row=10)
        self.history_entry.grid(pady=5, column=2, row=12)

        # Combobox ويجت
        self.dob_box = tkinter.ttk.Combobox(self.window, values=self.dateList, width=24, font=('B Nazanin', 12, 'bold'))
        self.dob_box.current(self.dateList.index(int(self.search_results[0][3])))
        self.mob_box = tkinter.ttk.Combobox(self.window, values=self.monthList, width=24,
                                            font=('B Nazanin', 12, 'bold'))
        self.mob_box.current(self.monthList.index(self.search_results[0][4]))
        self.yob_box = tkinter.ttk.Combobox(self.window, values=self.yearList, width=24, font=('B Nazanin', 12, 'bold'))
        self.yob_box.current(self.yearList.index(int(self.search_results[0][5])))
        self.gender = self.search_results[0][6]

        def set_gender_male():
            self.gender = "مرد"

        def set_gender_female():
            self.gender = "زن"

        self.gender_male = ttk.Radiobutton(self.window, text="مرد", variable=self.gender, value="مرد",
                                           command=set_gender_male, width=5).grid(pady=5, column=2, sticky="E",
                                                                                  row=7)
        self.gender_box = ttk.Radiobutton(self.window, text="زن", variable=self.gender, value="زن",
                                          command=set_gender_female, width=5).grid(pady=5, column=2, sticky="N",
                                                                                   row=7)
        self.blood_group_box = tkinter.ttk.Combobox(self.window, values=self.bloodGroupList, width=24,
                                                    font=('B Nazanin', 12, 'bold'))
        self.blood_group_box.current(self.bloodGroupList.index(self.search_results[0][10]))
        self.doctor_box = tkinter.ttk.Combobox(self.window, values=self.doctorList, width=20)
        self.doctor_box.current(self.doctorList.index(self.search_results[0][12]))
        self.time = DateEntry(self.window, width=24, background='darkblue', foreground='white', borderwidth=2)
        self.time.set_date(self.search_results[0][14])

        self.dob_box.grid(pady=5, column=2, row=4)
        self.mob_box.grid(pady=5, column=2, row=5)
        self.yob_box.grid(pady=5, column=2, row=6)
        self.blood_group_box.grid(pady=5, column=2, row=11)
        self.doctor_box.grid(pady=5, column=2, row=13)
        self.time.grid(pady=5, column=2, row=14)

        # Button ويجت
        tkinter.Button(self.window, width=18, font=('B Nazanin', 12, 'bold'), text="بروز رساني", relief=FLAT,
                       bg=button_background_color,
                       command=self.update).grid(pady=15, padx=5, column=1, row=15)
        tkinter.Button(self.window, width=18, font=('B Nazanin', 12, 'bold'), text="بازنشاني ", relief=FLAT,
                       bg=button_background_color,
                       command=self.reset).grid(
            pady=15, padx=5, column=2, row=15)
        tkinter.Button(self.window, width=18, font=('B Nazanin', 12, 'bold'), text="خروج", relief=FLAT,
                       bg=button_background_color,
                       command=self.i_exit).grid(
            pady=15, padx=5, column=3, row=15)

        self.window.mainloop()

    def pick_file(self):
        self.filename = tkinter.filedialog.askopenfilename()
        image = Image.open(self.filename)
        a = image.width / 120
        image = image.resize((120, int(image.height / a)), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.user_image.configure(image=self.image)

    def update(self):
        self.database.update(self.first_name_entry.get(), self.last_name_entry.get(), self.dob_box.get(),
                             self.mob_box.get(),
                             self.yob_box.get(), self.gender, self.address_entry.get(), self.phone_entry.get(),
                             self.email_entry.get(), self.blood_group_box.get(), self.history_entry.get(),
                             self.doctor_box.get(), self.filename, self.time.get(), self.id)
        tkinter.messagebox.showinfo("بروز رساني اطلاعات", "اطلاعات فوق با موفقيت بروزرساني شد")

    def reset(self):
        self.first_name_entry.delete(0, tkinter.END)
        self.last_name_entry.delete(0, tkinter.END)
        self.dob_box.set("")
        self.mob_box.set("")
        self.yob_box.set("")
        self.gender_box.set("")
        self.address_entry.delete(0, tkinter.END)
        self.phone_entry.delete(0, tkinter.END)
        self.email_entry.delete(0, tkinter.END)
        self.blood_group_box.set("")
        self.history_entry.delete(0, tkinter.END)
        self.doctor_box.delete(0, tkinter.END)

    def i_exit(self):
        self.window.destroy()


class DatabaseView:
    def full_view(self):
        self.database_view = tkinter.ttk.Treeview(self.database_view_window)
        self.database_view.grid(pady=5, padx=5, column=1, columnspan=19, row=4)
        self.database_view["show"] = "headings"
        self.database_view["columns"] = ("id", "fName", "lName", "dob", "mob", "yob", "gender", "address",
                                         "phone", "email", "bloodGroup", "history", "doctor", "time")
        self.database_view.heading("id", text="شناسه")
        self.database_view.heading("fName", text="نام")
        self.database_view.heading("lName", text="نام خانوادگي")
        self.database_view.heading("dob", text="روز")
        self.database_view.heading("mob", text="ماه")
        self.database_view.heading("yob", text="سال تولد")
        self.database_view.heading("gender", text="جنسيت")
        self.database_view.heading("address", text="آدرس منزل")
        self.database_view.heading("phone", text="شماره تلفن")
        self.database_view.heading("email", text="ايميل")
        self.database_view.heading("bloodGroup", text="گروه خوني")
        self.database_view.heading("history", text="سابقه بيماري")
        self.database_view.heading("doctor", text="پزشک")
        self.database_view.heading("time", text="نوبت")

        self.database_view.column("id", width=50, anchor=tkinter.CENTER)
        self.database_view.column("fName", width=100, anchor=tkinter.CENTER)
        self.database_view.column("lName", width=100, anchor=tkinter.CENTER)
        self.database_view.column("dob", width=60, anchor=tkinter.CENTER)
        self.database_view.column("mob", width=60, anchor=tkinter.CENTER)
        self.database_view.column("yob", width=60, anchor=tkinter.CENTER)
        self.database_view.column("gender", width=60, anchor=tkinter.CENTER)
        self.database_view.column("address", width=130, anchor=tkinter.CENTER)
        self.database_view.column("phone", width=100, anchor=tkinter.CENTER)
        self.database_view.column("email", width=100, anchor=tkinter.CENTER)
        self.database_view.column("bloodGroup", width=100, anchor=tkinter.CENTER)
        self.database_view.column("history", width=200, anchor=tkinter.CENTER)
        self.database_view.column("doctor", width=150, anchor=tkinter.CENTER)
        self.database_view.column("time", width=100, anchor=tkinter.CENTER)

    def doctor_view(self):
        self.database_view = tkinter.ttk.Treeview(self.database_view_window)
        self.database_view.grid(pady=5, padx=5, column=1, columnspan=19, row=4)
        self.database_view["show"] = "headings"
        self.database_view["columns"] = ("id", "fName", "lName", "field")

        # ستون عناوين
        self.database_view.heading("id", text="شناسه")
        self.database_view.heading("fName", text="نام")
        self.database_view.heading("lName", text="نام خانوادگي")
        self.database_view.heading("field", text="تخصص")

        # Treeview columns
        self.database_view.column("id", width=50, anchor=tkinter.CENTER)
        self.database_view.column("fName", width=100, anchor=tkinter.CENTER)
        self.database_view.column("lName", width=100, anchor=tkinter.CENTER)
        self.database_view.column("field", width=60, anchor=tkinter.CENTER)

    def __init__(self, data, type):
        self.database_view_window = tkinter.Tk()
        self.database_view_window.resizable(False, False)
        self.database_view_window.wm_title("اطلاعات ذخيره شده")
        self.database_view_window.configure(background='Light Grey')
        self.id = data[0][0]
        self.database = Database()

        if type == "person" or type == "all":
            self.first_name_entry = tkinter.Entry(self.database_view_window, width=25, font=('B Nazanin', 12, 'bold'))
            self.last_name_entry = tkinter.Entry(self.database_view_window, width=25, font=('B Nazanin', 12, 'bold'))
            tkinter.Label(self.database_view_window, bd=4, text="نام", width=14, font=('B Nazanin', 14)).grid(
                pady=5, column=1, row=2)
            self.first_name_entry.grid(pady=5, column=2, row=2)
            tkinter.Label(self.database_view_window, bd=4, text="نام خانوادگي", width=14, font=('B Nazanin', 14)).grid(
                pady=5, column=3, row=2)
            self.last_name_entry.grid(pady=5, column=4, row=2)
            tkinter.Button(self.database_view_window, width=18, font=('B Nazanin', 12, 'bold'), text="جست و جو",
                           relief=FLAT,
                           bg=button_background_color, command=self.database_search).grid(
                pady=15, padx=5, column=5, row=2)
            self.full_view()
        elif type == "doctor":
            self.doctor_view()
        elif type == "nobat":
            self.full_view()
            self.doctorList = []
            doctors = self.database.get_doctors()
            for doctor in doctors:
                self.doctorList.append(doctor[1] + " " + doctor[2] + " : " + doctor[3])
            self.doctor_box = tkinter.ttk.Combobox(self.database_view_window, values=self.doctorList, width=20)
            self.doctor_box.grid(pady=5, column=1, row=3)
            tkinter.Button(self.database_view_window, width=18, font=('B Nazanin', 12, 'bold'), text="جست و جو",
                           relief=FLAT, bg=button_background_color, command=self.nobat_search).grid(pady=15, padx=5,
                                                                                                       column=2, row=3)

        for record in data:
            self.database_view.insert('', 'end', values=record)
        self.database_view_window.mainloop()

    def database_search(self):
        self.data = self.database.search(self.first_name_entry.get(), self.last_name_entry.get(), "search")
        if len(self.data) == 0:
            messagebox.showinfo(app_name, "بيماري با اطلاعات وارد شده وجود ندارد.")
        else:
            self.database_view.destroy()
            self.full_view()
            self.database_view.insert('', 'end', values=self.data[0])

    def nobat_search(self):
        self.database_view.destroy()
        self.full_view()
        data = self.database.search_nobat_by_doctor(self.doctor_box.get())
        for record in data:
            self.database_view.insert('', 'end', values=record)


class DeleteUpdateWindow:
    def __init__(self, task):
        self.database = Database()
        window = tkinter.Tk()
        window.resizable(False, False)
        window.iconbitmap('favicon.ico')
        window.wm_title("حذف و بروزرساني اطلاعات بيمار")

        # مقدار دهي اوليه متغيرها
        self.heading = "لطفاً شناسه بيمار را وارد کنيد "

        # Labels
        tkinter.Label(window, text=self.heading).grid(pady=15, padx=15, column=3, rowspan=3)
        # tkinter.Label(window, text="شناسه بيمار", width=10, font=('B Nazanin', 14)).grid(pady=5, row=2)

        # Entry ويجت 
        self.id_entry = tkinter.Entry(window, width=5)
        self.id_entry.grid(pady=15, padx=15, column=2, row=1)

        # Button ويجت
        if task == "Delete":
            self.btn = tkinter.Button(window, width=20, relief=FLAT, bg=button_background_color, text="حذف",
                                      command=self.delete)
        elif task == "Update":
            self.btn = tkinter.Button(window, width=20, relief=FLAT, bg=button_background_color, text="بروزرساني",
                                      command=self.update)
        self.btn.grid(pady=15, padx=15, column=1, row=1)

    def delete(self):
        self.data = self.database.search_by_id(self.id_entry.get(), "search")
        if len(self.data) == 0:
            messagebox.showinfo(app_name, "بيماري با اطلاعات وارد شده وجود ندارد.")
        else:
            i_delete = messagebox.askyesno(app_name, "آيا مي خواهيد اطلاعات بيمار را حذف نماييد؟")
            if i_delete > 0:
                self.database.delete(self.id_entry.get())

    def update(self):
        id = self.id_entry.get()
        self.data = self.database.search_by_id(id, "search")
        if len(self.data) == 0:
            messagebox.showinfo(app_name, "بيماري با اطلاعات وارد شده وجود ندارد")
        else:
            UpdateWindow(id)


class SearchDeleteWindow:
    def __init__(self, task):
        self.database = Database()
        window = tkinter.Tk()
        window.resizable(False, False)
        window.iconbitmap('favicon.ico')
        window.wm_title("جستجوي اطلاعات بيمار")

        # مقدار دهي اوليه متغيرها
        self.heading = "لطفاً نام و نام خانوادگي بيمار را وارد کنيد "

        # Labels
        tkinter.Label(window, text=self.heading).grid(pady=15, padx=15, column=3, rowspan=3)
        tkinter.Label(window, font=('B Nazanin', 14), text="نام:").grid(pady=15, padx=15, column=1, row=1)
        tkinter.Label(window, font=('B Nazanin', 14), text="نام خانوادگي:").grid(pady=15, padx=15, column=1, row=2)
        # tkinter.Label(window, text="شناسه بيمار", width=10, font=('B Nazanin', 14)).grid(pady=5, row=2)

        self.fName = tkinter.Entry(window, width=24, font=('B Nazanin', 8, "bold"))
        self.lName = tkinter.Entry(window, width=24, font=('B Nazanin', 8, "bold"))
        self.fName.grid(pady=15, padx=15, column=2, row=1)
        self.lName.grid(pady=15, padx=15, column=2, row=2)

        # Button ويجت
        if task == "Search":
            self.btn = tkinter.Button(window, width=20, relief=FLAT, bg=button_background_color, text="جستجو",
                                      command=self.search)
        elif task == "Delete":
            self.btn = tkinter.Button(window, width=20, relief=FLAT, bg=button_background_color, text="حذف",
                                      command=self.delete)
        elif task == "Update":
            self.btn = tkinter.Button(window, width=20, relief=FLAT, bg=button_background_color, text="بروزرساني",
                                      command=self.update)

        self.btn.grid(pady=15, padx=15, column=2, row=3)

    def search(self):
        self.data = self.database.search(self.fName.get(), self.lName.get(), "search")
        if len(self.data) == 0:
            messagebox.showinfo(app_name, "بيماري با اطلاعات وارد شده وجود ندارد.")
        else:
            DatabaseView(self.data, "person")


class HomePage:
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("سيستم اطلاعات بيمار")
        self.homePageWindow.resizable(False, False)
#        self.homePageWindow.iconbitmap('favicon.ico')
        self.homePageWindow.geometry("545x545+0+0")

        image = Image.open(background_path)
        a = image.width / 540
        image = image.resize((540, int(image.height / a)), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = tkinter.Label(self.homePageWindow, image=self.background_image)
        self.background_label.place(x=0, y=0)

        tkinter.Label(self.homePageWindow, font=('Titr', 20), text="سيستم اطلاعات بيماران", bg="#e05b49", fg="white",
                      bd=1).grid(pady=10, padx=10, column=4, row=1, sticky='e')

        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="درج اطلاعات جديد",
                       relief=FLAT, bg=button_background_color, command=self.insert).grid(pady=14, padx=14, column=4,
                                                                                          row=3)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="دکتر جديد",
                       relief=FLAT, bg=button_background_color, command=self.insert_doctor).grid(pady=14, padx=14,
                                                                                                 column=4, row=6)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="بروزرساني ",
                       relief=FLAT, bg=button_background_color, command=self.update).grid(pady=10, padx=14, column=5,
                                                                                          row=3)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="جستجو",
                       relief=FLAT, bg=button_background_color, command=self.search).grid(pady=10, padx=7, column=3,
                                                                                          row=6)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="جستجو",
                       relief=FLAT, bg=button_background_color, command=self.search).grid(pady=10, padx=7, column=6,
                                                                                          row=4)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="جستجو",
                       relief=FLAT, bg=button_background_color, command=self.search).grid(pady=10, padx=7, column=6,
                                                                                          row=5)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="حذف",
                       relief=FLAT, bg=button_background_color, command=self.delete).grid(pady=10, padx=7, column=3,
                                                                                          row=3)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="ليست بيماران",
                       relief=FLAT, bg=button_background_color, command=self.display).grid(pady=12, padx=7, column=3,
                                                                                           row=7)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="ليست دکترها",
                       relief=FLAT, bg=button_background_color, command=self.doctors).grid(pady=12, padx=7, column=4,
                                                                                           row=7)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="ليست نوبت ها",
                       relief=FLAT, bg=button_background_color, command=self.nobats).grid(pady=12, padx=7, column=5,
                                                                                          row=7)
        tkinter.Button(self.homePageWindow, width=12, height=1, font=('B Nazanin', 14), text="خروج",
                       relief=FLAT, bg=button_background_color, command=self.i_exit).grid(pady=10, padx=7, column=5,
                                                                                          row=6)

        self.homePageWindow.mainloop()

    def insert(self):
        InsertWindow("Bimar")

    def insert_doctor(self):
        InsertWindow("Doctor")

    def update(self):
        DeleteUpdateWindow("Update")

    def search(self):
        SearchDeleteWindow("Search")

    def delete(self):
        DeleteUpdateWindow("Delete")

    def display(self):
        self.data = Database().display()
        DatabaseView(self.data, "all")

    def doctors(self):
        self.data = Database().get_doctors()
        DatabaseView(self.data, "doctor")

    def nobats(self):
        self.data = Database().display()
        DatabaseView(self.data, "nobat")

    def i_exit(self):
        i_exit = tkinter.messagebox.askyesno(app_name, "آيا مي خواهيد برنامه را ببنديد ؟")
        if i_exit > 0:
            self.homePageWindow.destroy()


HomePage()
