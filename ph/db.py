import sqlite3
DIR_LOCATION = "/home/${USER}/.local/share/"

conn = sqlite3.connect(DIR_LOCATION)
curs = conn.cursor()
