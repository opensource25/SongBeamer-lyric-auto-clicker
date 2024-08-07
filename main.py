from pynput import keyboard
import csv
import json
import os
import time
import threading
from difflib import SequenceMatcher
from vosk import Model, KaldiRecognizer

import overlay
from config import *


class SongAutoClicker:
    def __init__(self):
        self.songlist = {}
        self.song_order = ()
        self.compatible_songs = {}

        self.current_song_index = -1
        self.current_verse_index = -1

        self.status_overlay = None

        self.keyboard_controller = keyboard.Controller()

        self.new_result = False
        self.result = ""

    @property
    def current_song_data(self):
        return self.songlist[self.song_order[self.current_song_index]]

    @property
    def current_verse_key(self):
        return str(self.current_song_data['keymap'][self.current_verse_index])

    def setup_voice_recognition(self):
        # setup speechrecognition
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        model = Model(vosk_model_path)
        self.recognizer = KaldiRecognizer(model, RATE)

    def voice_recognize(self):
        while True:
            data = self.stream.read(CHUNK)
            if self.recognizer.AcceptWaveform(data):
                self.result = json.loads(self.recognizer.Result())['text']
                self.new_result = True

    def setup_hotkeys(self):
        hotkeys = {
            '<f13>': self.call_next_song,
            '<f14>': self.call_previous_song,
            '<f15>': self.call_next_verse,
            '<f16>': self.call_previous_verse,
            '<f17>': self.call_pause,
            '<f18>': self.call_play,
            '<f19>': self.call_exit
        }
        hotkeys_test = {
            '<f6>': self.call_next_song,
            '<f7>': self.call_previous_song,
            '<f8>': self.call_next_verse,
            '<f9>': self.call_previous_verse,
            '<f10>': self.call_pause,
            '<f11>': self.call_play,
            '<f12>': self.call_exit
        }
        self.hotkey_listener = keyboard.GlobalHotKeys(hotkeys_test)
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener.run)
        self.hotkey_thread.start()

    def setup_overlay(self, app):
        self.overlay_thread = overlay.OverlayThread(app)
        print("Starting overlay")
        self.overlay_thread.start()
        print("Overlay started")
        self.status_overlay = self.overlay_thread.get_status_overlay()

    @staticmethod
    def loop_indexes(index, length):
        if index < 0:
            return length - 1
        elif index >= length:
            return 0
        else:
            return index

    def next_song_index(self):
        return self.loop_indexes(self.current_song_index + 1, len(self.song_order))

    def previous_song_index(self):
        return self.loop_indexes(self.current_song_index - 1, len(self.song_order))

    def next_verse_index(self):
        return self.loop_indexes(self.current_verse_index + 1, len(self.current_song_data.get('verse_order')))

    def previous_verse_index(self):
        return self.loop_indexes(self.current_verse_index - 1, len(self.current_song_data.get('verse_order')))

    # Hotkey Callbacks
    def call_next_song(self):
        self.current_song_index = self.next_song_index()
        self.current_verse_index = 0

        self.status_overlay.update_status(song=self.song_order[self.current_song_index],
                                          verse=self.current_song_data.get('verse_order')[self.current_verse_index],
                                          next_verse=self.current_song_data.get('verse_order')[self.next_verse_index()],
                                          next_song=self.song_order[self.next_song_index()])

    def call_previous_song(self):
        self.current_song_index = self.previous_song_index()
        self.current_verse_index = 0

        self.status_overlay.update_status(song=self.song_order[self.current_song_index],
                                          verse=self.current_song_data.get('verse_order')[self.current_verse_index],
                                          next_verse=self.current_song_data.get('verse_order')[self.next_verse_index()],
                                          next_song=self.song_order[self.next_song_index()])

    def call_next_verse(self):
        self.current_verse_index = self.next_verse_index()

        self.keyboard_controller.tap(key=self.current_verse_key)
        self.status_overlay.update_status(verse=self.current_song_data.get('verse_order')[self.current_verse_index],
                                          next_verse=self.current_song_data.get('verse_order')[self.next_verse_index()])

    def call_previous_verse(self):
        self.current_verse_index = self.previous_verse_index()

        self.keyboard_controller.tap(key=self.current_verse_key)
        self.status_overlay.update_status(verse=self.current_song_data.get('verse_order')[self.current_verse_index],
                                          next_verse=self.current_song_data.get('verse_order')[self.next_verse_index()])

    def call_pause(self):
        pass

    def call_play(self):
        pass

    def call_exit(self):
        pass

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
        self.song_order = tuple(self.songlist.keys())

    def load_song(self, songname):
        sng_filename = self.compatible_songs[songname]
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
                    else:
                        continue
                elif line == "--" or line == "---":
                    lastline = "splitter"
                    if len(verse) > 0:
                        song_data.update({versename: verse})
                        verse = []
                        versename = ""
                else:
                    if lastline == "splitter":
                        versename = line
                        lastline = "versename"
                    elif lastline == "versename":
                        verse.append(line)
                        lastline = "verse"
                    elif lastline == "verse":
                        verse.append(line)

            song_keymap_by_verse_name = {}  # {verse_name: key}
            song_keymap_by_verse_index = {}  # {verse_index: key}
            for verse_index, verse in enumerate(song_data["verse_order"], start=1):
                if song_keymap_by_verse_name.get(verse) is None:
                    song_keymap_by_verse_name.update({verse_index: verse_index})

                key = song_keymap_by_verse_name.get(verse)
                song_keymap_by_verse_index.update({verse_index: key})

            song_data.update({"keymap": song_keymap_by_verse_index})

            if len(verse) > 0 and len(set(song_data["verse_order"])) < 10:
                self.songlist.update({songname: song_data})

        return song_data

    def load_compatible_songs(self):
        with open(compatible_songs_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            # skip header
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    self.compatible_songs.update({row[0]: row[1]})
                else:
                    print(f"Warning: Skipping row with fewer than 2 columns: {row}")

    def mainloop(self):
        while True:
            if self.new_result:
                self.new_result = False
                print(self.result)
            else:
                time.sleep(0.25)


if __name__ == '__main__':
    app = overlay.QApplication([])
    clicker = SongAutoClicker()

    clicker.load_compatible_songs()
    print("Compatible songs loaded")
    clicker.load_songlist()
    print("Songlist loaded")

    clicker.setup_voice_recognition()
    print("Voice recognition setup")

    threading.Thread(target=clicker.voice_recognize).start()
    threading.Thread(target=clicker.mainloop).start()

    clicker.setup_hotkeys()
    print("Hotkeys setup")
    clicker.setup_overlay(app)
    app.exec_()
    print("Overlay setup")
