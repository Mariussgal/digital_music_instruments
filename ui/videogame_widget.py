from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont
import time
import threading
from instrument import MusicPlayer, note_to_frequency
from core.recorder import get_recorder

KEYBOARD_TO_NOTES = {
    Qt.Key_A: "C4",
    Qt.Key_Z: "D4",
    Qt.Key_E: "E4",
    Qt.Key_R: "F4",
    Qt.Key_T: "G4",
    Qt.Key_Y: "A4",
    Qt.Key_U: "B4",
    Qt.Key_I: "C5",
    Qt.Key_O: "D5",
    Qt.Key_P: "E5",
    Qt.Key_W: "F5",
    Qt.Key_X: "G5",
    Qt.Key_C: "A5",
    Qt.Key_V: "B5",
    Qt.Key_1: "C6",
    Qt.Key_2: "D6",
    Qt.Key_3: "E6",
    Qt.Key_4: "F6",
    Qt.Key_5: "G6",
    Qt.Key_6: "A6",
    Qt.Key_7: "B6",
}



class GameButton(QPushButton):    
    def __init__(self, icon_name, note, parent=None):
        super().__init__(parent)
        self.note = note
        self.icon_name = icon_name
        self._init_ui()
    
    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(40, 40)
        self.setMaximumSize(120, 120)
        
        try:
            self.setIcon(QIcon(f"assets/Icons/{self.icon_name}.png"))
            self.setIconSize(QSize(32, 32))
        except:
            self.setText(self.note)
            self.setFont(QFont("", 10, QFont.Bold))
        
        self.setFlat(True)
        self.setFocusPolicy(Qt.NoFocus)
        
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: #f0f0f0;
                min-width: 40px;
                min-height: 40px;
                padding: 2px;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
                border: 2px solid #4f4f4f;
            }
        """)
    
    def set_pressed_style(self):
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #4f4f4f;
                border-radius: 6px;
                background-color: #d0d0d0;
                min-width: 40px;
                min-height: 40px;
                padding: 2px;
            }
        """)
    
    def set_released_style(self):
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: #f0f0f0;
                min-width: 40px;
                min-height: 40px;
                padding: 2px;
            }
        """)
    
    def resizeEvent(self, event):
        size = min(self.width(), self.height()) - 16 
        self.setIconSize(QSize(size, size))
        super().resizeEvent(event)


class VideogameWidget(QWidget):
    BASE_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
    GAME_ICONS = [
        "super-mario", "super-mario1", "plante-carnivore", "pieces-de-monnaie", 
        "champignon", "waluigi", "plante", "mario", "jeu", "le-manoir-de-luigi"
    ]
    
    def __init__(self, octaves=2, parent=None):
        super().__init__(parent)
        self.octaves = octaves
        self.music_player = MusicPlayer()
        self.recorder = get_recorder()
        self.buttons = []
        self.is_playing_music = False
        self._init_ui()
    
    def _init_ui(self):
        #Builds the graphical interface of the video game mode.
        #Displays information, the button grid, and configures keyboard focus.
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.status_label = QLabel("Video Game ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.octaves_label = QLabel(f"Number of octaves: {self.octaves}")
        self.octaves_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.octaves_label)
        
        self.setFocusPolicy(Qt.StrongFocus)
        QTimer.singleShot(0, self.setFocus)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        keyboard_info = QLabel("Use the A Z E R T Y U I O P W X C V 1 2 3 4 5 6 7 keys to play")
        keyboard_info.setAlignment(Qt.AlignCenter)
        keyboard_info.setStyleSheet("background-color: #e6f7ff; padding: 5px; border-radius: 3px;")
        main_layout.addWidget(keyboard_info)
        
        self.buttons_container = QWidget()
        scroll_area.setWidget(self.buttons_container)
        
        main_layout.addWidget(scroll_area, 1)  
        
        self._create_buttons()
    
    def _get_notes_for_octave(self):
        #Generates the list of notes to display according to the number of octaves.
        notes = []
        
        for octave in range(4, 4 + self.octaves):
            for note in self.BASE_NOTES:
                notes.append(f"{note}{octave}")
        
        return notes
    
    def keyPressEvent(self, event):
        note = KEYBOARD_TO_NOTES.get(event.key())
        if note:
            self._on_button_pressed(note)
            QTimer.singleShot(150, lambda: self._on_button_released(note))
        else:
            super().keyPressEvent(event)
    
    def _create_buttons(self):
        #Creates and displays the buttons for the game.
        if self.buttons_container.layout():
            while self.buttons_container.layout().count():
                item = self.buttons_container.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(self.buttons_container.layout())
        
        for button in self.buttons:
            if button.parent(): button.setParent(None)
            button.deleteLater()
        self.buttons.clear()
        
        buttons_layout = QGridLayout(self.buttons_container)
        buttons_layout.setContentsMargins(10, 10, 10, 10)
        buttons_layout.setSpacing(5)
        
        game_notes = self._get_notes_for_octave()
        
        num_columns = min(len(game_notes), 7)  
        
        for i, note in enumerate(game_notes):
            icon_index = i % len(self.GAME_ICONS)
            icon = self.GAME_ICONS[icon_index]
            
            button = GameButton(icon, note)
            
            def make_pressed_handler(n):
                return lambda: self._on_button_pressed(n)
            
            def make_released_handler(n):
                return lambda: self._on_button_released(n)
            
            button.pressed.connect(make_pressed_handler(note))
            button.released.connect(make_released_handler(note))
            
            row = i // num_columns
            col = i % num_columns
            buttons_layout.addWidget(button, row, col)
            self.buttons.append(button)
        for i in range(buttons_layout.rowCount()):
            buttons_layout.setRowStretch(i, 1)
        for i in range(buttons_layout.columnCount()):
            buttons_layout.setColumnStretch(i, 1)
    
    def _on_button_pressed(self, note):
        #Handles the press of a button.
        for button in self.buttons:
            if button.note == note:
                button.set_pressed_style()
                break
        try:
            frequency = note_to_frequency.get(note)
            if frequency:
                if isinstance(frequency, tuple):
                    frequency = frequency[0]

                threading.Thread(
                    target=self.music_player.play_videoGame_tone,
                    args=(frequency, 0.3)
                ).start()

                if self.recorder.is_currently_recording():
                    self.recorder.add_note(note)

                self.status_label.setText(f"Playing note: {note}")
        except Exception as e:
            self.status_label.setText(f"Error playing note: {e}")
    
    def _on_button_released(self, note):
        #Handles the release of a button
        #Restores the normal color of the button.
        for button in self.buttons:
            if button.note == note:
                button.set_released_style()
                break
        
        self.status_label.setText("Video Game ready")
    
    def set_octaves(self, octaves):
        #Changes the number of octaves displayed and updates the interface.
        if self.octaves != octaves:
            self.octaves = octaves
            self.octaves_label.setText(f"Number of octaves: {self.octaves}")
            self._create_buttons()
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
                        
                        self.music_player.play_videoGame_tone(frequency, duration)
                    else:
                        time.sleep(duration)
                except Exception as e:
                    print(f"Error playing note {note}: {e}")
                    time.sleep(duration)  

            self.status_label.setText("Video Game ready")
        except Exception as e:
            self.status_label.setText(f"Error playing music: {e}")
        finally:
            self.is_playing_music = False
    
    def recording_started(self):
        #Updates the status when recording starts.
        self.status_label.setText("Recording started")
    
    def recording_stopped(self):
        #Updates the status when recording stops.
        self.status_label.setText("Recording finished")