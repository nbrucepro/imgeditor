from tkinter import Tk
from auth import AuthApp
from database import create_table

create_table()

root = Tk()
AuthApp(root)
root.mainloop()

