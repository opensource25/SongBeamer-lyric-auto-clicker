from pynput import keyboard
import csv
import json
import os
from difflib import SequenceMatcher
from vosk import Model, KaldiRecognizer

from config import *


class SongAutoClicker:
    def __init__(self):
        self.songlist = {}
        self.compatible_songs = {}

        self.current_song = None
        self.current_song_index = 0
        self.current_verse = None
        self.current_verse_index = 0

    # def setup_voice_recognition(self, vosk_model_path=vosk_modle_path):
    #     audio = pyaudio.PyAudio()
    #     self.stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    #
    #     model = Model(vosk_model_path)
    #     self.recognizer = KaldiRecognizer(model, "rate")
    #
    # def voice_recognize(self):
    #     while True:
    #         data = self.stream.read(CHUNK)
    #         if self.recognizer.AcceptWaveform(data):
    #             result = json.loads(self.recognizer.Result())
    #

    def setup_hotkeys(self):
        # could be remapped with auto hot key for example to the numpad
        hotkeys = {
            'f13': self.next_song,
            'f14': self.previous_song,
            'f15': self.next_verse,
            'f16': self.previous_verse,
            'f17': self.pause,
            'f18': self.play,
            'f19': self.exit
        }
        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()

    # Hotkey Callbacks
    def next_song(self):
        if self.current_song_index == len(self.songlist):
            print("no more songs")
        else:
            self.current_song = list(self.songlist.keys())[self.current_song_index + 1]

        print("next song")

    def previous_song(self):
        print("previous song")

    def next_verse(self):
        if self.current_song_index + 2 <= 9:
            keyboard.Controller.press(str(self.current_song + 2))
        else:
            print("no keyboard shortcut possible")

    def previous_verse(self):
        if self.current_song_index - 1 >= 1:
            keyboard.Controller.press(str(self.current_song - 1))
        else:
            print("no keyboard shortcut possible")

    def pause(self):
        pass


    def play(self):
        if self.current_song_index + 1 <= 9:
            keyboard.Controller.press(str(self.current_song + 1))
        else:
            print("no keyboard shortcut possible")
        print("play")

    def exit(self):
        print("exit")

    def load_songlist(self, songlist_path=songlist_path):
        with open(songlist_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                songname = line.replace("\n", "").strip()
                # check if song is compatible
                if songname in self.compatible_songs.keys():
                    # adding song to songlist
                    song_data = self.load_song(songname)
                    self.songlist.update({songname: song_data})
                else:
                    raise Exception("Song " + songname + " is not compatible.")

    def load_song(self, songname):
        sng_filename = self.songlist[songname]
        sng_path = os.path.join(sng_dir, sng_filename)
        song_data = {}
        lastline = ""
        versename = ""
        verse = []
        with open(sng_path, "r") as sng_file:
            sng_lines = sng_file.readlines()
            # parse .sng file
            for line in sng_lines:
                line = line.replace("\n", "").strip()
                if line.startswith("#"):
                    if line.startswith("#Title="):
                        song_data.update({"titel": line.replace("#Title=", "").strip()})
                    elif line.startswith("#VerseOrder="):
                        song_data.update({"verse_order": line.replace("#VerseOrder=", "").split(",")})
                elif line.strip() == ("--" or "---"):
                    lastline = "splitter"
                    if len(verse) > 0:
                        song_data.update({versename: verse})
                        verse = []
                        versename = ""
                else:
                    line = line.strip()
                    if lastline == "splitter":
                        versename = line
                        lastline = "versename"
                    elif lastline == "versename":
                        verse.append(line)
                        lastline = "verse"
                    elif lastline == "verse":
                        verse.append(line)

        return song_data

    def load_compatible_songs(self):
        with open(compatible_songs_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            # skip header
            next(reader)
            for row in reader:
                self.compatible_songs.update({row[0]: row[1]})




if __name__ == '__main__':
    clicker = SongAutoClicker()
    clicker.setup_hotkeys()
    clicker.load_compatible_songs()
    clicker.load_songlist()
