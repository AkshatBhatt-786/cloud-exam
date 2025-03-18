import customtkinter as ctk

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


class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, text, width=200, height=50, **kwargs):
        super().__init__(
            master,
            text=text,
            width=width,
            height=height,
            fg_color=Colors.Buttons.PRIMARY,
            hover_color=Colors.Buttons.PRIMARY_HOVER,
            border_color=Colors.Buttons.PRIMARY, # 303F9F
            corner_radius=12,
            text_color="white",
            border_width=2,
            cursor="hand2",
            **kwargs
        )

class ErrorButton(ctk.CTkButton):
    def __init__(self, master, text, width=200, height=50, **kwargs):
        super().__init__(master, text=text, width=width, height=height,
                         fg_color=Colors.DANGER, border_color="#E74C3C", corner_radius=8, text_color="white", 
                         border_width=2, hover_color="#FFC080", cursor="hand2", **kwargs)


class IconButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=20, height=20,
            cursor="hand2", fg_color="transparent",
            text_color=Colors.Texts.BORDER,
            hover_color=Colors.SECONDARY,
            corner_radius=18,
            text="", **kwargs)
        
class SidebarButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, font=("Calibri", 16, "bold"),
            hover_color=Colors.PRIMARY,
            fg_color=Colors.PRIMARY,
            width=20, corner_radius=12, height=38,
            text_color=Colors.Texts.BORDER,
            cursor="hand2", **kwargs)

class LinkButton(ctk.CTkButton):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#1E293B",
            hover_color="#1E293B",
            width=35, height=35,
            text_color="#FFFFFF",
            cursor="hand2",
            font=("Poppins", 16)
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        self.configure(text_color="#A2DFF7")
    
    def on_leave(self, event):
        self.configure(text_color="#FFFFFF")

class CustomLabel(ctk.CTkLabel):
    def __init__(self, master=None, default_color=None, hover_color=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_color = default_color
        self.hover_color = hover_color
        self.configure(text_color=default_color)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        if self.hover_color:
            self.configure(text_color=self.hover_color)

    def on_leave(self, event=None):
        self.configure(text_color=self.default_color)

class SearchButton(ctk.CTkButton):
    def __init__(self, master, text, width=130, height=50, **kwargs):
        super().__init__(
            master,
            text=text,
            width=width,
            height=height,
            fg_color="#FF9800",
            border_color="#FF9800",
            corner_radius=12,
            text_color="white",
            border_width=2,
            hover_color="#F57C00",
            cursor="hand2",
            **kwargs
        )
