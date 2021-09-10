import sqlite3


# Connect into db

def connectdb():
    conn = sqlite3.connect('saak.db')
    return conn


#################################### For Audio Classification Part ###################################################

def createAudioRecords():
    cursor = connectdb().cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audioRecords (
        candidateID text PRIMARY KEY NOT NULL,
        examID text NOT NULL,
        chunkDirectory text NOT NULL,
        chunkName TEXT NOT NULL,
        keywords TEXT NOT NULL,
    )
   """)
    print("Audio Records Table Created Successfully")
    # connectdb().close()


def createMicViolationRecords():
    cursor = connectdb().cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS micRecords (
        candidateID text PRIMARY KEY NOT NULL,
        examID text NOT NULL,
        description text NOT NULL,
        date text NOT NULL,
        
    )
   """)
    print("Mic Records Table Created Successfully")
    # connectdb().close()


def insertAudioViolationRecord(record):
    cursor = connectdb().cursor()
    cursor.execute("INSERT INTO audioRecords VALUES (?,?,?,?,?)", record)
    print("Successfully inserted a audio violation record")


def insertMicViolationRecord(record):
    cursor = connectdb().cursor()
    cursor.execute("INSERT INTO micRecords VALUES (?,?,?,?)", record)
    print("Successfully inserted a mic violation record")


def selectAudioViolationRecords(candidateID, examID):
    cursor = connectdb().cursor()
    cursor.execute("SELECT * FROM candidate WHERE candidateID = ? and examID = ?", candidateID, examID)
    audioRecords = cursor.fetchall
    return audioRecords


def selectMicViolationRecords(candidateID, examID):
    cursor = connectdb().cursor()
    cursor.execute("SELECT * FROM micRecords WHERE candidateID = ? and examID = ?", candidateID, examID)
    micRecords = cursor.fetchall
    return micRecords
