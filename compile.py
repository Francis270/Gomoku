import os

SRCS = "srcs/"
PY_FILE = SRCS + "bot.py " + SRCS + "pisqpipe.py --name pbrain-bordeaux-francois.caicedo.exe --onefile"

print(PY_FILE)
os.system("pyinstaller " + PY_FILE)
