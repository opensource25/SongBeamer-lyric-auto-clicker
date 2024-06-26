from pynput import keyboard
import csv

import config

class SongAutoClicker():
    def __init__(self):
        self.songlist = []

    def setup_hotkeys(self):
        # could be remapped with auto hot key for example to the numpad
        hotkeys = {
            'f13' : self.next_song,
            'f14' : self.previous_song,
            'f15' : self.next_verse,
            'f16' : self.previous_verse,
            'f17' : self.pause,
            'f18' : self.play,
            'f19' : self.exit
        }
        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()

    # Hotkey Callbacks
    def next_song(self):
        print("next song")

    def previous_song(self):
        print("previous song")

    def next_verse(self):
        print("next verse")

    def previous_verse(self):
        print("previous verse")

    def pause(self):
        print("pause")

    def play(self):
        print("play")

    def exit(self):
        print("exit")


    def read_songlist(self, songlist_path=config.songlist_path):
        with open(songlist_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                self.songlist.append(line.replace("\n", "").strip())

    def check_songlist(self):
        for song in self.songlist:
            self.check_song_compatability(song)


    def load_song(self):
        pass




    def check_song_compatability(self, songname):
        with open(config.compatible_songs_path, "r", encoding="utf-8") as f:
            csvreader = csv.DictReader(f, delimiter=";")
            for row in csvreader:
                if row.get('songname') == songname:
                    return True
                else:
                    return False




if __name__ == '__main__':
    clicker = SongAutoClicker()
    # clicker.setup_hotkeys()
    # clicker.read_songlist()
    clicker.check_song_compatability("test")
