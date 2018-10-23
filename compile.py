from cx_Freeze import setup, Executable

base = None

executables = [Executable("pbrain-Gomoku francois.caicedo@epitech.eu.py", base=base)]

packages = ["idna", "sys"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "<Gomoku francois.caicedo@epitech.eu>",
    options = options,
    version = "<1.0>",
    description = '<Gomoku best bot>',
    executables = executables
)
