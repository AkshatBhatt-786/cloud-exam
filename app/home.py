import customtkinter as ctk
from ui_components import *
from report_card import ReportCard

class HomePage(ctk.CTkFrame):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master, fg_color=Colors.PRIMARY)
        self.master = master
        self.parent = parent
        self.student_data = kwargs.get("student_data")

        self.welcome_section = ctk.CTkFrame(self.master, fg_color=Colors.PRIMARY)
        self.welcome_section.pack(anchor="w", pady=(0, 30), padx=10)

        welcome_lbl = ctk.CTkLabel(
            self.welcome_section,
            text=f"Welcome",
            font=(BOLD_FONT, 52, "bold"),
            text_color=Colors.Texts.HEADERS
        )
        welcome_lbl.pack(pady=26, side="left", padx=10, anchor="sw")

        name_label = ctk.CTkLabel(
            self.welcome_section,
            text=f"{self.student_data['name']}",
            font=(BOLD_FONT, 32, "bold"),
            text_color=Colors.ACCENT
        )
        name_label.pack(pady=32, side="left", padx=10, anchor="sw")

        self.info_frame = ctk.CTkFrame(self.master, fg_color=Colors.PRIMARY)
        self.info_frame.pack(anchor="w", pady=(0, 10))

        enroll_lbl = ctk.CTkLabel(
            self.info_frame,
            text=f"Enrollment Number: {self.student_data['enrollment_no']}",
            font=(ITALIC_BOLD_FONT, 16, "italic"),
            text_color=Colors.Texts.HEADERS
        )
        enroll_lbl.pack(side="left", padx=10, pady=5)

        college_id_lbl = ctk.CTkLabel(
            self.info_frame,
            text=f"College ID: {self.student_data['college_id']}",
            font=(ITALIC_BOLD_FONT, 16, "italic"),
            text_color=Colors.Texts.HEADERS
        )
        college_id_lbl.pack(side="left", padx=10, pady=5)

        ctk.CTkFrame(self.master, height=2, fg_color=Colors.ACCENT).pack(fill="x", pady=10)

        self.result_wrapper = ctk.CTkFrame(self.master, fg_color=Colors.PRIMARY)
        self.result_wrapper.pack(anchor="center", pady=10)

        self.result_frame = ctk.CTkScrollableFrame(
            self.result_wrapper,
            fg_color=Colors.SECONDARY,
            border_color=Colors.BACKGROUND,
            corner_radius=10,
            width=600 
        )
        self.result_frame.pack() 

        self.exams = self.student_data.get("exams", {})

        if not self.exams:
            ctk.CTkLabel(
                self.result_frame,
                text="No results to display.",
                font=(ITALIC_BOLD_FONT, 16),
                text_color=Colors.Texts.HEADERS
            ).pack(pady=20)
        else:
            for exam_id, exam_data in self.exams.items():
                exam_card = ctk.CTkFrame(self.result_frame, fg_color=Colors.BACKGROUND)
                exam_card.pack(fill="x", pady=5, padx=10)

                # Exam title
                ctk.CTkLabel(
                    exam_card,
                    text=f"{self.exams.get(exam_id).get("result").get("title", f'Exam {exam_id}')}",
                    font=(BOLD_FONT, 14),
                    text_color=Colors.Texts.HEADERS
                ).pack(side="left", padx=10, pady=10)

                view_btn = ctk.CTkButton(
                    exam_card,
                    text="View Report",
                    font=(BOLD_FONT, 12),
                    command=lambda e_id=exam_id: self.view_report(e_id)
                )
                view_btn.pack(side="right", padx=10, pady=10)
    
    def view_report(self, exam_id):
        ReportCard(self.master, self.student_data, exam_id)
