import pyaudio


sng_dir = "./example-files/songs"
compatible_songs_path = "./example-files/compatible_songs.csv"

songlist_path = "./example-files/songlist.txt"

# voice recognition
vosk_model_path = "./models/vosk-model-de-0.21"
# pyaudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
