import customtkinter as ctk
from ui_components import *
from PIL import Image


class HomePage(ctk.CTkFrame):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master, fg_color=Colors.PRIMARY)
        self.master = master
        self.parent = parent
        self.student_data = kwargs.get("student_data")
        self.hero_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.hero_frame.grid(row=0, column=0, pady=(40, 20), sticky="nsew")
        
        self.welcome_label = ctk.CTkLabel(
            self.hero_frame,
            text=f"Welcome, {self.student_data.get("name")}! 👋",
            font=("Arial", 24, "bold"),
            text_color=Colors.Texts.HEADERS
        )
        self.welcome_label.pack(pady=(0, 10))

        self.purpose_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.purpose_frame.grid(row=1, column=0, pady=20, sticky="nsew")

        ctk.CTkLabel(
            self.purpose_frame,
            text="Cloud-Based Examination Platform",
            font=("Arial", 32, "bold"),
            text_color=Colors.Texts.HEADERS,
            wraplength=600
        ).pack(pady=(0, 15))

        ctk.CTkLabel(
            self.purpose_frame,
            text=(
                "Cloud Exam revolutionizes traditional testing methods by providing:\n\n"
                "• Secure, browser-locked examinations\n"
                "• Cloud-based question paper distribution\n"
                "• Real-time progress monitoring\n"
                "• Instant result analytics\n"
                "• Encrypted answer submission system\n\n"
                "Start your exam anytime, anywhere with our reliable cloud exam platform."
            ),
            font=("Arial", 16),
            text_color=Colors.Texts.HEADERS,
            justify="left"
        ).pack(pady=10, anchor="w")

        self.features_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.features_grid.grid(row=2, column=0, pady=30, sticky="nsew")

        features = [
            ("Exam Papers Backups", "assets/images/backup.png", "Automatically backup uploaded exam papers for secure data storage."),
            ("ID-Card Analysis - Performance Insights", "assets/images/id-card.png", "Gain detailed insights into student performance with advanced analytics."),
            ("Verified and Trusted", "assets/images/cloud.png", "Ensure the integrity of exam data with robust digital signatures and encryption.")
        ]

        for idx, (title, icon, desc) in enumerate(features):
            feature_card = ctk.CTkFrame(
                self.features_grid,
                fg_color=Colors.SECONDARY,
                corner_radius=12,
                border_width=1,
                border_color=Colors.BACKGROUND
            )
            feature_card.grid(row=0, column=idx, padx=15, pady=10, sticky="nsew")

            ctk.CTkLabel(
                feature_card,
                image=ctk.CTkImage(light_image=Image.open(getPath(icon)), size=(40, 40)),
                text=""
            ).pack(pady=(15, 10))

            ctk.CTkLabel(
                feature_card,
                text=title,
                font=("Arial", 14, "bold"),
                text_color=Colors.Texts.HEADERS
            ).pack(pady=(0, 5))


            ctk.CTkLabel(
                feature_card,
                text=desc,
                font=("Arial", 12),
                text_color=Colors.Texts.HEADERS,
                wraplength=150
            ).pack(pady=(0, 15))

        self.cta_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cta_frame.grid(row=3, column=0, pady=40, sticky="nsew")

        self.start_exam_btn = LinkButton(
            self.cta_frame,
            text="🚀 Apply For Exam",
            command=lambda: self.parent.redirect("exam-portal"),
            font=("Arial", 18, "bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.HIGHLIGHT,
            height=50,
            width=250,
            corner_radius=25
        )
        self.start_exam_btn.pack(pady=20)

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=4, column=0, pady=20, sticky="sew")

        ctk.CTkLabel(
            self.footer_frame,
            text="🔒 All exams are recorded and monitored for security purposes",
            font=("Arial", 10),
            text_color=Colors.Texts.PLACEHOLDER
        ).pack(side="bottom")

        self.grid_columnconfigure(0, weight=1)
        self.features_grid.grid_columnconfigure((0, 1, 2), weight=1)