import firebase_admin
from firebase_admin import credentials, firestore
import os
import socket
import json
from tkinter import messagebox
import hashlib

class FirebaseAuth:
    def __init__(self):
        service_account_json = os.getenv("FIREBASE_CONFIG")
        self.database_connected = False

        if service_account_json:
            try:
                cred_dict = json.load(open(service_account_json))
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.database_connected = True
            except Exception as e:
                print(f"Error initializing Firebase: {e}")
                self.database_connected = False

    def is_connected(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def student_login(self, enrollment, password):
        if not self.is_connected():
            messagebox.showerror("No Internet Connectivity", "No Internet Connection. Please check your network.")
            return

        if not self.database_connected:
            messagebox.showerror("Unable to Connect Database", "Database connection failed.")
            return

        student_ref = self.db.collection("students").document(enrollment)

        try:
            student = student_ref.get()
            if not student.exists:
                return None
            
            student_data = student.to_dict()
            stored_password = student_data.get("password")

            if stored_password == hashlib.sha256(password.encode()).hexdigest():
                return student_data 
            else:
                return None 
        except Exception as e:
            messagebox.showerror("Something went Wrong!", f"Failed to fetch student data: {e}")
            return

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_student(self, enrollment, name, password, college_id):
        if not self.is_connected():
            messagebox.showerror("Connection Error", "No Internet Connection. Please check your network.")

        if not self.database_connected:
            messagebox.showerror("Connection Error", "Database connection failed.")

        student_ref = self.db.collection("students").document(enrollment)

        try:
            if student_ref.get().exists:
                return False

            student_data = {
                "name": name,
                "password": self.hash_password(password),
                "college_id": college_id,
                "exams": {}
            }

            student_ref.set(student_data)
            return True
        except Exception as e:
            messagebox.showerror("Registeration Failed", f"Failed to register student: {e}")