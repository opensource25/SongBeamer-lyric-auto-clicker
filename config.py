import pyaudio


sng_dir = "./Songs"
compatible_songs_path = "./compatible_songs.csv"

songlist_path = "./songlist.txt"

# voice recognition
vosk_model_path = "./models/vosk-model-de-0.21"
# pyaudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
