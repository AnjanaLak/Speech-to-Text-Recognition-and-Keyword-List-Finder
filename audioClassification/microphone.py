### This will check and validate the microphone
import argparse

import pyaudio


# PyAudio Microphone List
def list_microphones():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    MICROPHONES_LIST = []
    MICROPHONES_DESCRIPTION = []
    MICROPHONES_NAMES = []
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            desc = "# %d - %s" % (i, p.get_device_info_by_host_api_device_index(0, i).get('name'))
            MICROPHONES_DESCRIPTION.append(desc)
            MICROPHONES_NAMES.append(p.get_device_info_by_host_api_device_index(0, i).get('name'))
            MICROPHONES_LIST.append(i)

    output = []
    output.append("=== Available Microphones: ===")
    output.append("\n".join(MICROPHONES_DESCRIPTION))
    output.append("======================================")
    return "\n".join(output), MICROPHONES_DESCRIPTION, MICROPHONES_LIST


output, desc, l = list_microphones()
print(output)

###########################
# Check Microphone
###########################
print("=====")
print("1 / 2: Checking Microphones... ")
print("=====")

desc, mics, indices = list_microphones()
if (len(mics) == 0):
    print("Error: No microphone found.")
    ### Need to report if no mic is found during the exam
    ### Need to check mic and display if mic is not connected
    # exit()

#############################################################################################################

#############
# Read Command Line Args
#############
MICROPHONE_INDEX = indices[0]
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mic", help="Select which microphone / input device to use")
args = parser.parse_args()
try:
    if args.mic:
        MICROPHONE_INDEX = int(args.mic)
        print("User selected mic: %d" % MICROPHONE_INDEX)
    else:
        mic_in = input("Select microphone [%d]: " % MICROPHONE_INDEX).strip()
        if (mic_in != ''):
            MICROPHONE_INDEX = int(mic_in)
except:
    print("Invalid microphone")
    ## Needs to report about the invalid mic status
    exit()

# Find description that matches the mic index
mic_desc = ""
for k in range(len(indices)):
    i = indices[k]
    if (i == MICROPHONE_INDEX):
        mic_desc = mics[k]
print("Using mic: %s" % mic_desc)
