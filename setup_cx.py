import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "requests_ntlm",
        # add other packages if needed
    ],
}

setup(
    name="Bloodbank App",
    version="1.0.0",
    description="A bloodbank application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)],
)
