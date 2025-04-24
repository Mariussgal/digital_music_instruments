#xylophone_widget.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QScrollArea, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import time
import threading
from instrument import MusicPlayer, note_to_frequency
from core.recorder import get_recorder

class XylophoneBar(QPushButton):

    COLORS = [
        "#8800FF",  # Violet
        "#4B0082",  # Indigo
        "#0000FF",  # Blue
        "#00FF00",  # Green
        "#FFFF00",  # Yellow
        "#FF7F00",  # Orange
        "#FF0000",  # Red
        "#FF1493",  # Pink
    ]
    
    def __init__(self, note, display_name, color_index, parent=None):
        super().__init__(parent)
        self.note = note
        self.display_name = display_name
        self.color_index = color_index
        self._init_ui()
    
    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(40, 100)
        
        color = self.COLORS[self.color_index % len(self.COLORS)]
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 2px solid #1a1a1a;
                border-radius: 8px;
                color: black;
                font-weight: bold;
                min-height: 100px;
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color)};
                border: 2px solid black;
            }}
        """)
        
        self.setText(self.display_name)
        self.setFont(QFont("Arial", 12, QFont.Bold))
        self.setFocusPolicy(Qt.NoFocus)
    
    def _darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        factor = 0.8 # decrease of 20%
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def set_pressed_style(self):
        color = self.COLORS[self.color_index % len(self.COLORS)]
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._darken_color(color)};
                border: 2px solid black;
                border-radius: 8px;
                color: black;
                font-weight: bold;
                min-height: 100px;
            }}
        """)
    
    def set_released_style(self):
        color = self.COLORS[self.color_index % len(self.COLORS)]
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 2px solid #1a1a1a;
                border-radius: 8px;
                color: black;
                font-weight: bold;
                min-height: 100px;
            }}
        """)

class XylophoneWidget(QWidget):
    NOTES = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si", "Do"]
    ENG_NOTES = ["C", "D", "E", "F", "G", "A", "B", "C"]
    
    def __init__(self, octaves=2, parent=None):
        super().__init__(parent)
        self.octaves = octaves
        self.music_player = MusicPlayer()
        self.recorder = get_recorder()
        self.bars = []
        self.is_playing_music = False
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.status_label = QLabel("Xylophone ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.octaves_label = QLabel(f"Number of octaves: {self.octaves}")
        self.octaves_label.setAlignment(Qt.AlignCenter)
        
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.octaves_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.bars_container = QWidget()
        scroll_area.setWidget(self.bars_container)
        
        main_layout.addWidget(scroll_area, 1) 
        
        self._create_bars()
    
    def _get_notes_for_octave(self):
        notes = []
        
        for octave in range(4, 4 + self.octaves):
            for note_index, eng_note in enumerate(self.ENG_NOTES):
                if note_index == len(self.ENG_NOTES) - 1:
                    if octave == 3 + self.octaves:
                        continue
                    note = f"{eng_note}{octave+1}"
                else:
                    note = f"{eng_note}{octave}"
                notes.append((note, self.NOTES[note_index]))
        return notes
    
    def _create_bars(self):
        if self.bars_container.layout():
            while self.bars_container.layout().count():
                item = self.bars_container.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(self.bars_container.layout())
        
        for bar in self.bars:
            if bar.parent(): bar.setParent(None)
            bar.deleteLater()
        self.bars.clear()
        
        bars_layout = QHBoxLayout(self.bars_container)
        bars_layout.setContentsMargins(10, 10, 10, 10)
        bars_layout.setSpacing(5)
        
        xylophone_notes = self._get_notes_for_octave()
        
        for i, (note, display_name) in enumerate(xylophone_notes):
            bar = XylophoneBar(note, display_name, i % len(XylophoneBar.COLORS))
            
            def make_pressed_handler(n):
                return lambda: self._on_bar_pressed(n)
            
            def make_released_handler(n):
                return lambda: self._on_bar_released(n)
            
            bar.pressed.connect(make_pressed_handler(note))
            bar.released.connect(make_released_handler(note))
            
            bars_layout.addWidget(bar)
            self.bars.append(bar)
    
    def _on_bar_pressed(self, note):
        for bar in self.bars:
            if bar.note == note:
                bar.set_pressed_style()
                break
        
        try:
            frequency = note_to_frequency.get(note)
            if frequency:
                if isinstance(frequency, tuple):
                    frequency = frequency[0]
                
                threading.Thread(
                    target=self.music_player.play_xylophone_tone,
                    args=(frequency, 0.3)
                ).start()
                
                if self.recorder.is_currently_recording():
                    self.recorder.add_note(note)
                
                self.status_label.setText(f"Playing note: {note}")
        except Exception as e:
            self.status_label.setText(f"Error playing note: {e}")
    
    def _on_bar_released(self, note):
        for bar in self.bars:
            if bar.note == note:
                bar.set_released_style()
                break
        
        self.status_label.setText("Xylophone ready")
    
    def set_octaves(self, octaves):
        if self.octaves != octaves:
            self.octaves = octaves
            self.octaves_label.setText(f"Number of octaves: {self.octaves}")
            self._create_bars()
            self.status_label.setText(f"Changed to {octaves} octaves")
    
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
                if note == "0" or note == "Unknown":  
                    time.sleep(duration)
                    continue
                try:
                    frequency = note_to_frequency.get(note)
                    if frequency:
                        if isinstance(frequency, tuple):
                            frequency = frequency[0]
                        
                        self.music_player.play_xylophone_tone(frequency, duration)
                    else:
                        time.sleep(duration)
                except Exception as e:
                    print(f"Error playing note {note}: {e}")
                    time.sleep(duration)  

            self.status_label.setText("Xylophone ready")
        except Exception as e:
            self.status_label.setText(f"Error playing music: {e}")
        finally:
            self.is_playing_music = False
    
    def recording_started(self):
        self.status_label.setText("Recording started")
    
    def recording_stopped(self):
        self.status_label.setText("Recording finished")