from tkinter import font
import tkinter as tk


class HelpOverlay:
    def __init__(self):
        self.root = tk.Tk()

        bg_color = "#D3D3D3"

        labels = [("F13: ", "Next Song"), ("F14: ", "Previous Song"), ("F15: ", "Next Verse"),
                  ("F16: ", "Previous Verse"), ("F17: ", "Pause"), ("F18: ", "Play"), ("F19: ", "Exit")]

        # Create the labels in a loop
        for i, (label_text, text) in enumerate(labels):
            tk.Label(self.root, text=label_text, justify="left", background=bg_color, foreground="black").grid(column=0, row=i, sticky='e')
            tk.Label(self.root, text=text, background=bg_color, foreground="black").grid(column=1, row=i, sticky='w')

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
        self.root.geometry("+%d+%d" % (screen_width - window_width, screen_height - window_height))  # Adjust the numbers as needed

        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.mainloop()


if __name__ == "__main__":
    help_overlay = HelpOverlay()