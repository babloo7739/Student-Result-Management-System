from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        # === Title ===
        title = Label(self.root, text="View Student Result ", 
                     font=("Goudy Old Style", int(self.screen_width/60), "bold"), 
                     bg="orange", fg="#262626")
        title.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.06)

        # === Search Section ===
        self.var_search = StringVar()
        lbl_search = Label(self.root, text="Search By Roll No:", 
                          font=("goudy old style", int(self.screen_width/70)), 
                          bg="white")
        lbl_search.place(relx=0.25, rely=0.12, relwidth=0.2, relheight=0.04)

        txt_search = Entry(self.root, textvariable=self.var_search, 
                          font=("goudy old style", int(self.screen_width/70)), 
                          bg="lightyellow")
        txt_search.place(relx=0.45, rely=0.12, relwidth=0.15, relheight=0.04)

        # Search and Clear Buttons
        btn_width = 0.07  # 7% of screen width
        btn_search = Button(self.root, text="Search", 
                           font=("goudy old style", int(self.screen_width/70)), 
                           bg="#03a9f4", fg="white", cursor="hand2", command=self.search)
        btn_search.place(relx=0.62, rely=0.12, relwidth=btn_width, relheight=0.04)
        
        btn_clear = Button(self.root, text="Clear", 
                          font=("goudy old style", int(self.screen_width/70)), 
                          bg="gray", fg="white", cursor="hand2", command=self.clear)
        btn_clear.place(relx=0.71, rely=0.12, relwidth=btn_width, relheight=0.04)

        # === Result Section ===
        col_width = 0.12  # 12% of screen width
        start_x = 0.12    # Starting X position for columns
        
        # Headers
        headers = ["Roll No", "Name", "Course", "Marks Obtained", "Total Marks", "Percentage"]
        for i, header in enumerate(headers):
            Label(self.root, text=header, font=("goudy old style", int(self.screen_width/80), "bold"), 
                 bg="white", relief=GROOVE).place(
                relx=start_x + (i * col_width), rely=0.25, 
                relwidth=col_width, relheight=0.06
            )

        # Value Labels
        self.labels = {}
        for i, field in enumerate(["roll", "name", "course", "marks", "total", "percentage"]):
            self.labels[field] = Label(self.root, font=("goudy old style", int(self.screen_width/85)), 
                                bg="white", relief=GROOVE)
            self.labels[field].place(
                relx=start_x + (i * col_width), rely=0.31, 
                relwidth=col_width, relheight=0.08
            )

        # Delete Button
        btn_delete = Button(self.root, text="Delete", 
                           font=("goudy old style", int(self.screen_width/70)), 
                           bg="red", fg="white", cursor="hand2", command=self.delete)
        btn_delete.place(relx=0.45, rely=0.45, relwidth=0.1, relheight=0.05)

    def search(self):
        con = sqlite3.connect(database="res.db")
        cur = con.cursor()
        try:
            if not self.var_search.get():
                messagebox.showerror("Error", "Roll No. is required", parent=self.root)
                return
            
            cur.execute("SELECT * FROM result WHERE roll=?", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                fields = ["roll", "name", "course", "marks", "total", "percentage"]
                for field, value in zip(fields, row[1:7]):
                    self.labels[field].config(text=value)
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_search.set("")
        for label in self.labels.values():
            label.config(text="")

    def delete(self):
        if not self.var_search.get():
            messagebox.showerror("Error", "Roll No. is required", parent=self.root)
            return
        
        con = sqlite3.connect(database="res.db")
        cur = con.cursor()
        try:
            if messagebox.askyesno("Confirm", "Delete this result?", parent=self.root):
                cur.execute("DELETE FROM result WHERE roll=?", (self.var_search.get(),))
                if cur.rowcount > 0:
                    messagebox.showinfo("Success", "Result deleted", parent=self.root)
                    self.clear()
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
                con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()


