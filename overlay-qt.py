from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HelpOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 255);")  # Semi-transparent grey

        layout = QVBoxLayout()

        labels = [("F13: ", "Next Song"), ("F14: ", "Previous Song"), ("F15: ", "Next Verse"),
                  ("F16: ", "Previous Verse"), ("F17: ", "Pause"), ("F18: ", "Play"), ("F19: ", "Exit")]

        font = QFont("Consolas", 14)

        for label_text, text in labels:
            label = QLabel(f"{label_text} {text}")
            label.setFont(font)
            layout.addWidget(label)

        self.setLayout(layout)


class StatusOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        layout = QVBoxLayout()

        self.song = QLabel("<songname>")
        self.verse = QLabel("<versename>")
        self.next_verse = QLabel("<Next Verse>")
        self.next_song = QLabel("<next song>")

        labels = [("Song: ", self.song), ("Verse: ", self.verse), ("next Verse: ", self.next_verse),
                  ("next Song: ", self.next_song)]

        font = QFont("Consolas", 14)

        for label_text, label in labels:
            label.setFont(font)
            layout.addWidget(QLabel(label_text))
            layout.addWidget(label)


if __name__ == '__main__':
    app = QApplication([])

    help_overlay = HelpOverlay()
    help_overlay.show()

    # status_overlay = StatusOverlay()
    # status_overlay.show()

    app.exec_()
