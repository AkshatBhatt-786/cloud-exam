import sys
from cx_Freeze import setup, Executable

include_files = [
    ("assets", "assets"),
    ("database", "database"),
    ("database/temp", "database/temp"), 
]

build_exe_options = {
    "packages": ["os", "dropbox", "firebase_admin"], 
    "include_files": include_files,
    "include_msvcr": True
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="CloudExam",
    version="1.0",
    description="Dropbox Integrated Exam Software",
    options={"build_exe": build_exe_options},
    executables=[Executable(
        "main.py", 
        base=base, 
        icon=r"D:\github_projects\cloud-exam\cloud-exam\app\assets\icons\icon.ico"
        )
    ]
)
