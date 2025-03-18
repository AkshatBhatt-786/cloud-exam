import customtkinter as ctk
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from ui_components import Colors
from tkinter import messagebox
from datetime import datetime, timedelta
from cryptography.exceptions import InvalidKey, InvalidTag
from PIL import Image
import os
import base64
import json
import random
from utils import getPath, centerWindow

class ExamUI(ctk.CTkFrame):
    def __init__(self, master, subject_details, student_data, questions, parent):
        super().__init__(master, fg_color=Colors.PRIMARY)
        self.master = master
        self.parent = parent
        self.subject = subject_details
        self.student = student_data
        random.shuffle(questions)
        self.questions = questions
        self.student_key = None
        self.answers = {}

        self.exam_start = datetime.strptime(str(self.subject['exam_start_time']), "%Y-%m-%d %H:%M:%S")
        self.exam_duration = timedelta(minutes=int(self.subject['time_duration']))
        self.end_time = self.exam_start + self.exam_duration

        self.configure_layout()
        self.create_sidebar()
        self.check_exam_status()

    def configure_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.pack(fill="both", expand=True)
    
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=280, fg_color=Colors.Sidebar.BACKGROUND)
        sidebar.pack_propagate(False)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=2)
        sidebar.grid_propagate(False)

        details_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        details_frame.pack(pady=15, padx=10, fill="x")
        
        ctk.CTkLabel(details_frame, text="Exam Details", 
                    font=("Calibri", 16, "bold"), 
                    text_color=Colors.Texts.HEADERS).pack(anchor="w")
        
        details = [
            ("Subject", self.subject['subject_name']),
            ("Code", self.subject['subject_code']),
            ("Date", self.subject['subject_date']),
            ("Duration", f"{self.subject['time_duration']} mins"),
            ("Total Marks", self.subject["total_marks"])
        ]
        
        for label, value in details:
            ctk.CTkLabel(details_frame, text=f"{label}: {value}", 
                        font=("Calibri", 12), 
                        text_color=Colors.Sidebar.TEXT).pack(anchor="w", pady=(10, 0))

        student_frame = ctk.CTkFrame(sidebar, fg_color=Colors.Sidebar.SECTION_BG)
        student_frame.pack(pady=15, padx=10, fill="x")
        
        ctk.CTkLabel(student_frame, text="Candidate Details", 
                    font=("Calibri", 14, "bold"), 
                    text_color=Colors.Texts.HEADERS).pack(anchor="w", padx=10, pady=10)
        
        student_info = [
            ("Name", self.student['name']),
            ("Enrollment", self.student['enrollment_no']),
            ("College ID", self.student['college_id'])
        ]
        
        for label, value in student_info:
            ctk.CTkLabel(student_frame, text=f"{label}: {value}", 
                        font=("Calibri", 12, "bold"), 
                        text_color=Colors.Sidebar.TEXT).pack(anchor="w", padx=2, pady=2)

        self.timer_label = ctk.CTkLabel(sidebar, text="00:00:00", 
                                      font=("Consolas", 26, "bold"),
                                      text_color=Colors.Special.HEADER_ACCENT)
        self.timer_label.pack(pady=20)

        instructions_frame = ctk.CTkFrame(sidebar, fg_color=Colors.Sidebar.SECTION_BG)
        instructions_frame.pack(pady=15, padx=10, fill="x")
        
        ctk.CTkLabel(instructions_frame, text="Instructions", 
                    font=("Calibri", 14, "bold"), 
                    text_color=Colors.Texts.HEADERS).pack(anchor="w", padx=10, pady=10)
        
        for instr in self.subject['instructions']:
            ctk.CTkLabel(instructions_frame, text=f"{instr}", 
                         font=("Calibri", 11), 
                         text_color=Colors.Special.BULLET_POINTS,
                         wraplength=220).pack(anchor="w", pady=2, padx=2)
    
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
        
        ctk.CTkLabel(content_frame, text="Exam Will Start In",
                    font=("Calibri", 24, "bold"), 
                    text_color=Colors.Special.HEADER_ACCENT).pack(pady=10)
        
        self.waiting_timer = ctk.CTkLabel(
            content_frame, 
            image=ctk.CTkImage(light_image=Image.open(getPath("assets\\images\\deadline.png")), size=(50, 50)),
            compound="left",
            text=" 00:00:00", 
            font=("Consolas", 32, "bold"),
            text_color=Colors.Texts.HEADERS)
        self.waiting_timer.pack(padx=10, pady=10)

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


    def submit_exam(self, timeout=False):
        if timeout:
            submitted_answers = {q_num: var.get() for q_num, var in self.answers.items()}
            self.student_key = submitted_answers
            self.master.destroy()
            return

        confirm = messagebox.askyesno(
        title="Submit Exam?",
        message="Are you sure you want to submit the exam? You cannot change your answers after submission.",
        )
    
        if not confirm:
            return  
        
        submitted_answers = {q_num: var.get() for q_num, var in self.answers.items()}
        self.student_key = submitted_answers
        self.answer_key = self.subject["answer_key"]
        self.marks_per_question = self.get_marks_per_question(self.questions)

        results = self.evaluate_exam(user_responses=self.student_key, correct_answers=self.answer_key, marks_per_question=self.marks_per_question)
        print(results)
        

        self.master.destroy()


    def create_answer_input(self, parent, question, q_num):
        input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        q_id = question['id']
        if question['type'] == 'MCQ':
            self.answers[q_id] = ctk.StringVar()
            for opt in question['options']:
                ctk.CTkRadioButton(input_frame, text=opt,
                                  variable=self.answers[q_id],
                                  value=opt,
                                  text_color=Colors.Texts.FIELDS).pack(anchor="w", pady=2) 
        
        elif question['type'] == 'True/False':
            self.answers[q_num] = ctk.StringVar()
            ctk.CTkRadioButton(input_frame, text="True", text_color=Colors.Texts.HEADERS,
                             variable=self.answers[q_num],
                             value="True").pack(side="left", padx=20)
            ctk.CTkRadioButton(input_frame, text="False", text_color=Colors.Texts.HEADERS,
                             variable=self.answers[q_num],
                             value="False").pack(side="left", padx=20)
        
        elif question['type'] == 'One Word':
            self.answers[q_num] = ctk.StringVar()
            entry = ctk.CTkEntry(input_frame, 
                               textvariable=self.answers[q_num],
                               placeholder_text="Type your answer here...",
                               fg_color=Colors.Inputs.BACKGROUND,
                               border_color=Colors.Inputs.BORDER,
                               text_color=Colors.Texts.HEADERS,
                               width=400)
            entry.pack(anchor="w", pady=2)

    def create_exam_interface(self):
        if datetime.now() > self.end_time:
            self.submit_exam()
            return

        self.main_frame = ctk.CTkFrame(self, fg_color=Colors.PRIMARY)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color=Colors.PRIMARY)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for display_idx, question in enumerate(self.questions, 1):
            self.create_question_widget(display_idx, question, scroll_frame)

        nav_frame = ctk.CTkFrame(self.main_frame, fg_color=Colors.PRIMARY)
        nav_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(nav_frame, text="Submit Exam", 
                      fg_color=Colors.SUCCESS,
                      hover_color="#16a34a",
                      command=self.submit_exam).pack(side="right", padx=5)

        self.start_timer()

    def load_questions(self):
        max_questions = 10 
        end_index = min(self.current_question_index + max_questions, len(self.questions))

        for idx in range(self.current_question_index, end_index):
            question = self.questions[idx]
            self.create_question_widget(idx + 1, question)

        self.current_question_index = end_index

    def create_question_widget(self, display_idx, question, parent_frame):
        q_frame = ctk.CTkFrame(parent_frame, 
                             fg_color=Colors.Cards.BACKGROUND,
                             border_color=Colors.Cards.BORDER,
                             border_width=1,
                             corner_radius=8)
        q_frame.pack(fill="x", pady=5, padx=5)

        header_frame = ctk.CTkFrame(q_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(header_frame, text=f"Question {display_idx}", 
                    font=("Calibri", 15, "bold"), 
                    text_color=Colors.Texts.HEADERS).pack(side="left")

        ctk.CTkLabel(header_frame, text=f"[{question['marks']} Marks]", 
                    font=("Calibri", 12), 
                    text_color=Colors.Special.FOOTER_TEXT).pack(side="left", padx=10)

        ctk.CTkLabel(q_frame, text=question['text'], 
                    font=("Calibri", 14), 
                    text_color=Colors.Texts.FIELDS,
                    wraplength=800, justify="left").pack(anchor="w", padx=10, pady=(0, 10))

        self.create_answer_input(q_frame, question, display_idx)


    def evaluate_exam(user_responses, correct_answers, marks_per_question):
        result = {
            "total_score": 0, 
            "correct_count": 0,
            "wrong_count": 0,
            "not_attempted": 0,
            "not_attempted_ids": [],
            "wrong_answers_ids": [],
            "correct_answers_ids": [],
            "marks_correct": 0,
            "marks_wrong": 0,
            "marks_not_attempted": 0
        }

        for question_id, correct_answer in correct_answers.items():
            user_answer = user_responses.get(question_id, "").strip()
            question_marks = int(marks_per_question.get(question_id, 1)) 

            if not user_answer:
                result["not_attempted"] += 1
                result["not_attempted_ids"].append(question_id)
                result["marks_not_attempted"] += question_marks 
            elif user_answer == correct_answer:
                result["correct_count"] += 1
                result["correct_answers_ids"].append(question_id)
                result["total_score"] += question_marks
                result["marks_correct"] += question_marks 
            else:
                result["wrong_count"] += 1
                result["wrong_answers_ids"].append(question_id)
                result["marks_wrong"] += question_marks 

        return result
    
    @staticmethod
    def get_marks_per_question(question_list):
        question_marks_details = {}

        for question_id, details in question_list.items():
                question_marks_details[question_id] = details.get("marks", 1)

        return question_marks_details
