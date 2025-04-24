from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont
import time
import threading
from instrument import MusicPlayer, note_to_frequency
from core.recorder import get_recorder

class PianoKey(QPushButton):
    def __init__(self, note, display_name, is_black=False, parent=None):
        super().__init__(parent)
        self.note = note
        self.display_name = display_name
        self.is_black = is_black
        self._init_ui()
    
    def _init_ui(self):
        palette = self.palette()
        if self.is_black:
            palette.setColor(QPalette.Button, QColor(0, 0, 0))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            self.setStyleSheet("QPushButton { border: 1px solid black; background-color: black; }")
        else:
            palette.setColor(QPalette.Button, QColor(255, 255, 255))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            self.setStyleSheet("QPushButton { border: 1px solid black; background-color: white; }")
        
        self.setPalette(palette)
        self.setText(self.display_name)
        self.setFont(QFont("", 15))
        self.setFocusPolicy(Qt.NoFocus)
        self.setFlat(False)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def set_pressed_style(self):
        self.setStyleSheet(f"QPushButton {{ border: 1px solid {'black'}; "
                          f"background-color: {'#323232' if self.is_black else '#c8c8c8'}; }}")
    
    def set_released_style(self):
        self.setStyleSheet(f"QPushButton {{ border: 1px solid {'black'}; "
                          f"background-color: {'black' if self.is_black else 'white'}; }}")


class PianoWidget(QWidget):
    WHITE_NOTES = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si"]
    BLACK_NOTES = ["Do#", "Ré#", "Fa#", "Sol#", "La#"]
    ENG_WHITE_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
    ENG_BLACK_NOTES = ["C#", "D#", "F#", "G#", "A#"]
    BLACK_POSITIONS = [0, 1, 3, 4, 5]
    
    def __init__(self, octaves=2, parent=None):
        super().__init__(parent)
        self.octaves = octaves
        self.music_player = MusicPlayer()
        self.recorder = get_recorder()
        self.white_keys = []
        self.black_keys = []
        self.is_playing_music = False
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.status_label = QLabel("Piano ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.octaves_label = QLabel(f"Number of octaves: {self.octaves}")
        self.octaves_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.octaves_label)

        self.piano_container = QFrame()
        self.piano_container.setFrameStyle(QFrame.StyledPanel)
        self.piano_container.setMinimumHeight(200)
        main_layout.addWidget(self.piano_container)

        self._create_keyboard()
    
    def _create_keyboard(self):
        def make_handler(func, note):
            return lambda checked=False: func(note)
        
        if self.piano_container.layout():
            while self.piano_container.layout().count():
                item = self.piano_container.layout().takeAt(0)
                if item.widget(): item.widget().deleteLater()
            QWidget().setLayout(self.piano_container.layout())
        
        for key in self.white_keys + self.black_keys:
            if key.parent(): key.setParent(None)
            key.deleteLater()
        
        self.white_keys.clear()
        self.black_keys.clear()
        
        piano_layout = QGridLayout(self.piano_container)
        piano_layout.setContentsMargins(0, 0, 0, 0)
        piano_layout.setSpacing(0)
        
        for octave in range(self.octaves):
            for i, (display_name, eng_name) in enumerate(zip(self.WHITE_NOTES, self.ENG_WHITE_NOTES)):
                note = f"{eng_name}{octave+4}" 
                key = PianoKey(note, display_name, is_black=False)
                key.setMinimumHeight(150)
                col = octave * len(self.WHITE_NOTES) + i
                piano_layout.addWidget(key, 0, col, 2, 1) 
                key.pressed.connect(make_handler(self._on_key_pressed, note))
                key.released.connect(make_handler(self._on_key_released, note))
                self.white_keys.append(key)
        
        for octave in range(self.octaves):
            for i, pos in enumerate(self.BLACK_POSITIONS):
                if i < len(self.BLACK_NOTES):
                    eng_name = self.ENG_BLACK_NOTES[i]
                    display_name = self.BLACK_NOTES[i]
                    note = f"{eng_name}{octave+4}"
                    key = PianoKey(note, display_name, is_black=True)
                    key.setFixedHeight(100)
                    col = octave * len(self.WHITE_NOTES) + pos
                    piano_layout.addWidget(key, 0, col, 1, 1) 
                    key.pressed.connect(make_handler(self._on_key_pressed, note))
                    key.released.connect(make_handler(self._on_key_released, note))
                    self.black_keys.append(key)
        
        for i in range(piano_layout.columnCount()):
            piano_layout.setColumnStretch(i, 1)
    
    def _on_key_pressed(self, note):
        for key in self.white_keys + self.black_keys:
            if key.note == note:
                key.set_pressed_style()
                break
        
        try:
            frequency = note_to_frequency.get(note)
            if frequency:
                if isinstance(frequency, tuple):
                    frequency = frequency[0]
                
                threading.Thread(
                    target=self.music_player.play_piano_tone,
                    args=(frequency, 0.3)
                ).start()
                
                if self.recorder.is_currently_recording():
                    self.recorder.add_note(note)
        except Exception as e:
            self.status_label.setText(f"Error playing note: {e}")
    
    def _on_key_released(self, note):
        for key in self.white_keys + self.black_keys:
            if key.note == note:
                key.set_released_style()
                break
        
        self.status_label.setText("Piano ready")
    
    def set_octaves(self, octaves):
        if self.octaves != octaves:
            self.octaves = octaves
            self.octaves_label.setText(f"Number of octaves: {self.octaves}")
            self._create_keyboard()
    
    def play_music(self, notes):
        if self.is_playing_music:
            return
        
        self.is_playing_music = True
        self.status_label.setText(f"Playing music: {len(notes)} notes")
        
        thread = threading.Thread(target=self._play_notes_thread, args=(notes,))
        thread.daemon = True
        thread.start()
    
    def _play_notes_thread(self, notes):
        try:
            for note, duration in notes:
                if note in ("0", "Unknown"):
                    time.sleep(duration)
                    continue
                
                try:
                    frequency = note_to_frequency.get(note)
                    if frequency:
                        if isinstance(frequency, tuple):
                            frequency = frequency[0]
                        self.music_player.play_piano_tone(frequency, duration)
                    else:
                        time.sleep(duration)
                except Exception as e:
                    print(f"Error playing note {note}: {e}")
                    time.sleep(duration)
            
            self.status_label.setText("Piano ready")
        except Exception as e:
            self.status_label.setText(f"Error playing music: {e}")
        finally:
            self.is_playing_music = False
    
    def recording_started(self):
        self.status_label.setText("Recording started")
    
    def recording_stopped(self):
        self.status_label.setText("Recording stopped")