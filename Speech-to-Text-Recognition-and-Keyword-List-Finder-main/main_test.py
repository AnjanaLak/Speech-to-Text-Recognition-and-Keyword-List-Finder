import os

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub import AudioSegment as am
import directoryManager


#### Need to retrieve info through Flask API
def getSessionInfo():
    candidateID = 'IT17019750'
    examID = 'IT4140'
    return candidateID, examID


def silence_based_conversion(path):
    # calling the getSessionInfo function
    candidateID, examID = getSessionInfo()
    ## Importing the directory manager
    dir = directoryManager.createDirectories(candidateID, examID)
    print(dir)
    with open("api-key.json") as f:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api-key.json'
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    myaudio = AudioSegment.from_file(path, "wav")
    chunk_length_ms = 14000  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)

    # open a file where we will concatenate and store the recognized text

    fh = open("recognized.txt", "w+")

    # move into the directory to store the audio files.
    os.chdir('data/' + candidateID + '/' + examID + '/' + 'audio_chunks')

    # Export all of the individual chunks as wav files

    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

    i = 0
    for chunk in chunks:
        print("in chunks")
        chunk_silent = AudioSegment.silent(duration=10)
        audio_chunk = chunk_silent + chunk + chunk_silent
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate='192k', format="wav")
        filename = 'chunk' + str(i) + '.wav'
        print("Processing chunk " + str(i))
        file = filename
        r = sr.Recognizer()
        with sr.AudioFile(file) as source:
            # r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)
        try:
            rec = r.recognize_google_cloud(audio_listened, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            # rec = r.recognize_google(audio_listened)
            print(type(rec))
            # if rec:
            #     if rec.__contains__(keywordList):
            #         rec = rec + "=> chunk file name : " + str(chunk)
            fh.write(rec + ". ")
            # need to include the chunk info, matched keywords if
            # found the string is not empty and contains at least a single keyword
            # should only write info to the file only if a keyword exists
            # then read the final file and capture the related keyword and chunk
            # and then include the chunk info to the database
            # To the report include chunk info, and upload the chunks to the
            # drive

        except:
            rec = r.recognize_google_cloud(audio_listened, show_all=True)
            print(rec, type(rec))

        i += 1


if __name__ == '__main__':
    print('Starting speech recognition process')

    # path = input()
    path = 'output.wav'  ## need a .wav file with 16kHz sample rate

    silence_based_conversion(path)

# sound = am.from_file(filepath, format='wav', frame_rate=22050)
# sound = sound.set_frame_rate(16000)
# sound.export(filepath, format='wav')
