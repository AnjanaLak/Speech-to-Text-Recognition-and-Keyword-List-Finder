import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub import AudioSegment as am


def silence_based_conversion(path):
    myaudio = AudioSegment.from_file(path, "wav")
    chunk_length_ms = 4000  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec

    # open a file where we will concatenate
    # and store the recognized text
    fh = open("recognized.txt", "w+")

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
            rec = r.recognize_google_cloud(audio_listened)
            # print(rec)
            fh.write(rec + ". ")
        except:
            rec = r.recognize_google_cloud(audio_listened, show_all=True)
            print(rec, type(rec))

        i += 1


if __name__ == '__main__':
    print('Starting speech recognition process')

    # path = input()
    path = 'test.wav'  ## need a .wav file with 16kHz sample rate

    silence_based_conversion(path)


# sound = am.from_file(filepath, format='wav', frame_rate=22050)
# sound = sound.set_frame_rate(16000)
# sound.export(filepath, format='wav')