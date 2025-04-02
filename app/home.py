import customtkinter as ctk
from ui_components import *


class HomePage(ctk.CTkFrame):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master, fg_color=Colors.PRIMARY)
        self.master = master
        self.parent = parent
        self.student_data = kwargs.get("student_data")
 
        self.welcome_frame = ctk.CTkFrame(self.master, fg_color=Colors.PRIMARY, border_color=Colors.BACKGROUND)
        self.welcome_frame.pack(padx=10, pady=10, anchor="center")
        ctk.CTkLabel(self.welcome_frame, text="Welcome", font=("Arial", 18, "bold")).pack(padx=10, pady=10, side="left")
        ctk.CTkLabel(self.welcome_frame, text=f"{self.student_data["name"]}", font=("Arial", 16, "bold")).pack(padx=10, pady=10, side="left")



