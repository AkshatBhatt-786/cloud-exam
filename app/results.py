import customtkinter as ctk
from ui_components import *


class ResultsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        ctk.CTkLabel(self.master, text="Exam Results", 
                    font=("Arial", 24, "bold"),
                    text_color=Colors.Texts.HEADERS).pack(pady=20)
        
        # Results Table
        results_frame = ctk.CTkFrame(self.master, fg_color=Colors.PRIMARY)
        results_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Table Headers
        headers = ["Exam Name", "Date", "Score", "Status", "Details"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(results_frame, text=header,
                       font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10)
        
        # Sample Data
        exams = [
            ["Cloud Basics", "2024-03-15", "85%", "Passed"],
            ["Security Exam", "2024-03-18", "92%", "Passed"],
            ["Advanced Topics", "2024-03-20", "63%", "Failed"]
        ]
        
        for row, exam in enumerate(exams, start=1):
            for col, value in enumerate(exam):
                ctk.CTkLabel(results_frame, text=value).grid(row=row, column=col, padx=10)
            
            details_btn = ctk.CTkButton(results_frame, text="View Details",
                                      command=lambda e=exam: self.show_details(e))
            details_btn.grid(row=row, column=4, padx=10)

        # Chart Frame
        chart_frame = ctk.CTkFrame(self, fg_color=Colors.PRIMARY)
        chart_frame.pack(fill="x", padx=20, pady=20)
        
        # Add chart visualization here
        ctk.CTkLabel(chart_frame, text="Performance Chart").pack()

    def show_details(self, exam):
        # Show detailed results
        pass