import customtkinter as ctk
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
from cryptography.exceptions import InvalidKey, InvalidTag
import os
import base64
import json
from utils import getPath

# ============================== Colors Configuration ==============================
class Colors:
    PRIMARY = "#FFFFFF"
    SECONDARY = "#F5F5F5"
    ACCENT = "#3498db"
    HIGHLIGHT = "#22D3EE"
    SUCCESS = "#4ADE80"
    WARNING = "#FACC15"
    DANGER = "#D94E63"
    BACKGROUND = "#FFFFFF"

    class Texts:
        HEADERS = "#2c3e50"
        FIELDS = "#34495e"
        PLACEHOLDER = "#95a5a6"
        BORDER = "#bdc3c7"

    class Sidebar:
        BACKGROUND = "#F2F9FA"
        BORDER = "#FFD3BA"
        HOVER = "#A8DADC"
        TEXT = "#4A4A4A"
        SECTION_BG = "#B0E5E8"
        BUTTON_BG = "#C4E4E7"

    class Buttons:
        PRIMARY = "#3498db"
        PRIMARY_HOVER = "#2980b9"
        SECONDARY = "#C4E4E7"
        SECONDARY_HOVER = "#A8DADC"
        DISABLED = "#94A3B8"
        TEXT = "#FFFFFF"

    class Inputs:
        BACKGROUND = "#F5F5F5"
        BORDER = "#bdc3c7"
        TEXT = "#34495e"
        PLACEHOLDER = "#95a5a6"

    class Cards:
        BACKGROUND = "#ecf0f1"
        BORDER = "#3498db"

    class Special:
        ERROR_TEXT = "#D94E63"
        HEADER_ACCENT = "#1565C0"
        HIGHLIGHT_TEXT = "#e67e22"
        BULLET_POINTS = "#8e44ad"
        FOOTER_TEXT = "#7f8c8d"


# ============================== Exam Interface ==============================
class ExamUI(ctk.CTkFrame):
    def __init__(self, master, subject_details, student_data, questions):
        super().__init__(master, fg_color=Colors.PRIMARY)
        self.master = master
        self.subject = subject_details
        self.student = student_data
        self.questions = questions
        self.answers = {}
        
        self.exam_start = datetime.strptime(self.subject['start_time'], "%d/%m/%Y %H:%M:%S")
        self.exam_duration = timedelta(minutes=int(self.subject['live_time_duration']))
        self.end_time = self.exam_start + self.exam_duration

        self.configure_layout()
        self.create_sidebar()
        self.check_exam_status()

    def configure_layout(self):
        self.master.geometry("1366x768")
        self.master.title(f"{self.subject['name']} - Exam Portal")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.pack(fill="both", expand=True)

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, fg_color=Colors.Sidebar.BACKGROUND)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=2)
        sidebar.grid_propagate(False)

        # Subject Details
        details_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        details_frame.pack(pady=15, padx=10, fill="x")
        
        ctk.CTkLabel(details_frame, text="Exam Details", 
                    font=("Calibri", 16, "bold"), 
                    text_color=Colors.Texts.HEADERS).pack(anchor="w")
        
        details = [
            ("Subject", self.subject['name']),
            ("Code", self.subject['subject_code']),
            ("Date", self.subject['subject_date']),
            ("Duration", f"{self.subject['live_time_duration']} mins"),
            ("Total Marks", self.subject['total_marks'])
        ]
        
        for label, value in details:
            ctk.CTkLabel(details_frame, text=f"{label}:", 
                        font=("Calibri", 12, "bold"), 
                        text_color=Colors.Sidebar.TEXT).pack(anchor="w", pady=(10, 0))
            ctk.CTkLabel(details_frame, text=value, 
                        font=("Calibri", 12), 
                        text_color=Colors.Sidebar.TEXT).pack(anchor="w")

        # Student Information
        student_frame = ctk.CTkFrame(sidebar, fg_color=Colors.Sidebar.SECTION_BG)
        student_frame.pack(pady=15, padx=10, fill="x")
        
        ctk.CTkLabel(student_frame, text="Candidate Details", 
                    font=("Calibri", 14, "bold"), 
                    text_color=Colors.Texts.HEADERS).pack(anchor="w")
        
        student_info = [
            ("Name", self.student['name']),
            ("Enrollment", self.student['enroll']),
            ("College ID", self.student['college_id'])
        ]
        
        for label, value in student_info:
            ctk.CTkLabel(student_frame, text=f"{label}: {value}", 
                        font=("Calibri", 12), 
                        text_color=Colors.Sidebar.TEXT).pack(anchor="w", pady=2)

        # Timer
        self.timer_label = ctk.CTkLabel(sidebar, text="00:00:00", 
                                      font=("Consolas", 24, "bold"),
                                      text_color=Colors.Special.HEADER_ACCENT)
        self.timer_label.pack(pady=20)

        # Instructions
        instructions_frame = ctk.CTkFrame(sidebar, fg_color=Colors.Sidebar.SECTION_BG)
        instructions_frame.pack(pady=15, padx=10, fill="x")
        
        ctk.CTkLabel(instructions_frame, text="Instructions", 
                    font=("Calibri", 14, "bold"), 
                    text_color=Colors.Texts.HEADERS).pack(anchor="w")
        
        for instr in self.subject['instructions']:
            ctk.CTkLabel(instructions_frame, text=f"‣ {instr}", 
                         font=("Calibri", 11), 
                         text_color=Colors.Special.BULLET_POINTS,
                         wraplength=220).pack(anchor="w", pady=2)
        # ... (sidebar content same as before)

        # self.timer_label = ctk.CTkLabel(sidebar, text="00:00:00", 
        #                               font=("Consolas", 24, "bold"),
        #                               text_color=Colors.Special.HEADER_ACCENT)
        # self.timer_label.pack(pady=20)

    def check_exam_status(self):
        if datetime.now() < self.exam_start:
            self.create_waiting_screen()
            self.start_waiting_timer()
        else:
            self.create_exam_interface()

    def create_waiting_screen(self):
        self.waiting_frame = ctk.CTkFrame(self, fg_color=Colors.PRIMARY)
        self.waiting_frame.grid(row=0, column=1, sticky="nsew")
        
        content_frame = ctk.CTkFrame(self.waiting_frame, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(content_frame, 
                    text="Please wait for the exam to begin.\nDo not close this window or refresh the page.",
                    font=("Calibri", 14),
                    text_color=Colors.Texts.FIELDS,
                    justify="center").pack(pady=20)
        
        ctk.CTkLabel(content_frame, text="🕒 Exam Will Start In", 
                    font=("Calibri", 24, "bold"), 
                    text_color=Colors.Special.HEADER_ACCENT).pack(pady=10)
        
        self.waiting_timer = ctk.CTkLabel(content_frame, text="00:00:00", 
                                        font=("Consolas", 32, "bold"),
                                        text_color=Colors.Texts.HEADERS)
        self.waiting_timer.pack(pady=10)

    def start_waiting_timer(self):
        def update():
            now = datetime.now()
            if now >= self.exam_start:
                self.waiting_frame.destroy()
                self.create_exam_interface()
                return
            
            remaining = self.exam_start - now
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.waiting_timer.configure(
                text=f" {hours:02d}:{minutes:02d}:{seconds:02d}",
                text_color=Colors.Special.HEADER_ACCENT
            )
            self.timer_label.configure(
                text=f"Starts in: {hours:02d}:{minutes:02d}:{seconds:02d}",
                text_color=Colors.Special.HIGHLIGHT_TEXT
            )
            self.after(1000, update)
        
        update()

    def create_exam_interface(self):
        now = datetime.now()
        if now > self.end_time:
            self.submit_exam()
            return
        
        self.end_time = min(self.end_time, now + self.exam_duration)
        
        self.main_frame = ctk.CTkFrame(self, fg_color=Colors.PRIMARY)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Questions Scrollable Area
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color=Colors.PRIMARY)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        scroll_frame.grid_columnconfigure(0, weight=1)

        for idx, question in enumerate(self.questions, 1):
            q_frame = ctk.CTkFrame(scroll_frame, 
                                 fg_color=Colors.Cards.BACKGROUND,
                                 border_color=Colors.Cards.BORDER,
                                 border_width=1,
                                 corner_radius=8)
            q_frame.pack(fill="x", pady=5, padx=5)
            
            header_frame = ctk.CTkFrame(q_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(header_frame, text=f"Question {idx}", 
                        font=("Calibri", 14, "bold"), 
                        text_color=Colors.Texts.HEADERS).pack(side="left")
            
            ctk.CTkLabel(header_frame, text=f"[{question['marks']} Marks]", 
                        font=("Calibri", 12), 
                        text_color=Colors.Special.FOOTER_TEXT).pack(side="left", padx=10)

            ctk.CTkLabel(q_frame, text=question['text'], 
                        font=("Calibri", 12), 
                        text_color=Colors.Texts.FIELDS,
                        wraplength=800).pack(anchor="w", padx=10, pady=(0, 10))

            self.create_answer_input(q_frame, question, idx)

        nav_frame = ctk.CTkFrame(self.main_frame, fg_color=Colors.PRIMARY)
        nav_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(nav_frame, text="Submit Exam", 
                      fg_color=Colors.SUCCESS,
                      hover_color="#16a34a",
                      command=self.submit_exam).pack(side="right", padx=5)

        self.start_timer()

    def start_timer(self):
        def update():
            remaining = self.end_time - datetime.now()
            if remaining.total_seconds() <= 0:
                self.timer_label.configure(text="00:00:00", text_color=Colors.DANGER)
                self.submit_exam()
                return
            
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.configure(
                text=f"{hours:02d}:{minutes:02d}:{seconds:02d}",
                text_color=Colors.Special.HEADER_ACCENT
            )
            self.after(1000, update)
        
        update()

    def submit_exam(self):
        print("Exam submitted! Answers:", self.answers)
        self.master.destroy()

    def create_answer_input(self, parent, question, q_num):
        input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        if question['type'] == 'mcq':
            self.answers[q_num] = ctk.StringVar()
            for opt in question['options']:
                ctk.CTkRadioButton(input_frame, text=opt,
                                  variable=self.answers[q_num],
                                  value=opt,
                                  text_color=Colors.Texts.FIELDS).pack(anchor="w", pady=2)
        
        elif question['type'] == 't/f':
            self.answers[q_num] = ctk.StringVar()
            ctk.CTkRadioButton(input_frame, text="True",
                             variable=self.answers[q_num],
                             value="True").pack(side="left", padx=20)
            ctk.CTkRadioButton(input_frame, text="False",
                             variable=self.answers[q_num],
                             value="False").pack(side="left", padx=20)
        
        elif question['type'] == 'one_word':
            self.answers[q_num] = ctk.StringVar()
            entry = ctk.CTkEntry(input_frame, 
                               textvariable=self.answers[q_num],
                               placeholder_text="Type your answer here...",
                               fg_color=Colors.Inputs.BACKGROUND,
                               border_color=Colors.Inputs.BORDER,
                               width=400)
            entry.pack(anchor="w", pady=2)

# ============================== Helper Methods ==============================
def _derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def _decrypt_data(encrypted_data, password):
    try:
        salt = base64.b64decode(encrypted_data['salt'])
        iv = base64.b64decode(encrypted_data['iv'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        
        key = _derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        pad_len = plaintext[-1]
        return plaintext[:-pad_len].decode()
    except (InvalidKey, ValueError, InvalidTag):
        return None

# ============================== Sample Execution ==============================
if __name__ == "__main__":
    sample_subject = {
        'name': 'Advanced Python',
        'subject_code': 'CS501',
        'start_time': (datetime.now() + timedelta(seconds=100)).strftime("%d/%m/%Y %H:%M:%S"),
        'live_time_duration': 120,
        "subject_date": "17-04-2025",
        'total_marks': 100,
        'instructions': [
            'No internet access allowed',
            'All questions are compulsory'
        ]
    }

    sample_student = {
        'name': 'John Doe',
        'enroll': 'EN2020',
        'college_id': 'CLG123'
    }

    sample_questions = [
        {
            'text': 'Explain Python generators',
            'marks': 10,
            'type': 'one_word'
        },
        {
            'text': 'Is Python interpreted?',
            'marks': 5,
            'type': 't/f'
        }
    ]

    root = ctk.CTk()
    ExamUI(root, sample_subject, sample_student, sample_questions)
    root.mainloop()