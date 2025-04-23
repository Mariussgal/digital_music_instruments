from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class PianoWidget(QWidget):    
    def __init__(self, octaves=2, parent=None):
        super().__init__(parent)
        self.octaves = octaves
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Piano Widget - Hello World!")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.octaves_label = QLabel(f"Number of octaves: {self.octaves}")
        self.octaves_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.octaves_label)
    
    def set_octaves(self, octaves):
        self.octaves = octaves
        self.octaves_label.setText(f"Number of octaves: {self.octaves}")
    
    def play_music(self, notes):
        self.label.setText(f"Playing {len(notes)} notes on Piano")
    
    def recording_started(self):
        self.label.setText("Piano - Recording started")
    
    def recording_stopped(self):
        self.label.setText("Piano Widget - Hello World!")