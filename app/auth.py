import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import hashlib

class FirebaseAuth:
    def __init__(self):
        service_account_json = os.getenv("FIREBASE_CONFIG") 
        print("FIREBASE_CONFIG:", service_account_json)

        self.database_connected = False
        self.db = None

        if service_account_json:
            with open(service_account_json, "r") as f:
                cred_dict = json.load(f)
                
            cred = credentials.Certificate(cred_dict)

            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.database_connected = True
            else:
                self.database_connected = False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_student(self, enrollment, name, password, college_id):
        student_ref = self.db.collection("students").document(enrollment)
        
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

    def student_login(self, enrollment, password):
        if self.database_connected:
            student_ref = self.db.collection("students").document(str(enrollment))
            student = student_ref.get()

            if student.exists:
                data = student.to_dict()
                if data["password"] == self.hash_password(password):
                    return data
                else:
                    return None
            else:
                return None