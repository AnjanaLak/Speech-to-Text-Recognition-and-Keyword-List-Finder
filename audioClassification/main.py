import os
import re
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub import AudioSegment as am
import directoryManager
# import keywordList as kw
from datetime import datetime
from audioClassification import db

from audioClassification.models import Audio_Record, audio_Record_Schema

kw = ["one", "tell me", "please", "know", "know this", "correct", "is this", "this", "that", "which", "what",
      "where", "possible", "last", "first", "second", "third", "fourth", "fifth", "final", "here", "hello",
      "one", "two", "three", "four", "five", "question", "correct", "wrong", "incorrect", "not sure", "top",
      "bottom", "maybe", "might be", "true", "false"]


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def listToString(s):
    # initialize an empty string
    str1 = ", "
    # return string
    return (str1.join(s))


def silence_based_conversion(audio_path, candidateID, examinationID):
    ## to get the current working directory
    cwd = os.getcwd()
    ## Importing the directory manager
    dir = directoryManager.createDirectories(candidateID, examinationID, cwd)
    print(os.getcwd() + " ==> is my current working directory")
    with open("api-key.json") as f:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api-key.json'
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    myaudio = AudioSegment.from_file(audio_path, "wav")
    chunk_length_ms = 14000  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)

    # open a file where we will concatenate and store the recognized text

    fh = open("recognized.txt", "w+")

    # move into the directory to store the audio files.
    os.chdir('../data/' + candidateID + '/' + examinationID + '/' + 'audio_chunks')

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
            #rec = r.recognize_google_cloud(audio_listened, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            rec = r.recognize_google(audio_listened)
            print(type(rec))
            print(os.getcwd() + "==> is the directory of chunk processed" + "./chunk{0}.wav".format(i))
            fh.write(rec + ". ")

            ## store values into database as records
            text_record = rec
            matched_keywords = []
            match_records = {}
            candidate_Id = 'IT17019750'
            exam_id = 'IT4140'
            chunk_dir_path = os.getcwd() + "./chunk{0}.wav"
            keywordlist = kw
            print(text_record)

            if text_record:
                for keyword in keywordlist:
                    if findWholeWord(keyword)(text_record):
                        matched_keywords.append(keyword)
                        print("matched")
                    else:
                        # print("Not matched")
                        pass
                # need to insert the record from here
                record = Audio_Record(candidate_Id, exam_id, chunk_dir_path, datetime.now(),
                                      listToString(matched_keywords))  # creating an article object
                db.session.add(record)  # adding the record to the object
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)


                # print(audio_Record_Schema.jsonify(record))
            else:
                print("Chunk is empty")

        except:
            rec = r.recognize_google_cloud(audio_listened, show_all=True)
            print(rec, type(rec))

        i += 1
    os.chdir(cwd)
    print(os.getcwd() + " ==> is my current working directory after processing is completed")

    return 2


def start(audio_path, candidateID, examinationID):
    # path = "output.wav"
    if silence_based_conversion(audio_path, candidateID, examinationID) == 2:
        return "Completed"
    else:
        return "Not completed"
