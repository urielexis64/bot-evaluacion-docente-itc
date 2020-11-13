import pyodbc
from datetime import datetime
import winsound

def getConnection():
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                              'Database=PruebasSoftware;'
                              'UID=sa;'
                              'PWD=sa;')
    except:
        return None
    else:
        return conn


def insert(control_num: int, fullname: str, career: str):
    try:
        connection = getConnection()
        cursor = connection.cursor()
        data = [control_num, fullname, career, datetime.now()]

        cursor.execute('INSERT INTO EvaluacionDocenteBOT VALUES (?, ?, ?, ?)', data)
        connection.commit()
    except Exception as e:
        print(e)
    else:
        duration = 100  # milliseconds
        freq = 600  # Hz
        winsound.Beep(freq, duration)
