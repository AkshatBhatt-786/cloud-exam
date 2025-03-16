from auth import FirebaseAuth
import customtkinter as ctk
from PIL import Image
import re
import sys
from tkinter import messagebox
from ui_components import *
import tkinter as tk
from utils import getPath, centerWindow

class CloudAuthView(ctk.CTkToplevel):
    def __init__(self, firebase_auth, on_login_success):
        super().__init__()
        self.firebase_auth = firebase_auth
        self.on_login_success = on_login_success
        self.title("Auth | Cloud Exam")
        try:
            if sys.platform.startswith("win"):
                self.after(200, lambda: self.iconbitmap(getPath("assets\\icons\\icon.ico")))
        except Exception:
            pass
        self.geometry(centerWindow(self, 900, 650))
        self.configure(fg_color=Colors.PRIMARY)
        self.resizable(False, False)
        self.student_data = None
        
        self.name_valid = False
        self.enrollment_valid = False
        self.college_valid = False
        self.password_strong = False
        self.passwords_match = False
        
        self.build_ui()

    def build_ui(self):
        self.container = ctk.CTkFrame(self, width=850, height=600, fg_color=Colors.SECONDARY, corner_radius=12)
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        self.container.pack_propagate(False)

        self.image_frame = ctk.CTkFrame(
            self.container, width=250, height=500, fg_color=Colors.PRIMARY, corner_radius=0
        )
        self.image_frame.pack(side="left", fill="y")
        self.image_frame.pack_propagate(False)

        ctk.CTkLabel(self.image_frame, text="Cloud Exam",
                     font=("Inter", 22, "bold"), text_color=Colors.Texts.HEADERS).pack(pady=20)

        ctk.CTkLabel(self.image_frame, text="Secure. Smart. Seamless",
                     font=("Inter", 14), text_color=Colors.Texts.FIELDS).pack()

        ctk.CTkLabel(self.image_frame, text="", image=ctk.CTkImage(light_image=Image.open(getPath("assets\\images\\cloud_logo.png")), size=(220, 220))).pack(pady=50)

        self.content_frame = ctk.CTkFrame(self.container, width=600, height=700, fg_color=Colors.SECONDARY)
        self.content_frame.pack(side="right", fill="y")
        self.content_frame.pack_propagate(False)

        self.tab_view = ctk.CTkTabview(self.content_frame, segmented_button_fg_color=Colors.SECONDARY, fg_color="transparent", text_color=Colors.Texts.HEADERS, segmented_button_selected_color="#1A237E", segmented_button_unselected_color="#7986CB", width=550, border_color=Colors.Texts.BORDER)
        self.tab_view.place(relx=0.5, rely=0.6, anchor="center")
        self.tab_view.add("Login")
        self.tab_view.add("Register")

        self.create_login_form()
        self.create_register_form()

    def create_login_form(self):
        login_frame = self.tab_view.tab("Login")
        login_frame.configure(width=550, height=600)
        login_frame.pack_propagate(False)
        
        ctk.CTkLabel(login_frame, text="Welcome Back!", font=("Inter", 16, "bold"), text_color=Colors.Texts.HEADERS).pack(pady=20)
   
        ctk.CTkLabel(login_frame, text="Enrollment Number", font=("Inter", 12, "bold"), text_color=Colors.Texts.HEADERS).pack(pady=5)
        self.login_enrollment = ctk.CTkEntry(login_frame, validate="key", placeholder_text="Enter your Enrollment No", fg_color=Colors.PRIMARY, corner_radius=8, width=280, height=34)
        self.login_enrollment.configure(validatecommand=(self.login_enrollment.register(self.validate_numeric_input), '%P'))
        self.login_enrollment.pack(pady=5)
        self.login_enrollment.bind("<KeyRelease>", self.real_time_enrollment_check)
        
        ctk.CTkLabel(login_frame, text="Password", font=("Inter", 12, "bold"), text_color=Colors.Texts.HEADERS).pack(pady=5)
        self.login_password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="●", fg_color=Colors.PRIMARY, corner_radius=8, width=280, height=34)
        self.login_password.pack(pady=5)
        
        self.login_status = ctk.CTkLabel(login_frame, text="", text_color="red")
        self.login_status.pack(pady=5)
        
        PrimaryButton(login_frame, text="Login", command=self.attempt_login).pack(pady=15)

    def create_register_form(self):
        self.register_frame = self.tab_view.tab("Register")
        self.register_frame.configure(width=550, height=600)
        self.register_frame.pack_propagate(False)

        self.reg_name = ctk.CTkEntry(self.register_frame, placeholder_text="Full Name", fg_color=Colors.PRIMARY, corner_radius=8, width=280, height=34)
        self.reg_name.pack(pady=5)
        self.reg_name.bind("<KeyRelease>", self.check_name_validation)

        self.name_validation_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        self.name_validation_frame.pack(pady=5)

        self.name_format_status = ctk.CTkLabel(self.name_validation_frame, 
                                                   text="◍ Full Name", 
                                                   text_color="gray")
        self.name_format_status.pack(anchor="w")
       
        self.reg_enrollment = ctk.CTkEntry(self.register_frame, validate="key", placeholder_text="Enrollment Number", fg_color=Colors.PRIMARY, corner_radius=8, width=280, height=34)
        self.reg_enrollment.configure(validatecommand=(self.reg_enrollment.register(self.validate_numeric_input), '%P'))
        self.reg_enrollment.pack(pady=5)
        self.reg_enrollment.bind("<KeyRelease>", self.check_enrollment_availability)

        self.enrollment_validation_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        self.enrollment_validation_frame.pack(pady=5)
        
        self.enrollment_format_status = ctk.CTkLabel(self.enrollment_validation_frame, 
                                                   text="◍ 12-digit Number", 
                                                   text_color="gray")
        self.enrollment_availability_status = ctk.CTkLabel(self.enrollment_validation_frame, 
                                                         text="◍ Enrollment Available", 
                                                         text_color="gray")
        self.enrollment_format_status.pack(anchor="w")
        self.enrollment_availability_status.pack(anchor="w")
        
        self.reg_college = ctk.CTkEntry(self.register_frame, placeholder_text="College ID", fg_color=Colors.PRIMARY, corner_radius=8, width=280, height=34)
        self.reg_college.pack(pady=5)
        self.reg_college.bind("<KeyRelease>", self.check_college_validity)

        self.reg_college_validation_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        self.reg_college_validation_frame.pack(pady=5)
        
        self.college_status = ctk.CTkLabel(self.reg_college_validation_frame, text="◍ College ID Valid", 
                                          text_color="gray")
        self.college_status.pack(anchor="w")
        
        self.reg_password = ctk.CTkEntry(self.register_frame, placeholder_text="Create Strong Password", show="●", fg_color=Colors.PRIMARY, corner_radius=8, width=280, height=34)
        self.reg_password.pack(pady=5)
        self.reg_password.bind("<KeyRelease>", self.check_password_strength)

        self.password_validation_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        self.password_validation_frame.pack(pady=5)
        
        self.password_status = ctk.CTkLabel(self.password_validation_frame, text="◍ Password Strength", 
                                           text_color="gray")
        self.password_status.pack(anchor="w")
        
        self.reg_confirm_password = ctk.CTkEntry(self.register_frame, placeholder_text="Confirm Password", show="●", fg_color=Colors.PRIMARY, corner_radius=8, width=280, height=34)
        self.reg_confirm_password.pack(pady=5)
        self.reg_confirm_password.bind("<KeyRelease>", self.check_password_match)
      
        self.match_validation_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        self.match_validation_frame.pack(pady=5)
        
        self.match_status = ctk.CTkLabel(self.match_validation_frame, text="◍ Passwords Match", 
                                        text_color="gray")
        self.match_status.pack(anchor="w")
        
        PrimaryButton(self.register_frame, text="Register", command=self.attempt_registration).pack(pady=15)

    def check_name_validation(self, event):
        name = self.reg_name.get()
        if name != "" and len(name) > 6:
            self.name_valid = True
            self.name_format_status.configure(text="✓ Valid Username", text_color="green")
        else:
            self.name_valid = False
            self.name_format_status.configure(text="✓ Enter your full name", text_color="red")

    def validate_numeric_input(self, new_value):
        return new_value.isdigit() and len(new_value) <= 12 or new_value == ""

    def real_time_enrollment_check(self, event):
        enrollment = self.login_enrollment.get()
        if len(enrollment) != 12:
            self.login_status.configure(text="Enrollment must be exactly 12 digits", 
                                      text_color="red")
        else:
            self.login_status.configure(text="✓ Valid format", text_color="green")
            
    def check_enrollment_availability(self, event):
        enrollment = self.reg_enrollment.get()
        if len(enrollment) != 12:
            self.enrollment_format_status.configure(text="⨯ Must be 12 digits", text_color="red")
            self.enrollment_availability_status.configure(text="◍ Enrollment Available",text_color="gray")
            self.enrollment_valid = False
            return
        self.enrollment_format_status.configure(text="✓ Valid format", text_color="green")
        
        if self.firebase_auth.db is not None:
            if self.firebase_auth.db.collection("students").document(enrollment).get().exists:
                self.enrollment_availability_status.configure(text="⨯ Enrollment Exists", text_color="red")
                self.enrollment_valid = False
            else:
                self.enrollment_availability_status.configure(text="✓ Enrollment Available", text_color="green")
                self.enrollment_valid = True
        

    def check_college_validity(self, event):
        college_id = self.reg_college.get()
        college_id_list = ["IT060786", "CS060786"]
        if len(college_id) >= 8:
            if college_id in college_id_list:
                self.college_status.configure(text="✓ College ID Valid", text_color="green")
                self.college_valid = True
            else:
                self.college_status.configure(text="⨯ Invalid College ID", text_color="red")
                self.college_valid = False
        else:
            self.college_status.configure(text="⨯ Invalid College ID", text_color="red")
            self.college_valid = False

    def check_password_strength(self, event):
        password = self.reg_password.get()
        if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            self.password_status.configure(text="✓ Strong Password", text_color="green")
            self.password_strong = True
        else:
            self.password_status.configure(text="⨯ Weak Password", text_color="red")
            self.password_strong = False

    def check_password_match(self, event):
        if self.reg_password.get() == self.reg_confirm_password.get():
            self.match_status.configure(text="✓ Passwords Match", text_color="green")
            self.passwords_match = True
        else:
            self.match_status.configure(text="⨯ Passwords Don't Match", text_color="red")
            self.passwords_match = False

    def attempt_login(self):
        enrollment = self.login_enrollment.get()
        password = self.login_password.get()
        
        student_data = self.firebase_auth.student_login(enrollment, password)
        if student_data:
            self.student_data = student_data
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid enrollment or password")

    def run(self):
        self.build_ui()
        self.mainloop()

    def attempt_registration(self):
        if all([self.enrollment_valid, self.college_valid, self.password_strong, self.passwords_match]):
            success = self.firebase_auth.register_student(
                enrollment=self.reg_enrollment.get(),
                name=self.reg_name.get(), 
                password=self.reg_password.get(),
                college_id=self.reg_college.get()
            )
            if success:
                messagebox.showinfo("Success", "Registration successful!")
                self.tab_view.set("Login")
            else:
                messagebox.showerror("Error", "Registration failed")
        else:
            messagebox.showwarning("Validation Error", "Please fix all validation issues before submitting")
