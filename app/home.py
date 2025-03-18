import customtkinter as ctk
from PIL import Image
from utils import getPath, centerWindow
from ui_components import Colors
from results import ResultsPage
from exam_portal_page import ExamPortalPage


class QuickActionButton(ctk.CTkButton):
    def __init__(self, master, text, command, icon):
        super().__init__(master, text=text, command=command,
                        image=ctk.CTkImage(light_image=Image.open(getPath(icon)),
                        compound="left", anchor="w",
                        fg_color=Colors.SECONDARY,
                        hover_color=Colors.HIGHLIGHT))

class ExamCard(ctk.CTkFrame):
    def __init__(self, master, exam_data):
        super().__init__(master, fg_color=Colors.SECONDARY)
        self.exam_data = exam_data
        self.create_widgets()
        
    def create_widgets(self):
        ctk.CTkLabel(self, text=self.exam_data["name"], 
                   font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self, text=self.exam_data["date"]).grid(row=1, column=0, sticky="w")
        status_label = ctk.CTkLabel(self, text=self.exam_data["status"])
        status_label.grid(row=0, column=1, rowspan=2, padx=10)
        
        if self.exam_data["status"] == "Completed":
            status_label.configure(text_color=Colors.SUCCESS)
        elif self.exam_data["status"] == "Pending":
            status_label.configure(text_color=Colors.WARNING)
        else:
            status_label.configure(text_color=Colors.ACCENT)

class RecentExamsScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_cards()
        
    def create_cards(self):
        exams = [
            {"name": "Cloud Basics", "date": "2024-03-15", "status": "Completed"},
            {"name": "Security Exam", "date": "2024-03-18", "status": "Pending"},
            {"name": "Advanced Topics", "date": "2024-03-20", "status": "Upcoming"}
        ]
        
        for exam in exams:
            ExamCard(self, exam).pack(pady=5)

class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        ctk.CTkLabel(self, text="Welcome to Cloud Exam", 
                    font=("Arial", 24, "bold"),
                    text_color=Colors.Texts.HEADERS).pack(pady=20)
        
        # Main Content
        content_frame = ctk.CTkFrame(self, fg_color=Colors.PRIMARY)
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Left Column
        left_col = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=20)
        
        ctk.CTkLabel(left_col, text="Recent Exams",
                   font=("Arial", 16, "bold")).pack(anchor="w")
        
        # Add recent exam cards
        self.recent_exams = RecentExamsScrollFrame(left_col)
        self.recent_exams.pack(expand=True, fill="both", pady=10)
        
        # Right Column
        right_col = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=20)
        
        ctk.CTkLabel(right_col, text="Quick Actions",
                   font=("Arial", 16, "bold")).pack(anchor="w")
        
        # Quick action buttons
        QuickActionButton(right_col, text="Start New Exam", 
                        command=lambda: self.master.redirect(ExamPortalPage),
                        icon="assets/images/exam_icon.png").pack(pady=5)
        
        QuickActionButton(right_col, text="View Results", 
                        command=lambda: self.master.redirect(ResultsPage),
                        icon="assets/images/results_icon.png").pack(pady=5)