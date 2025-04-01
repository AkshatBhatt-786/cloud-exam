from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from dropbox.exceptions import ApiError, AuthError, BadInputError, InternalServerError
from datetime import datetime
from ui_components import *
from utils import getPath
import dropbox
import customtkinter as ctk
import os
import base64
import json

DBX_PATH = os.getenv("DBX_BACKEND")

class DropboxBackend:

    def __init__(self, access_token: str, app_key: str, app_secret: str, root_path: str):
        self.dbx = dropbox.Dropbox(access_token, app_key=app_key, app_secret=app_secret)
        self.root_path = root_path

    @staticmethod
    def handle_error(e):
        if isinstance(e, AuthError):
            print("Authentication error. Please check your access token.")
        elif isinstance(e, ApiError):
            print(f"API error: {e}")
        elif isinstance(e, BadInputError):
            print("Bad input error. Please verify your inputs.")
        elif isinstance(e, InternalServerError):
            print("Internal server error. Please try again later.")
        else:
            print(f"An unexpected error occurred: {e}")

    def lists_files(self, folder_path):
        dropbox_files = []
        try:
            files = self.dbx.files_list_folder(folder_path)
            for entry in files.entries:
                print(f"File: {entry.name}")
                dropbox_files.append(entry.name)
            return dropbox_files
        except Exception as e:
            print(f"Failed to find folder path: {folder_path}.")
            print(e)
            return None

    def download_file(self, dropbox_path: str, local_path: str):
        try:
            metadata, res = self.dbx.files_download(dropbox_path)
            with open(local_path, "wb") as f:
                f.write(res.content)
            
            return True
        except ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                return False
            return False
        except PermissionError:
            return False
        except Exception as e:
            return False


class ExamPortalPage(ctk.CTkFrame):
    def __init__(self, master, parent=None):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.master = master
        self.parent = parent
        self.maximized = False

        self.procedure_frame = ctk.CTkFrame(self.master, fg_color=Colors.SECONDARY, border_color=Colors.PRIMARY)
        self.procedure_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.procedure_label = ctk.CTkLabel(
            self.procedure_frame, text="Maximize the application screen to proceed further",
            font=("Consolas", 16, "bold"),
            text_color=Colors.Texts.HEADERS
        )
        self.procedure_label.pack(padx=10, pady=10, anchor="center")

        self.check_responsiveness()

    def build(self):
        ctk.CTkLabel(self.master, text="Welcome to the Cloud Exam Portal", font=("Calibri", 18, "bold"), text_color=Colors.HIGHLIGHT).place(relx=0.5, rely=0.07, anchor="center")
        ctk.CTkLabel(self.master, text="Your organization has assigned you an exam to complete through this platform. Use the Exam ID and Access code provided to log in and begin your assessment.", font=("Calibri", 14), justify="center", text_color=Colors.Texts.HEADERS, wraplength=700).place(relx=0.5, rely=0.15, anchor="center")
        frame = ctk.CTkFrame(self.master, fg_color=Colors.Cards.BACKGROUND, border_color=Colors.Cards.BORDER, border_width=2, corner_radius=10, width=600, height=400)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)

        ctk.CTkLabel(frame, text="EXAM PORTAL", font=("Calibri", 18, "bold"), text_color=Colors.Texts.HEADERS).pack(padx=10, pady=10, anchor="center")

        self.exam_id_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.exam_id_frame.pack(pady=10, anchor="center", fill="x", padx=25)
        self.exam_id_label = ctk.CTkLabel(self.exam_id_frame, text_color=Colors.Texts.FIELDS, text="EXAM ID       ", font=("Calibri", 16, "bold"))
        self.exam_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.exam_id_entry = ctk.CTkEntry(self.exam_id_frame, text_color=Colors.Inputs.TEXT, placeholder_text_color=Colors.Inputs.PLACEHOLDER, border_color=Colors.Inputs.BORDER, placeholder_text="Enter Exam-ID", fg_color=Colors.Inputs.BACKGROUND, height=42, width=280)
        self.exam_id_entry.grid(row=0, column=1, pady=5, sticky="w", padx=28)

        self.access_code_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.access_code_frame.pack(pady=10, anchor="center", fill="x", padx=25)
        self.password_label = ctk.CTkLabel(self.access_code_frame, text_color=Colors.Texts.HEADERS, text="ACCESS CODE", font=("Calibri", 16, "bold"))
        self.password_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.access_code_entry = ctk.CTkEntry(self.access_code_frame, text_color=Colors.Inputs.TEXT, placeholder_text_color=Colors.Inputs.PLACEHOLDER, border_color=Colors.Inputs.BORDER, placeholder_text="Enter Access Code", fg_color=Colors.Inputs.BACKGROUND, height=42, width=280, show="●")
        self.access_code_entry.grid(row=0, column=1, padx=19.5, pady=5, sticky="w")

        self.access_exam_btn = PrimaryButton(frame, text="Apply For Exam", width=180, height=42,
                                             command=lambda: self.authenticate_paper())
        self.access_exam_btn.pack(pady=30, padx=30, anchor="center")

        self.validation_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.validation_frame.pack(pady=5)
        
        self.validation_status = ctk.CTkLabel(self.validation_frame, text="◍ Apply for Exam", text_color="gray")
        self.validation_status.pack(anchor="center")
    
    def clear_input_fields(self):
        self.exam_id_entry.delete(0, "end")
        self.access_code_entry.delete(0, "end")

    def authenticate_paper(self):
        self.validation_status.configure(text="Connecting...", text_color=Colors.Texts.HEADERS)
        
        with open(DBX_PATH, "r") as f:
            data = json.load(f)

        access_token = data["access_token"]
        app_key = data["app_key"]
        app_secret = data["app_secret"]


        dbx_backend = DropboxBackend(access_token, app_key, app_secret, getPath("database\\temp"))
        file_exists = dbx_backend.download_file(dropbox_path=f"/uploads/{self.exam_id_entry.get().upper()}.enc", local_path=getPath(f"database\\temp\\{self.exam_id_entry.get().upper()}.enc"))
        if not file_exists:
            self.validation_status.configure(text="Exam ID or Access Code is incorrect both are case-sensitive", text_color=Colors.Special.ERROR_TEXT)
            return

        filepath = getPath(f"database\\temp\\{self.exam_id_entry.get().upper()}") + ".enc"
        access_code = self.access_code_entry.get()

        if not os.path.exists(filepath):
            self.validation_status.configure(text="Exam ID or Access Code is incorrect both are case-sensitive", text_color=Colors.Special.ERROR_TEXT)
            self.clear_input_fields()
            return

        self.validation_status.configure(text="Authorizing...", text_color=Colors.Special.HIGHLIGHT_TEXT)
        with open(filepath, 'r') as f:
            encrypted_data = json.load(f)

        try:
            decrypted_data = self._decrypt_data(encrypted_data, access_code)
            if not decrypted_data:
                self.validation_status.configure(text="Exam ID or Access Code is incorrect both are case-sensitive", text_color=Colors.Special.ERROR_TEXT)
                self.clear_input_fields()
                return

            data = json.loads(decrypted_data)

            exam_date = data["auth_data"]["registration_date"]
            registration_time = data["auth_data"]["registration_time"] + ":00"
            registration_close_time = data["auth_data"]["registration_end_time"] + ":00"

            exam_datetime = datetime.strptime(f"{exam_date} {registration_time}", "%d-%m-%Y %H:%M:%S")
            close_datetime = datetime.strptime(f"{exam_date} {registration_close_time}", "%d-%m-%Y %H:%M:%S")
            current_time = datetime.now()

            sub_details = data["subject_details"]
            sub_details["exam_start_time"] = close_datetime
            sub_details["answer_key"] = data["answer-key"]
            sub_details["question_mapping"] = data["question-mapping"]
            questions_data = data["questions"]

            if current_time < exam_datetime:
                self.validation_status.configure(
                    text=f"Registration is open, but you must wait until the exam registration starts.\nTry again on {registration_time}.", 
                    text_color=Colors.Special.HIGHLIGHT_TEXT
                )
                return 

            elif exam_datetime <= current_time <= close_datetime:
                self.validation_status.configure(
                    text="You are registered! Redirecting to exam (questions hidden until start time).", 
                    text_color="green"
                )
                sub_details["exam-id"] = self.exam_id_entry.get().upper()
                sub_details["access-code"] = self.access_code_entry.get().upper()
                self.after(3000, lambda: self.parent.redirect("exam-page", subject_details=sub_details, questions=questions_data))

            else:
                self.validation_status.configure(text="Registration is closed.", text_color=Colors.Special.ERROR_TEXT)

        except Exception as e:
            self.validation_status.configure(text="Error during authentication.", text_color=Colors.Special.ERROR_TEXT)
            print("Error:", e)


    def check_responsiveness(self):
        self.update_idletasks()

        width = self.parent.winfo_width()
        height = self.parent.winfo_height()

        if width >= self.winfo_screenwidth() - 5 and height >= self.winfo_screenheight() - 5:
            if not self.maximized:
                self.maximized = True
                self.procedure_label.destroy()
                self.parent.attributes("-topmost", True)
                self.parent.overrideredirect(True) 
                self.build()
        else:
            if self.maximized:
                self.maximized = False

        # Schedule next check
        self.after(1000, self.check_responsiveness)

    def _derive_key(self, password, salt):
        # ! Credits ! Tech with tim & Neuraline YT
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def _encrypt_data(self, data, password):
        salt = os.urandom(16)
        key = self._derive_key(password, salt)
        iv = os.urandom(16)
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)
        ciphertext = encryptor.update(padded_data.encode()) + encryptor.finalize()
        
        return {
            'salt': base64.b64encode(salt).decode(),
            'iv': base64.b64encode(iv).decode(),
            'ciphertext': base64.b64encode(ciphertext).decode()
        }

    def _decrypt_data(self, encrypted_data, password):
        # ! Credits ! Tech with tim & Neuraline YT
        try:
            salt = base64.b64decode(encrypted_data['salt'])
            iv = base64.b64decode(encrypted_data['iv'])
            ciphertext = base64.b64decode(encrypted_data['ciphertext'])
            
            key = self._derive_key(password, salt)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            pad_len = plaintext[-1]
            return plaintext[:-pad_len].decode()
        except (InvalidKey, ValueError, InvalidTag):
            return None