import os


def createDirectories(candidateID, examID, cwd):
    candidateID = candidateID
    examID = examID
    data = cwd + '/' + 'data'

    try:
        os.mkdir(data)
    except(FileExistsError):
        pass

    try:
        os.chdir(data + '/')
        os.mkdir(candidateID)
    except(FileExistsError):
        pass
    os.chdir('../audioClassification')
    try:
        os.chdir(data + '/' + candidateID + '/')
        os.mkdir(examID)
    except(FileExistsError):
        pass

    os.chdir('..')
    print(os.getcwd())
    try:
        os.chdir(data + '/' + candidateID + '/' + examID + '/')
        os.mkdir('audio_chunks')

    except(FileExistsError):
        pass
    os.chdir('../../../audioClassification')
    print(os.getcwd())
