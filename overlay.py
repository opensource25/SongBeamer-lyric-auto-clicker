from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDesktopWidget, QGridLayout
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont
import threading


class HelpOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(200, 200, 200, 200);")

        layout = QVBoxLayout()

        labels = [("F13", "Next Song"), ("F14", "Previous Song"), ("F15", "Next Verse"),
                  ("F16", "Previous Verse"), ("F17", "Pause"), ("F18", "Play"), ("F19", "Exit")]

        font = QFont("Consolas", 14)

        for key, info in labels:
            label = QLabel(f"{key}: {info}")
            label.setFont(font)
            layout.addWidget(label)

        self.setLayout(layout)

    def showEvent(self, event):
        # Move the widget to the bottom right corner
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width() - 10, screen_geometry.height() - self.height() - 10)


class StatusOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(200, 200, 200, 200);")

        layout = QGridLayout()

        self.song = QLabel("<songname>")
        self.verse = QLabel("<versename>")
        self.next_verse = QLabel("<Next Verse>")
        self.next_song = QLabel("<next song>")

        labels = [("Song:", self.song), ("Verse:", self.verse), ("next Verse:", self.next_verse),
                  ("next Song:", self.next_song)]

        font = QFont("Consolas", 14)

        for i, (title, content) in enumerate(labels):
            title_label = QLabel(title)
            title_label.setFont(font)
            layout.addWidget(title_label, i, 0, alignment=Qt.AlignRight)

            content.setFont(font)
            layout.addWidget(content, i, 1, alignment=Qt.AlignLeft)

        self.setLayout(layout)

    def update_status(self, song=None, verse=None, next_verse=None, next_song=None):
        if song is not None:
            self.song.setText(song)
        if verse is not None:
            self.verse.setText(verse)
        if next_verse is not None:
            self.next_verse.setText(next_verse)
        if next_song is not None:
            self.next_song.setText(next_song)
        self.repaint()

    def showEvent(self, event):
        # Move the widget to the top right corner
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width() - 10, 10)


class OverlayThread(QThread):
    def __init__(self, app):
        super().__init__()
        self.status_overlay = None
        self.help_overlay = None
        self.app = app
        self.overlay_initialized = threading.Event()
        print("Initializing overlay thread")

    def run(self):
        print("Starting overlay")

        self.help_overlay = HelpOverlay()
        self.status_overlay = StatusOverlay()

        self.help_overlay.show()
        self.status_overlay.show()

        self.overlay_initialized.set()
        print("Overlay started")

    def get_status_overlay(self):
        self.overlay_initialized.wait()
        return self.status_overlay
