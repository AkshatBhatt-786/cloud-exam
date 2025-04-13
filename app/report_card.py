import customtkinter as ctk
from ui_components import *
from utils import centerWindow, getPath
from PIL import Image

class ReportCard(ctk.CTkToplevel):
    def __init__(self, master, student_data, exam_id, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Exam Report")
        self.geometry(centerWindow(master, 1200, 800, self._get_window_scaling(), (0, 150)))
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.configure(fg_color=Colors.BACKGROUND)

        exam_data = student_data["exams"][exam_id]["result"]

        main_frame = ctk.CTkFrame(self, fg_color=Colors.BACKGROUND)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header = ctk.CTkFrame(main_frame, fg_color=Colors.PRIMARY, corner_radius=20)
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header,
            text="Exam Report",
            image=ctk.CTkImage(light_image=Image.open(getPath("assets\\images\\cloud_logo.png")), size=(40, 40)),
            compound="left",
            font=(BOLD_FONT, 28, "bold"),
            text_color=Colors.Texts.HEADERS
        ).pack(side="left", padx=25, pady=15)
        
        ctk.CTkLabel(
            header,
            text=f"#{exam_id}",
            font=(BOLD_FONT, 18),
            text_color=Colors.Texts.PLACEHOLDER
        ).pack(side="right", padx=25, pady=15)

        # --- Student Info Grid ---
        info_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_grid.pack(fill="x", pady=10)
        
        info_items = [
            ("👤 Name", student_data["name"]),
            ("🎓 Enrollment", student_data["enrollment_no"]),
            ("🏫 College ID", student_data["college_id"])
        ]
        
        for col, (label, value) in enumerate(info_items):
            frame = ctk.CTkFrame(info_grid, fg_color="transparent")
            frame.grid(row=0, column=col, padx=10, sticky="nsew")
            ctk.CTkLabel(frame, text=label, 
                       font=(BOLD_FONT, 12),
                       text_color=Colors.Texts.PLACEHOLDER).pack(anchor="w")
            ctk.CTkLabel(frame, text=value, 
                       font=(BOLD_FONT, 14),
                       text_color=Colors.Texts.HEADERS).pack(anchor="w")

        # --- Score Cards ---
        score_Cards = ctk.CTkFrame(main_frame, fg_color="transparent")
        score_Cards.pack(fill="x", pady=15)
        
        self._create_score_card(score_Cards, "✅ Correct", 
                              exam_data["correct_count"], exam_data["marks_correct"], Colors.SUCCESS)
        self._create_score_card(score_Cards, "❌ Wrong", 
                              exam_data["wrong_count"], exam_data["marks_wrong"], Colors.DANGER)
        self._create_score_card(score_Cards, "⏭ Skipped", 
                              exam_data["not_attempted"], exam_data["marks_not_attempted"], Colors.WARNING)

        # --- Total Score Display ---
        total_frame = ctk.CTkFrame(main_frame, fg_color=Colors.ACCENT, corner_radius=20)
        total_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(total_frame, text="TOTAL SCORE",
                   font=(BOLD_FONT, 16),
                   text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(total_frame, text=f"{exam_data['total_score']}",
                   font=(BOLD_FONT, 42, "bold"),
                   text_color="white").pack(pady=(0, 15))

        analysis_frame = ctk.CTkFrame(main_frame, fg_color=Colors.SECONDARY, corner_radius=15)
        analysis_frame.pack(fill="x", pady=10)
        
        self._create_analysis_section(analysis_frame, "Correct Answers", 
                                    exam_data["correct_answers_ids"], Colors.SUCCESS)
        self._create_analysis_section(analysis_frame, "Wrong Answers", 
                                    exam_data["wrong_answers_ids"], Colors.DANGER)
        self._create_analysis_section(analysis_frame, "Not Attempted", 
                                    exam_data["not_attempted_ids"], Colors.WARNING)

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="Close Report", 
                    font=(BOLD_FONT, 14),
                    width=120,
                    fg_color=Colors.Buttons.PRIMARY,
                    hover_color=Colors.Buttons.PRIMARY_HOVER,
                    command=self.destroy).pack(pady=10)

    def _create_score_card(self, parent, title, count, marks, color):
        card = ctk.CTkFrame(parent, fg_color=Colors.Cards.BACKGROUND, 
                          border_color=Colors.Cards.BORDER,
                          border_width=1,
                          corner_radius=15)
        card.pack(side="left", expand=True, padx=5, pady=5)
        
 
        ctk.CTkLabel(card, text=title,
                   font=(BOLD_FONT, 14),
                   text_color=color).pack(padx=10, pady=(10, 0))
      
        ctk.CTkLabel(card, text=f"{count} Questions",
                   font=(BOLD_FONT, 20, "bold"),
                   text_color=Colors.Texts.HEADERS).pack(padx=10, pady=5)
        
        ctk.CTkLabel(card, text=f"{marks} Marks",
                   font=(BOLD_FONT, 16),
                   text_color=Colors.Texts.PLACEHOLDER).pack(padx=10, pady=(0, 10))

    def _create_analysis_section(self, parent, title, items, color):
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=15, pady=10)
        
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=title,
                   font=(BOLD_FONT, 14, "bold"),
                   text_color=color).pack(side="left")
        ctk.CTkLabel(header, text=f"({len(items)})",
                   font=(BOLD_FONT, 14),
                   text_color=Colors.Texts.PLACEHOLDER).pack(side="left", padx=5)
    
        tag_frame = ctk.CTkFrame(section, fg_color="transparent")
        tag_frame.pack(fill="x", pady=5)
        
        for qid in items:
            ctk.CTkLabel(tag_frame, text=qid,
                       font=(BOLD_FONT, 14, "bold"),
                       fg_color=color,
                       text_color="#333333",
                       corner_radius=8,
                       padx=8,
                       pady=2).pack(side="left", padx=2)