from tkinter import *
from PIL import Image, ImageTk
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass
import sqlite3

class RSE:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Set window to full screen
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.config(bg="thistle")

        # === Title Bar ===
        title = Label(self.root, text="Student Result Management",
                      padx=10, compound=LEFT,
                      font=("Goudy Old Style", 20, "bold"),
                      bg="#033054", fg="white")
        title.place(relx=0, y=0, relwidth=1, height=50)

        # ... (keep previous imports and class definition unchanged until menu_frame section)

        # === Menu Frame ===
        menu_frame = LabelFrame(self.root, text="Menu", font=("Times New Roman", 15), bg="mistyrose")
        menu_frame.place(relx=0.01, rely=0.08, relwidth=0.98, relheight=0.1)

        # === Menu Buttons === (Improved proportional spacing)
        buttons = [
            ("Course", self.add_course),
            ("Student", self.add_student),
            ("Result", self.add_result),
            ("View Results", self.add_report)  # Shortened text for better fit
        ]

        # Calculate dynamic button width and spacing
        num_buttons = len(buttons)
        button_spacing = 0.02  # 2% space between buttons
        total_spacing = (num_buttons - 1) * button_spacing
        button_width = (1 - total_spacing) / num_buttons

        x_position = 0.0
        for text, command in buttons:
            Button(menu_frame, text=text, font=("Goudy Old Style", 15, "bold"),
                   bg="#0b5377", fg="white", cursor="hand2", command=command,
                   anchor="center", wraplength=150  # Ensures text wraps if needed
                   ).place(relx=x_position, rely=0.1, relwidth=button_width, relheight=0.8)
            x_position += button_width + button_spacing

        # ... (rest of the code remains the same)
        # === Background Image ===
        try:
            bg_img = Image.open("images/bg3.png")
            bg_img = bg_img.resize((self.screen_width, int(self.screen_height*0.5)), Image.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(bg_img)
            Label(self.root, image=self.bg_img).place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.5)
        except Exception as e:
            print(f"Error loading background image: {e}")

        # === Statistics Section === (Responsive positioning)
        self.statistics = {
            "course": {"relx": 0.05, "bg": "red", "label": None},
            "student": {"relx": 0.35, "bg": "#0676ad", "label": None},
            "result": {"relx": 0.65, "bg": "#038074", "label": None}
        }

        for stat, config in self.statistics.items():
            config["label"] = Label(self.root, text=f"Total {stat.capitalize()}\n[0]", 
                                   font=("Goudy Old Style", 20), bd=10, relief=RIDGE,
                                   bg=config["bg"], fg="white")
            config["label"].place(relx=config["relx"], rely=0.75, relwidth=0.25, relheight=0.15)

        # === Footer ===
        Label(self.root, 
              text="SRMS - Student Result Management System\nContact Us for any Technical Issue: 987xxxxx01",
              font=("Goudy Old Style", 12),
              bg="#262626", fg="white").pack(side=BOTTOM, fill=X)

        # Initialize real-time updates
        self.update_statistics()

    def update_statistics(self):
        try:
            con = sqlite3.connect(database="res.db")
            cur = con.cursor()
            
            counts = {
                "course": cur.execute("SELECT COUNT(*) FROM course").fetchone()[0],
                "student": cur.execute("SELECT COUNT(*) FROM student").fetchone()[0],
                "result": cur.execute("SELECT COUNT(*) FROM result").fetchone()[0]
            }
            
            for stat, count in counts.items():
                self.statistics[stat]["label"].config(text=f"Total {stat.capitalize()}\n[{count}]")
                
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}")
        finally:
            con.close()
        
        self.root.after(2000, self.update_statistics)

    # Window Management Methods
    def add_course(self):
        self._create_window(CourseClass)

    def add_student(self):
        self._create_window(studentClass)

    def add_result(self):
        self._create_window(resultClass)

    def add_report(self):
        self._create_window(reportClass)

    def _create_window(self, class_ref):
        new_win = Toplevel(self.root)
        new_win.state('zoomed')  # Open child windows maximized
        class_ref(new_win)

if __name__ == "__main__":
    root = Tk()
    obj = RSE(root)
    root.mainloop()
