##A system for receiving personal information about people who have been vaccinated against corona
##A system that receives data and stores it in a database
##The program allows the user to make changes to the received data, view the information or data to the relevant parties
from DatabaseCreat import *         # pip install pymysql
import hashlib,tkinter,colorama     # pip install colorama
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image      # pip install Pillow
from termcolor import colored       # pip install termcolor
from sys import exit
import re
import  matplotlib.pyplot as plt    # pip install matplotlib

colorama.init()
DataBaseCREATE()                    #Database Connection function by import DatabaseCreat.py script

##---Database Connection---##
try:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 port=3306,
                                 db='DetailsDB',
                                 )  # cursorclass=pymysql.cursors.DictCursor#charset='TRUE'
    Mycursor = connection.cursor()  # Mycursor to perform database operations
except pymysql.Error:
    messagebox.showinfo("Error", "Database connection failed")
    print(colored("Database connection failed", "red"))
    exit()

# --Show_info_Screen Function--#
#showing Data in A Table
# Showing Vaccine Success and fail Rates
# Showing the amount of people who took the vaccine
def Show_info_Screen():
    screen4 = tk.Tk()
    screen4.geometry("600x400")
    screen4.title("Application")
    screen4.configure(bg="LightSkyBlue1")

    def Menu():
        screen4.destroy()
        Second_Page()

    #--view_percentage Function--#
    # Showing Vaccine Success and fail Rates
    # Showing the amount of people who took the vaccine and success
    def view_percentage():
        count = 0  # The amount of Vaccine success
        amount_people = 0               # The amount of people who took the vaccine
        Mycursor.execute("SELECT * FROM details")
        myresult = Mycursor.fetchall()  # fetchall = sql code for get info from DB table
        for row in myresult:
            amount_people = amount_people + 1
            for succ in row:
                if succ == 'yes':
                    count = count + 1
        # print(amount_people)
        succ_rate1 = (count / amount_people) * 100
        fail_rate2 = 100 - succ_rate1
        succ = float(succ_rate1)
        fail = float(fail_rate2)

        labels = ('Vaccine Success', 'Vaccine Failure')
        sizes = [succ, fail]
        explode = (0, 0)                # only "explode" the 2nd slice (i.e. 'Hogs')
        colors = ['green', 'red']

        fig, ax1 = plt.subplots(facecolor='c')
        ax1.pie(sizes,colors=colors, explode=explode, labels=labels, autopct='%0.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')               # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.xlabel( "The Vaccine success Number is {} successful out of {} people".format(count,amount_people), {"size": 12})
        Succ_Fail_Update(succ_rate1, fail_rate2)
        plt.show()


    #--Succ_Fail_Update Function--#
    #Save the Success and Failures precentage in the Database
    def Succ_Fail_Update(succ_rate1, fail_rate2):
        # Mycursor.execute("SELECT * FROM viewinfo")
        # myresult2 = Mycursor.fetchall()

        sqll = (" INSERT INTO viewInfo (Succ_rate,Fail_rate) VALUES (00.00, 00.00) ")
        Mycursor.execute(sqll)
        connection.commit()

        Mycursor.execute("SELECT * FROM viewinfo")
        myresult2 = Mycursor.fetchall()
        connection.commit()

        sql1 = (" UPDATE viewinfo SET Succ_rate = '{}' WHERE Fail_rate = '{}' ".format(succ_rate1, myresult2[0][1]))
        Mycursor.execute(sql1)
        connection.commit()
        sql = (" UPDATE viewinfo SET Fail_rate = '{}' WHERE Fail_rate = '{}' ".format(fail_rate2, myresult2[0][1]))
        Mycursor.execute(sql)
        connection.commit()

        sqll = (" DELETE FROM `viewinfo` WHERE Succ_rate='{}' ".format(00.00))
        Mycursor.execute(sqll)
        connection.commit()


    #--view_information_table Function--#
    #Grep Data From Database and Show Data in a Table
    def view_information_table():
        screen5 = tk.Tk()
        screen5.geometry("600x400")
        screen5.title("Application")

        Mycursor.execute("SELECT * FROM details")
        myresult = Mycursor.fetchall()

        table = ttk.Treeview(screen5, height = 23)
        table['show']='headings'            #delete the first empty column

        #for change the theme column looks(back ground columns) and size and color
        theme=ttk.Style(screen5)
        theme.theme_use("clam")
        theme.configure(".", font=('Helvetica', 12))
        theme.configure("Treeview.Heading", foreground='blue', font=('Helvetica', 12,"bold"))

        #Define number of columns
        table["columns"] = ("id", "Fname", "Lname", "ID Number", "City", "Question", "Stamp")

        #Assign the width,minwidth and anchor to the respective columns
        table.column("id", width=50, minwidth=50, anchor=tk.CENTER)
        table.column("Fname", width=100, minwidth=100, anchor=tk.CENTER)
        table.column("Lname", width=100, minwidth=100, anchor=tk.CENTER)
        table.column("ID Number", width=150, minwidth=150, anchor=tk.CENTER)
        table.column("City", width=100, minwidth=100, anchor=tk.CENTER)
        table.column("Question", width=50, minwidth=50, anchor=tk.CENTER)
        table.column("Stamp", width=150, minwidth=150, anchor=tk.CENTER)

        table.heading("id", text="id", anchor=tk.CENTER)
        table.heading("Fname", text="Fname", anchor=tk.CENTER)
        table.heading("Lname", text="Lname", anchor=tk.CENTER)
        table.heading("ID Number", text="ID Number", anchor=tk.CENTER)
        table.heading("City", text="City", anchor=tk.CENTER)
        table.heading("Question", text="Question", anchor=tk.CENTER)
        table.heading("Stamp", text="Stamp", anchor=tk.CENTER)

        i = 0
        for ro in myresult:
            table.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6],))
            i = i + 1

        # creating a scrollbar ttk.scrollbar with set orient=horizontal for X and orient=vertical for Y
        hsb = ttk.Scrollbar(screen5, orient="horizontal", command=table.xview)

        hsb.configure(command=table.xview)
        table.configure(xscrollcommand=hsb.set)
        hsb.pack(fill=X, side=BOTTOM)

        hsb2 = ttk.Scrollbar(screen5,orient="vertical", command=table.yview)
        hsb2.configure(command=table.yview)
        table.configure(yscrollcommand=hsb2.set)
        hsb2.pack(fill=Y,side = RIGHT)

        # table.place(x=50,y=50)
        table.pack()
        screen5.mainloop()


    view_info_Table_Button = tk.Button(screen4, text="View information table", width=30, bd=5, bg="dark green", font=("Arial", 15), command=view_information_table)
    view_info_Table_Button.place(x=100, y=50)

    success_failure_Button = tk.Button(screen4, text="View Success and Failure percentage", width=30, bd=5, bg="dark green", font=("Arial", 15), command=view_percentage)
    success_failure_Button.place(x=100, y=150)

    Menu_Button = tk.Button(screen4, text="Main Menu", width=14, height = 3, bd=5, bg="dark red", font=("Arial", 12, "bold"), command=Menu)
    # Menu_Button.grid(row=16, column=0,)
    Menu_Button.place(x=100, y=250)

    exit_Button = tk.Button(screen4, text="EXIT", width=14, height = 3, bd=5, bg="dark red", font=("Arial", 12, "bold"), command=screen4.destroy)
    exit_Button.place(x=300, y=250)

    screen4.mainloop()


# --Manage_Page Function--#
# choices Add Record, Edit/Manage Record, Delete Record
def Manage_Page():
    screen3 = Tk()
    screen3.geometry("600x600")#1200x1000
    screen3.title("Application")
    screen3.configure(bg="LightSkyBlue1")
    # image1 = Image.open("Cc.jpg")
    # image1 = image1.resize((600, 600), Image.ANTIALIAS)
    # test = ImageTk.PhotoImage(image1)
    # label1 = tkinter.Label(image=test)
    # label1.image = test
    # label1.place(x=0,y=0)

    def Menu():
        screen3.destroy()
        Second_Page()

    # --isNumber Function--#
    # check User ID Input if its int or str
    def isNumber(IDinput_check):
        for i in range(len(IDinput_check)):
            if IDinput_check[i].isdigit() != True:
                return False
        return True

    # --checkISetInfo_string Function--#
    # check user Input if its valid
    def checkISetInfo_string(input):
        if input.replace(" ", "").isalpha():
            return True
        else:
            return False

    # --Encrypted_Stamp Function--#
    # Check if ID number if already exists in the system
    def Encrypted_Stamp(ID_Stamp_Check):
        Mycursor.execute("SELECT encrypted_stamp FROM details")
        myresult = Mycursor.fetchall()
        m = hashlib.md5()
        for s in ID_Stamp_Check:
            m.update(s.encode())
        fn = m.hexdigest()

        if (fn,) in myresult:
            return True
        else:
            return False

    #update Function save records in database After make Changes on Record
    def update():
        record_id = delete_box.get()
        if checkISetInfo_string(f_name_editor.get()) == False:
            messagebox.showerror("Error", "Invalid Name, please try again!")
        elif checkISetInfo_string(l_name_editor.get()) == False:
            messagebox.showerror("Error", "Invalid Last Name, please try again!")
        elif isNumber(ID_editor.get()) == False:
            messagebox.showerror("Error", "Invalid ID number, please try again!")
        elif len(ID_editor.get()) != 9:
            messagebox.showerror("Error", "ID number length illegal, please try again!")
        # elif Encrypted_Stamp(ID_editor.get()) == True:
        #     messagebox.showerror("Error", "Invalid ID number already exists in the system")
        elif checkISetInfo_string(city_editor.get()) == False:
            messagebox.showerror("Error", "Invalid City name, please try again!")
        elif checkISetInfo_string(qusetion_editor.get()) == False:
            messagebox.showerror("Error", "Invalid input its not string, in Qusetion Please answer yes or no")
        elif qusetion_editor.get() != 'yes' and qusetion_editor.get() != 'no' and qusetion_editor.get() != 'YES' and qusetion_editor.get() != 'NO':
            messagebox.showerror("Error", "Invalid input, in Qusetion Please answer yes or no")
        else:
            sql = " UPDATE details SET Fname = '{}' WHERE ID_index = '{}'".format(f_name_editor.get(), record_id)
            Mycursor.execute(sql)
            connection.commit()
            sql = " UPDATE details SET Lname = '{}' WHERE ID_index = '{}'".format(l_name_editor.get(), record_id)
            Mycursor.execute(sql)
            connection.commit()
            sql = " UPDATE details SET ID_Number = '{}' WHERE ID_index = '{}'".format(ID_editor.get(), record_id)
            Mycursor.execute(sql)
            connection.commit()
            sql = " UPDATE details SET City = '{}' WHERE ID_index = '{}'".format(city_editor.get(), record_id)
            Mycursor.execute(sql)
            connection.commit()
            sql = " UPDATE details SET Successed = '{}' WHERE ID_index = '{}'".format(qusetion_editor.get(), record_id)
            Mycursor.execute(sql)
            connection.commit()
            SaveData()
            editor.destroy()

    #Create Screen window for Edit Function to update Record in DB by clicking on Save Button(calling update Function)
    def edit():
        global editor
        editor = Tk()
        editor.geometry("400x400")  # 1200x1000
        editor.title("Update A Record")
        editor.configure(bg="LightSkyBlue1")

        Mycursor.execute("SELECT * FROM details WHERE  ID_index = '{}'".format(delete_box.get()))
        myresult = Mycursor.fetchall()

        #Creat Global Variables for text box names
        global f_name_editor
        global l_name_editor
        global ID_editor
        global city_editor
        global qusetion_editor
        global stamp_editor

        # creat text Boxes
        f_name_editor = Entry(editor, width=30)
        f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
        l_name_editor = Entry(editor, width=30)
        l_name_editor.grid(row=1, column=1)
        ID_editor = Entry(editor, width=30)
        ID_editor.grid(row=2, column=1)
        city_editor = Entry(editor, width=30)
        city_editor.grid(row=3, column=1)
        qusetion_editor = Entry(editor, width=30)
        qusetion_editor.grid(row=4, column=1)
        # stamp_editor = Entry(editor, width=30)
        # stamp_editor.grid(row=5, column=1)

        # creat Text Box Labels
        f_name_label = Label(editor, text="First Name",bg="LightSkyBlue1")
        f_name_label.grid(row=0, column=0)
        l_name_label = Label(editor, text="Last Name",bg="LightSkyBlue1")
        l_name_label.grid(row=1, column=0)
        ID_label = Label(editor, text="ID Number",bg="LightSkyBlue1")
        ID_label.grid(row=2, column=0)
        city_label = Label(editor, text="City",bg="LightSkyBlue1")
        city_label.grid(row=3, column=0)
        question_label = Label(editor, text="is the Vaccnise Succsed?",bg="LightSkyBlue1")
        question_label.grid(row=4, column=0)
        # stamp_label = Label(editor, text="Stamp")
        # stamp_label.grid(row=5, column=0)

        for record in myresult:
            f_name_editor.insert(0, record[1])
            l_name_editor.insert(0, record[2])
            ID_editor.insert(0, record[3])
            city_editor.insert(0, record[4])
            qusetion_editor.insert(0, record[5])
            # stamp_editor.insert(0, record[6])

            # Creat a Save Button to save edited record
            save_Button = Button(editor, text="Save Record", bg="dark green", command=update)
            save_Button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)  # x=130, y=850

    #creat Function to Delete a record and reset Id index
    def delete():
        sql = "DELETE FROM details WHERE ID_index = '{}'".format(delete_box.get())
        sql22 = "SET @num := 0; "
        sql23 = "UPDATE details SET ID_index = @num :=(@num+1); "
        sql24 = "ALTER TABLE details AUTO_INCREMENT = 1;"
        Mycursor.execute(sql)
        Mycursor.execute(sql22)
        Mycursor.execute(sql23)
        Mycursor.execute(sql24)

        connection.commit()
        SaveData()
        delete_box.delete(0, END)

    # --setInfo Function--#
    # Data reception for a database
    def setInfo():
        x = 1
        if checkISetInfo_string(f_name.get()) == False:
            messagebox.showerror("Error", "Invalid Name, please try again!")
        elif checkISetInfo_string(l_name.get()) == False:
            messagebox.showerror("Error", "Invalid Last Name, please try again!")
        elif isNumber(ID.get()) == False:
            messagebox.showerror("Error", "Invalid ID number, please try again!")
        elif len(ID.get()) != 9:
            messagebox.showerror("Error", "ID number length illegal, please try again!")
        elif Encrypted_Stamp(ID.get()) == True:
            messagebox.showerror("Error","Invalid ID number already exists in the system")
        elif checkISetInfo_string(city.get()) == False:
            messagebox.showerror("Error", "Invalid City name, please try again!")
        elif checkISetInfo_string(qusetion.get()) == False:
            messagebox.showerror("Error", "Invalid input its not string, in Qusetion Please answer yes or no")
        elif qusetion.get() != 'yes' and qusetion.get() != 'no' and qusetion.get() != 'YES' and qusetion.get() != 'NO':
            messagebox.showerror("Error", "Invalid input, in Qusetion Please answer yes or no")
        else:
            #encrypted_stamp ID Loop
            m = hashlib.md5()
            for s in ID.get():
                m.update(s.encode())
            encStamp = m.hexdigest()

            # #ecrypted/encode ID number & save in DATABASE
            # alphabet_Num = '0123456789'
            # key = 5
            # encryptID = ''
            # for i in ID.get():
            #     post = alphabet_Num.find(i)
            #     newpost = (post + key) % 10  # 10%10=0
            #     encryptID += alphabet_Num[newpost]

            sql = (" INSERT INTO details (Fname,Lname,ID_Number,City,Successed,encrypted_stamp) VALUES (%s, %s, %s, %s, %s, %s) ")
            vals = (f_name.get(), l_name.get(), ID.get(), city.get(), qusetion.get(),encStamp)
            Mycursor.execute(sql, vals)
            connection.commit()

            print(colored("The data was saved to the database", "green"))
            SaveData()
            f_name.delete(0, END)
            l_name.delete(0, END)
            ID.delete(0, END)
            city.delete(0, END)
            qusetion.delete(0, END)

    #creat Query Function to view/show information from DB
    def viewInfo():
        pass
        # Mycursor.execute("SELECT * FROM details")
        # myresult = Mycursor.fetchall()
        #
        # print_records = ''
        # for record in myresult:
        #     print_records += str(record) + "\n"
        #
        # query_label = Label(screen3, text=print_records)
        # query_label.grid(row=12, column=0, columnspan=2)

        connection.commit()
    #creat text Boxes
    f_name = Entry(screen3,width=30)
    f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name = Entry(screen3,width=30)
    l_name.grid(row=1, column=1)
    ID = Entry(screen3,width=30)
    ID.grid(row=2, column=1)
    city = Entry(screen3,width=30)
    city.grid(row=3, column=1)
    qusetion = Entry(screen3,width=30)
    qusetion.grid(row=4, column=1)
    delete_box = Entry(screen3, width=30)
    delete_box.grid(row=9, column=1, pady=5)

    #creat Text Box Labels
    f_name_label = Label(screen3, text ="First Name", bg="LightSkyBlue1", font=("Arial", 12, "bold"))
    f_name_label.grid(row=0, column=0, pady=(10, 0))
    l_name_label = Label(screen3, text ="Last Name", bg="LightSkyBlue1", font=("Arial", 12, "bold"))
    l_name_label.grid(row=1, column=0)
    ID_label = Label(screen3, text ="ID Number", bg="LightSkyBlue1", font=("Arial", 12, "bold"))
    ID_label.grid(row=2, column=0)
    city_label = Label(screen3, text ="City", bg="LightSkyBlue1", font=("Arial", 12, "bold"))
    city_label.grid(row=3, column=0)
    question_label = Label(screen3, text ="is the Vaccnise Succsed?", bg="LightSkyBlue1", font=("Arial", 12, "bold"))
    question_label.grid(row=4, column=0)
    delete_box_label = Label(screen3, text="Select ID index", bg="LightSkyBlue1", font=("Arial", 12, "bold"))
    delete_box_label.grid(row=9, column=0, pady=5)

    #creat Sumbit Button
    submit_Button = Button(screen3, text="Add Record",bg="dark green", font=("Arial", 12, "bold"), command=setInfo)
    submit_Button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)#x=130, y=850

    #creat Query Button
    # query_Button = Button(screen3, text="show Record",bg="dark green", command=viewInfo)
    # query_Button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)#x=130, y=850

    #creat delete Button
    delete_Button = Button(screen3, text="Delete Record",bg="dark green", font=("Arial", 12, "bold"), command=delete)
    delete_Button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)#x=130, y=850

    #creat Update Button
    edit_Button = Button(screen3, text="Edit Record",bg="dark green", font=("Arial", 12, "bold"), command=edit)
    edit_Button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=143)#x=130, y=850

    Menu_Button = tk.Button(screen3, text="Main Menu", width=14, height = 3, bd=5, bg="dark red", font=("Arial", 12, "bold"), command=Menu)
    # Menu_Button.grid(row=16, column=0,)
    Menu_Button.place(x=100, y=450)

    exit_Button = tk.Button(screen3, text="EXIT", width=14, height = 3, bd=5, bg="dark red", font=("Arial", 12, "bold"), command=screen3.destroy)
    exit_Button.place(x=400, y=450)

    screen3.mainloop()


#--SaveData--#
#Save data to a file if the system crashes
def SaveData():
    Mycursor.execute("SELECT * FROM details")
    myresult = Mycursor.fetchall()
    connection.commit()

    with open('SaveData', 'w') as fp:
        fp.write('\n'.join('{} {} {} {} {} {}'.format(x[0], x[1], x[2], x[3], x[4], x[5]) for x in myresult))

    return print(colored("Data Saved in File name: 'SaveData.txt'", "green"))


#--Second page Function--#
#the main menu, Choices page(Manage information, View information, EXIT)
def Second_Page():
    screen2 = tk.Tk()
    screen2.geometry("800x600")
    screen2.title("Application")

    image1 = Image.open("Cc.jpg")
    image1 = image1.resize((800, 600), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    label1 = tkinter.Label(image=test)
    label1.image = test
    label1.pack()

    def Show_infoScreen():
        screen2.destroy()
        Show_info_Screen()

    def Manage_screen():
        screen2.destroy()
        Manage_Page()


    MangeB1 = tk.Button(screen2, text="Manage information", width=40, bd=5, bg="dark green", font=("Arial", 15),command=Manage_screen )
    MangeB1.place(x=210, y=175)
    viewB2 = tk.Button(screen2, text="View information", width=40, bd=5, bg="dark green", font=("Arial", 15), command=Show_infoScreen)
    viewB2.place(x=210, y=275)
    exitB3 = tk.Button(screen2, text="EXIT", width=40, bd=5, bg="dark red", font=("Arial", 15), command=screen2.destroy)
    exitB3.place(x=210, y=375)

    screen2.mainloop()


# --Registry Function--#
# Registration to the system / username,password,Email
def register_page():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("500x350")
    screen1.configure(bg="deep sky blue")

    global username
    global password
    global email
    global username_entry
    global password_entry
    global email_entry

    username = tk.Label(screen1, text="Username:", font=("Arial", 15), bg="deep sky blue")
    username.place(x=10, y=10)
    username_entry = tk.Entry(screen1, width=30, bd=5)
    username_entry.place(x=200, y=10)

    password = tk.Label(screen1, text="Password:", font=("Arial", 15), bg="deep sky blue")
    password.place(x=10, y=60)
    password_entry = tk.Entry(screen1, width=30, bd=5, show='*')
    password_entry.place(x=200, y=60)

    email = tk.Label(screen1, text="Email:", font=("Arial", 15), bg="deep sky blue")
    email.place(x=10, y=110)
    email_entry = tk.Entry(screen1, width=30, bd=5)
    email_entry.place(x=200, y=110)

    # --registry user Function--#
    #Check An invalid  input and formating to encode and Save in Database
    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()

        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not (EMAIL_REGEX.match(email)):
            messagebox.showerror("Error", "Invalid Email, please Try again")
        elif username == "" or password == "" or email == "":
            messagebox.showerror("Error", "Please fill the complete field!!")
        else:
            m = hashlib.md5()
            m2 = hashlib.md5()
            m3 = hashlib.md5()
            for s in username:
                m.update(s.encode())
            username_encStamp = m.hexdigest()
            for s2 in password:
                m2.update(s2.encode())
            password_encStamp = m2.hexdigest()
            for s3 in email:
                m3.update(s3.encode())
            email_encStamp = m3.hexdigest()

            sql = (" INSERT INTO user (username,passwd,Email) VALUES (%s, %s, %s) ")
            vals = (username_encStamp, password_encStamp, email_encStamp)
            Mycursor.execute(sql, vals)
            connection.commit()
            messagebox.showinfo("Welcome", "You are registered successfully")
            return screen1.destroy()

    B22 = tk.Button(screen1, text="Sign in", bg="dark orange", font=("Arial", 15), command=register_user)
    B22.place(x=200, y=200)


#--login_Page Function--#
#Login to the system and Register Button for registration
#After registration successfully and Login successfully , it will open Second_Page(the main menu)
def login_Page():
    try:
        global screen
        screen = tk.Tk()
        screen.geometry("800x600")
        screen.title("Application")
        Label(text="Welcome", bg="grey", width="300", height="2", font=("Calibri", 16)).pack()
        Label(text="").pack()

        border = tk.LabelFrame(screen, text='Login', bg='ivory', bd=10, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx=150, pady=150)

        userName = tk.Label(screen, text="Username:", font=("Arial Bold", 15))
        userName.place(x=230, y=275)
        UserInput = tk.Entry(screen, width=30, bd=5)
        UserInput.place(x=360, y=278)
        userPass = tk.Label(screen, text="Password:", font=("Arial Bold", 15))
        userPass.place(x=230, y=320)
        PassInput = tk.Entry(screen, width=30, bd=5, show='*')
        PassInput.place(x=360, y=320)

        def verify():
            Mycursor.execute("SELECT username FROM user")
            myuser = Mycursor.fetchall()
            Mycursor.execute("SELECT passwd FROM user")
            mypass = Mycursor.fetchall()

            username = UserInput.get()
            password = PassInput.get()

            m3 = hashlib.md5()
            m4 = hashlib.md5()
            for s in username:
                m3.update(s.encode())
            username2 = m3.hexdigest()
            for s2 in password:
                m4.update(s2.encode())
            password2 = m4.hexdigest()

            if (username2,) in myuser and (password2,) in mypass:
                screen.destroy()
                Second_Page()
            else:
                messagebox.showinfo("Error", "Please provide correct username and password!!")

        B1 = tk.Button(screen, text="Submit", font=("Arial", 15), command=verify)
        B1.place(x=530, y=348)

        B2 = tk.Button(screen, text="Register", bg="dark orange", font=("Arial", 15), command=register_page)
        B2.place(x=680, y=60)

        # b3 = tk.Button(screen, text="EXIT", width=14, height=3, bd=5, bg="dark red",font=("Arial", 12, "bold"), command=exit)
        # b3.place(x=640, y=500)

        screen.mainloop()

    except pymysql.Error:
        messagebox.showinfo("Error", "Database connection failed {}".format(pymysql.Error))
        login_Page()
    except TypeError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()
    except MemoryError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()
    except ImportError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()
    except IndexError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()
    except NameError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()
    except ValueError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()
    except FileNotFoundError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()
    except SyntaxError as err:
        messagebox.showinfo("Error {}".format(err))
        login_Page()


# --main Function--#
##check if Tables Exits in Database by calling check Table Exits Function else it we be created.
##After create tables success, will open login_Page
def main():
    def check_Table_Exits():
        Mycursor.execute('SHOW TABLES')
        cnt = 0
        for table in Mycursor:
            if 'details' in table:
                cnt = cnt + 1
                return cnt

    if check_Table_Exits() == 1:
        login_Page()
    else:
        Mycursor.execute('CREATE TABLE user (username VARCHAR(255), passwd VARCHAR(255), Email VARCHAR(255))')
        Mycursor.execute('CREATE TABLE details (ID_index INT unsigned PRIMARY KEY AUTO_INCREMENT, Fname VARCHAR(20),Lname VARCHAR(20),ID_Number INT(9),City VARCHAR(20),Successed VARCHAR(3),encrypted_stamp VARCHAR(255))')
        Mycursor.execute('CREATE TABLE viewInfo (Succ_rate FLOAT(4,2), Fail_rate FLOAT(4,2))')
        print(colored("Tables Created in Database.", "green"))
        login_Page()

if __name__ == main():
    main()