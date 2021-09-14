import os


def createDirectories(candidateID, examID):
    candidateID = candidateID
    examID = examID
    data = 'data'

    try:
        os.mkdir(data)
    except(FileExistsError):
        pass

    try:
        os.chdir(data + '/')
        os.mkdir(candidateID)
    except(FileExistsError):
        pass
    os.chdir('..')
    try:
        os.chdir(data + '/' + candidateID + '/')
        os.mkdir(examID)
    except(FileExistsError):
        pass

    os.chdir('../..')
    print(os.getcwd())
    try:
        os.chdir(data + '/' + candidateID + '/' + examID + '/')
        os.mkdir('audio_chunks')

    except(FileExistsError):
        pass
    os.chdir('../../..')
    print(os.getcwd())
