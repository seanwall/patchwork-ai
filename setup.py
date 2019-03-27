import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Patchwork TD Learning",
    options={"build_exe": {"packages":["pygame"]}},
    executables = executables

    )