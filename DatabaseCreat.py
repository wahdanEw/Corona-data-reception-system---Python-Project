import pymysql
import colorama
from termcolor import colored
from tkinter import messagebox
colorama.init()
##---Database Connection---##
try:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 port=3306,
                                 )  # cursorclass=pymysql.cursors.DictCursor#charset='TRUE'
    Mycursor = connection.cursor()  # Mycursor to perform database operations
    print(colored("Database connection Succeeded\n", "green"))
except pymysql.Error:
    messagebox.showinfo("Error", "Database connection failed")
    print(colored("Database connection failed", "red"))

def DataBaseCREATE():
    Mycursor.execute('SHOW DATABASES')
    if ("detailsdb",) in Mycursor:
        return True
    else:
        Mycursor.execute('CREATE DATABASE DetailsDB')
        return False , print("Database Created.")
