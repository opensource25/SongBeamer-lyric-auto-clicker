from tkinter import font
import tkinter as tk
import threading


class HelpOverlay:
    def __init__(self):
        self.root = tk.Tk()

        bg_color = "#D3D3D3"

        labels = [("F13: ", "Next Song"), ("F14: ", "Previous Song"), ("F15: ", "Next Verse"),
                  ("F16: ", "Previous Verse"), ("F17: ", "Pause"), ("F18: ", "Play"), ("F19: ", "Exit")]

        # Create the labels in a loop
        for i, (label_text, text) in enumerate(labels):
            tk.Label(self.root, text=label_text, justify="left", background=bg_color).grid(column=0, row=i, sticky='e')
            tk.Label(self.root, text=text, background=bg_color).grid(column=1, row=i, sticky='w')

        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Consolas", size=14)
        self.root.configure(background=bg_color)

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        print(window_width, window_height)

        # Specify the position of the window
        self.root.geometry("+%d+%d" % (screen_width - window_width, screen_height - window_height))

        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_focusmodel("passive")
        self.root.mainloop()


class StatusOverlay:
    def __init__(self):
        self.root = tk.Tk()

        bg_color = "#D3D3D3"

        self.song = tk.StringVar()  # "<songname>"
        self.verse = tk.StringVar  # "<versename>"
        self.next_verse = tk.StringVar  # "<Next Verse>"
        self.next_song = tk.StringVar  # "<next song>"

        labels = [("Song: ", self.song), ("Verse: ", self.verse), ("next Verse: ", self.next_verse),
                  ("next Song: ", self.next_song)]

        # Create the labels in a loop
        for i, (label_text, text) in enumerate(labels):
            tk.Label(self.root, text=label_text, justify="left", background=bg_color).grid(column=0, row=i, sticky='e')
            tk.Label(self.root, textvariable=text, background=bg_color).grid(column=1, row=i, sticky='w')

        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Consolas", size=14)
        self.root.configure(background=bg_color)

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        window_width = 400
        window_height = self.root.winfo_reqheight()

        # Specify the position of the window
        self.root.geometry("%dx%d+%d+%d" % (window_width, window_height, screen_width - window_width - 5, 5))

        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)

    def update_text(self, song, verse: str, next_verse, next_song):
        self.song.set(song)
        self.verse.set(verse)
        self.next_verse.set(next_verse)
        self.next_song.set(next_song)

    def run(self):
        threading.Thread(target=self.root.mainloop).start()
        # self.root.mainloop()


if __name__ == "__main__":
    # help_overlay = HelpOverlay()
    status_overlay = StatusOverlay()
    # threading.Thread(target=status_overlay.run).start()
    status_overlay.run()
    print("test")
    # status_overlay.update_text("Song", "Verse", "Next Verse", "Next Song")
