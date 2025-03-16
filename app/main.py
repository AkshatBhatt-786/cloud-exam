import customtkinter as ctk
from utils import centerWindow, getPath
from auth import FirebaseAuth
from auth_view import CloudAuthView
import threading


class CloudExamApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Cloud Exam v1.0.0 (Beta)")
        self.minsize(700, 600)
        self.geometry(centerWindow(self, 1150, 720, self._get_window_scaling(), (0, 130)))
        self.iconbitmap(bitmap=getPath("assets\\icons\\icon.ico"))
        self.content_frame = None
        self.user_manager = FirebaseAuth()
        self.auth_view = CloudAuthView(self.user_manager, self.on_login_success)

        self.auth_view.run()

    def on_login_success(self):
        self.auth_view.destroy()
        print(self.auth_view.student_data)
        self.mainloop()

if __name__ == "__main__":
    app = CloudExamApp()