from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class XylophoneWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel("Xylophone Widget - Hello World!")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
    
    def play_music(self, notes):
        self.label.setText(f"Playing {len(notes)} notes on Xylophone")
    
    def recording_started(self):
        self.label.setText("Xylophone - Recording started")
    
    def recording_stopped(self):
        self.label.setText("Xylophone Widget - Hello World!")