import customtkinter as ctk
from utils import centerWindow, getPath
from auth import FirebaseAuth
from auth_view import CloudAuthView
from exam_portal_page import ExamPortalPage
from exam_page import ExamUI
from ui_components import *
from PIL import Image
# import logging
# import grpc

# grpc._cython.cygrpc.set_default_logger_severity(logging.CRITICAL)

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

        self.icon_frame, self.name_frame = None, None
        self.start_pos = 0
        self.end_pos = -0.2
        self.in_start_pos = True
        self.pos = self.start_pos
        self.start_pos += 0.02
        self.width = abs(self.start_pos - self.end_pos)
        self.halfway_pos = ((self.start_pos + self.end_pos) / 2) - 0.06
        self.configure(fg_color=Colors.BACKGROUND)
        self.main_content = ctk.CTkFrame(
            master=self,
            fg_color=Colors.PRIMARY,
            corner_radius=15,
            border_width=0,
            border_color=Colors.Texts.BORDER
        )
        self.main_content.place(relx=0.25, rely=0.09, relwidth=0.7, relheight=0.9)

        self.sidebar = ctk.CTkFrame(
            master=self,
            fg_color=Colors.Sidebar.BACKGROUND,
            border_color=Colors.Sidebar.BORDER,
            border_width=2,
            corner_radius=10
        )

        if self.name_frame is None:
            self._create_name_frame()

        if self.icon_frame is None:
            self._create_icon_frame()

        self.sidebar.place(relx=self.start_pos, rely=0.14, relwidth=self.width, relheight=0.8)
        self.sidebar.columnconfigure((0, 1), weight=1)
        self.sidebar.rowconfigure(0, weight=1)
        self.auth_view.run()
        # self.mainloop()

    def on_login_success(self):
        # print(self.auth_view.student_data)
        self.auth_view.destroy()
        self.mainloop()

    def _create_name_frame(self):
        self.name_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color=Colors.PRIMARY,
            corner_radius=8,
            width=140,
            scrollbar_fg_color=Colors.PRIMARY,
            scrollbar_button_color=Colors.PRIMARY,
            scrollbar_button_hover_color=Colors.PRIMARY
        )
        self.name_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.name_frame.grid_propagate(flag=False)

        header_frame = ctk.CTkFrame(
            master=self.name_frame,
            fg_color=Colors.HIGHLIGHT,
            height=40,
            corner_radius=8
        )
        header_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        header_label = ctk.CTkLabel(
            master=header_frame,
            text="Welcome Back",
            font=("Arial", 12, "bold"),
            text_color="white"
        )
        header_label.pack(pady=5)

        self.logo = ctk.CTkLabel(
            master=self.name_frame,
            text="Cloud Exam",
            image=ctk.CTkImage(light_image=Image.open(getPath("assets\\images\\cloud_logo.png")), size=(100, 100)),
            font=("Consolas", 18, "bold"),
            compound="top",
            text_color=Colors.HIGHLIGHT
        )
        self.logo.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self.home_redirect_link_btn = SidebarButton(
            master=self.name_frame,
            text="Home",
            command=lambda: self.redirect_to_home_page()
        )
        self.home_redirect_link_btn.grid(row=2, column=0, pady=10, sticky="w")


    def _create_icon_frame(self):
        self.icon_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color=Colors.SECONDARY,
            corner_radius=8,
            width=60,
            scrollbar_fg_color=Colors.SECONDARY,
            scrollbar_button_color=Colors.SECONDARY,
            scrollbar_button_hover_color=Colors.SECONDARY
        )

        self.icon_frame.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="nsew")
        self.icon_frame.pack_propagate(flag=False)
        self.icon_frame.grid_propagate(flag=False)

        self.toggle_btn = ctk.CTkButton(
            self.icon_frame,
            fg_color="transparent",
            text_color=Colors.Texts.BORDER,
            hover_color=Colors.SECONDARY,
            corner_radius=18,
            text="",
            image=ctk.CTkImage(light_image=Image.open(getPath("assets\\images\\hamburger.png")), size=(30, 30)),
            width=20,
            height=20,
            command=self.animate
        )
        self.toggle_btn.grid(row=0, column=0, pady=20, padx=5, sticky="nsew")

        self.home_btn = IconButton(
            self.icon_frame,
            image=ctk.CTkImage(light_image=Image.open(getPath("assets\\images\\home.png")), size=(30, 30)),
            command=lambda: self.redirect("home-page")
        )
        self.home_btn.grid(row=1, column=0, pady=20, padx=5, sticky="nsew")

        self.exam_portal_btn = IconButton(
            self.icon_frame,
            image=ctk.CTkImage(light_image=Image.open(getPath("assets\\images\\exam_portal.png")), size=(30, 30)),
            command=lambda: self.redirect(page_name="exam-portal")
        )
        self.exam_portal_btn.grid(row=2, column=0, pady=20, padx=5, sticky="nsew")

    def animate(self):
        if self.in_start_pos:
            self.animate_to(self.halfway_pos)
            self.main_content.place_configure(relx=0.10, rely=0.09, relwidth=0.85, relheight=0.9)
        else:
            self.animate_to(self.start_pos)
            self.main_content.place_configure(relx=0.25, rely=0.09, relwidth=0.7, relheight=0.9)

    def animate_to(self, target_pos):
        if abs(self.pos - target_pos) > 0.008:
            step = -0.008 if self.pos > target_pos else 0.008
            self.pos += step
            self.sidebar.place(relx=self.pos, rely=0.14, relwidth=self.width, relheight=0.8)
            self.sidebar.after(10, self.animate_to, target_pos)
        else:
            self.pos = target_pos
            self.sidebar.place(relx=self.pos, rely=0.14, relwidth=self.width, relheight=0.8)
            self.in_start_pos = self.pos == self.start_pos  
    
    def redirect(self, page_name, **kwargs):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        self.attributes("-topmost", False)
        self.overrideredirect(False)

        if page_name == "home-page":
            self.title("CLoud Exam v1.0.0 (beta)")
            # self.result_page = ResultsPage(self.main_content)
            # self.result_page.pack(padx=10, pady=10, anchor="center")
        
        if page_name == "exam-portal":
            self.title("Exam Portal | Cloud Exam")
            self.exam_portal_page = ExamPortalPage(self.main_content, self)
            self.exam_portal_page.pack(padx=10, pady=10, anchor="center")

        if page_name == "exam-page":
            self.sidebar.destroy()
            self.main_content.place_forget()
            subject_details = kwargs.get("subject_details")
            questions = kwargs.get("questions")
            self.attributes("-topmost", True)
            # self.overrideredirect(True)
            self.exam_portal_page = ExamUI(self, subject_details=subject_details, student_data=self.auth_view.student_data, questions=questions, parent=self)
            self.exam_portal_page.pack(padx=10, pady=10, anchor="center")

if __name__ == "__main__":
    app = CloudExamApp()