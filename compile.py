import os

PATH = "C:\\Users\\Francis\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts"
SRCS = "srcs\\"
NAME = "pbrain-bordeaux-francois.caicedo.exe"
PY_FILE = SRCS + "bot.py " + SRCS + "pisqpipe.py --name " + NAME + " --onefile"

print(PY_FILE)
os.system("pyinstaller -p " + PATH + " " + PY_FILE)
os.system("copy dist\\" + NAME + " .")
print("Press ENTER to exit")
input()
