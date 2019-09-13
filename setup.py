from cx_Freeze import setup, Executable

setup(
    name="Link-Finder",
    version="0.0.1",
    options={"build_exe": {"include_files": ["drivers/"], "include_msvcr": True}},
    executables=[Executable("find_link.py")],
)
