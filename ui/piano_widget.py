from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, 
                          QSizePolicy, QGridLayout, QHBoxLayout, QComboBox,
                          QDialog, QDialogButtonBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QColor, QPalette, QFont
import time
import threading
from instrument import MusicPlayer, note_to_frequency
from core.recorder import get_recorder



SIMPLE_SONGS = {
    "Au Clair de la Lune": """Do Do Do Ré
Mi Ré Do Mi
Ré Ré Do""",

    "Frère Jacques": """Do Ré Mi Do
Do Ré Mi Do
Mi Fa Sol
Mi Fa Sol
Sol La Sol Fa Mi Do
Sol La Sol Fa Mi Do
Do Sol Do
Do Sol Do""",

    "Happy Birthday": """Do Do Ré Do Fa Mi
Do Do Ré Do Sol Fa
Do Do Do' La Fa Mi Ré
La# La# La Fa Sol Fa""",
    
    "Twinkle Twinkle": """Do Do Sol Sol La La Sol
Fa Fa Mi Mi Ré Ré Do
Sol Sol Fa Fa Mi Mi Ré
Sol Sol Fa Fa Mi Mi Ré
Do Do Sol Sol La La Sol
Fa Fa Mi Mi Ré Ré Do""",
    
    "Vive le Vent": """Mi Mi Mi
Mi Mi Mi
Mi Sol Do Ré Mi
Fa Fa Fa Fa
Fa Mi Mi Mi
Mi Ré Ré Mi Ré Sol""",
    
    "Le Lion est Mort ce Soir": """Fa Mi Ré Do
Fa Mi Ré Do
Fa Mi Ré Do
Fa Mi Ré
Do Ré Mi Fa Sol La
Do' La Sol Fa Mi Ré Do"""
}


# Dictionary of correspondence between keyboard keys and piano notes
KEYBOARD_TO_NOTES = {
    #Octave 1
    Qt.Key_A: "C4", # Do    
    Qt.Key_Q: "C#4", # Do#
    Qt.Key_Z: "D4", # Ré
    Qt.Key_S: "D#4", # Ré#
    Qt.Key_E: "E4",  # Mi
    Qt.Key_R: "F4", # Fa
    Qt.Key_D: "F#4", # Fa#
    Qt.Key_T: "G4", # Sol
    Qt.Key_F: "G#4", # Sol#
    Qt.Key_Y: "A4", # La
    Qt.Key_G: "A#4", # La#
    Qt.Key_U: "B4", # Si
    #Octave 2
    Qt.Key_I: "C5", # Do
    Qt.Key_H: "C#5",  
    Qt.Key_O: "D5",
    Qt.Key_J: "D#5",
    Qt.Key_P: "E5",
    Qt.Key_W: "F5",
    Qt.Key_K: "F#5",
    Qt.Key_X: "G5",
    Qt.Key_L: "G#5",
    Qt.Key_C: "A5",
    Qt.Key_M: "A#5",
    Qt.Key_V: "B5",
    #Octave 3
    Qt.Key_1: "C6",
    Qt.Key_B: "C#6",
    Qt.Key_2: "D6",
    Qt.Key_N: "D#6",
    Qt.Key_3: "E6",
    Qt.Key_4: "F6",
    Qt.Key_5: "G6",
    Qt.Key_6: "A6",
    Qt.Key_7: "B6",
}

# Key names to be displayed
KEY_NAMES = {
    Qt.Key_A: "A", Qt.Key_Z: "Z", Qt.Key_E: "E", Qt.Key_R: "R", 
    Qt.Key_T: "T", Qt.Key_Y: "Y", Qt.Key_U: "U", Qt.Key_I: "I",
    Qt.Key_O: "O", Qt.Key_P: "P", Qt.Key_W: "W", Qt.Key_X: "X",
    Qt.Key_C: "C", Qt.Key_V: "V", Qt.Key_1: "1", Qt.Key_2: "2",
    Qt.Key_3: "3", Qt.Key_4: "4", Qt.Key_5: "5", Qt.Key_6: "6",
    Qt.Key_7: "7", Qt.Key_Q: "Q", Qt.Key_S: "S", Qt.Key_D: "D",
    Qt.Key_F: "F", Qt.Key_G: "G", Qt.Key_H: "H", Qt.Key_J: "J",
    Qt.Key_K: "K", Qt.Key_L: "L", Qt.Key_N: "N", Qt.Key_B: "B",
    Qt.Key_M: "M",
}



class SongCheatSheetDialog(QDialog):
    # Improved dialog window showing song playlists
    
    def __init__(self, song_name, song_notes, parent=None):
       
        # Initializes dialog window with song name and notes.
 
        super().__init__(parent)
        self.setWindowTitle(f"How to play : {song_name}")
        self.resize(500, 400)
        self.initUI(song_name, song_notes)
    
    def initUI(self, song_name, song_notes):
        # Builds the graphical interface for the cheat sheet window.
        layout = QVBoxLayout()
    
        title_label = QLabel(song_name)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instructions for the user
        instructions = QLabel("Follow the notes below to play this piece :")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setFont(QFont("Arial", 12))
        layout.addWidget(instructions)
        
        # Text area to display the notes
        notes_text = QTextEdit()
        notes_text.setReadOnly(True)
        notes_text.setFont(QFont("Arial", 14))
        
        # Format notes to highlight them
        formatted_notes = ""
        lines = song_notes.split('\n')
        for line in lines:
            notes = line.split()
            formatted_line = ""
            for note in notes:
                # Add formatting to each note
                if note == "Do":
                    formatted_line += "<span style='color: #FF5733; font-weight: bold;'>Do</span> "
                elif note == "Ré" or note == "Ré#":
                    formatted_line += "<span style='color: #FFC300; font-weight: bold;'>" + note + "</span> "
                elif note == "Mi":
                    formatted_line += "<span style='color: #DAF7A6; font-weight: bold;'>Mi</span> "
                elif note == "Fa" or note == "Fa#":
                    formatted_line += "<span style='color: #C70039; font-weight: bold;'>" + note + "</span> "
                elif note == "Sol" or note == "Sol#":
                    formatted_line += "<span style='color: #900C3F; font-weight: bold;'>" + note + "</span> "
                elif note == "La" or note == "La#":
                    formatted_line += "<span style='color: #581845; font-weight: bold;'>" + note + "</span> "
                elif note == "Si":
                    formatted_line += "<span style='color: #0000FF; font-weight: bold;'>Si</span> "
                else:
                    formatted_line += note + " "
            formatted_notes += formatted_line + "<br>"
        
        notes_text.setHtml(formatted_notes)
        notes_text.setStyleSheet("background-color: #f8f8f8; border: 1px solid #ddd; padding: 10px;")
        layout.addWidget(notes_text)
        

        tip_label = QLabel("Tip: Press the keys in the order shown. Notes with a ' are one octave higher.")
        tip_label.setStyleSheet("color: #555; font-style: italic;")
        layout.addWidget(tip_label)
        

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
        
        self.setLayout(layout)


class CheatSheetButton(QPushButton):
    # Button to display the cheat sheet for the piano
    def __init__(self, parent=None):
        super().__init__("Keystrokes", parent)
        self.setStyleSheet("background-color: #e6f7ff; border: 1px solid #99d6ff;")
        self.clicked.connect(self.show_cheatsheet_dialog)
        self.interactive_guide = None
        
    def show_cheatsheet_dialog(self):
        # Displays the cheat sheet dialog for the piano
        dialog = QDialog(self.parent())
        dialog.setWindowTitle("Piano help")
        dialog.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Instructions for the user
        instructions = QLabel("Select a song to learn :")
        instructions.setFont(QFont("Arial", 12))
        layout.addWidget(instructions)
        
        # Song selector
        song_selector = QComboBox()
        for song_name in SIMPLE_SONGS.keys():
            song_selector.addItem(song_name)
        song_selector.setStyleSheet("font-size: 12px; padding: 5px;")
        layout.addWidget(song_selector)
        
        # Help options
        help_options = QFrame()
        help_layout = QVBoxLayout(help_options)
        
        self.show_notes_radio = QPushButton("See notes")    
        self.show_notes_radio.setStyleSheet("text-align: left; padding: 10px;")
        help_layout.addWidget(self.show_notes_radio)
        
        self.interactive_radio = QPushButton("Interactive guide")
        self.interactive_radio.setStyleSheet("text-align: left; padding: 10px;")
        help_layout.addWidget(self.interactive_radio)
        
        layout.addWidget(help_options)
        

        buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        

        self.show_notes_radio.clicked.connect(lambda: self.show_song_notes(dialog, song_selector.currentText()))
        self.interactive_radio.clicked.connect(lambda: self.show_interactive_guide(dialog, song_selector.currentText()))
        
        dialog.exec_()
    
    def show_song_notes(self, parent_dialog, selected_song):
        parent_dialog.accept()
        if selected_song in SIMPLE_SONGS:
            song_notes = SIMPLE_SONGS[selected_song]
            cheatsheet = SongCheatSheetDialog(selected_song, song_notes, self.parent())
            cheatsheet.exec_()
    
    def show_interactive_guide(self, parent_dialog, selected_song):
        parent_dialog.accept()
        if selected_song in SIMPLE_SONGS:
            song_notes = SIMPLE_SONGS[selected_song]

            piano_widget = None
            parent = self.parent()
            while parent:
                if isinstance(parent, PianoWidget):
                    piano_widget = parent
                    break
                parent = parent.parent()
            
            if piano_widget:
                if self.interactive_guide:
                    self.interactive_guide.close()
                
                self.interactive_guide = InteractiveSongGuide(selected_song, song_notes, piano_widget)
                self.interactive_guide.show()


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
        

        key_displayed = ""
        for key, note_value in KEYBOARD_TO_NOTES.items():
            if note_value == self.note:
                key_displayed = KEY_NAMES.get(key, "")
                break

        if key_displayed:
            self.setText(f"{self.display_name}\n({key_displayed})")
        else:
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
    piano_key_to_note = KEYBOARD_TO_NOTES
    
    WHITE_NOTES = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si"]
    ENG_WHITE_NOTES = ["C", "D", "E", "F", "G", "A", "B"]

    BLACK_NOTES = ["Do#", "Ré#", "Fa#", "Sol#", "La#"]
    ENG_BLACK_NOTES = ["C#", "D#", "F#", "G#", "A#"]
    BLACK_POSITIONS = [0, 1, 3, 4, 5]
    
    def __init__(self, octaves=2, parent=None):
        # Configures the appearance of the key (color, text, style).
        # Also displays the associated keyboard key if available.
        super().__init__(parent)
        self.octaves = octaves
        self.music_player = MusicPlayer()
        self.recorder = get_recorder()
        self.white_keys = []
        self.black_keys = []
        self.is_playing_music = False
        self._init_ui()
        
    @property
    def all_keys(self):
        return self.white_keys + self.black_keys
    
    def play_piano_note(self, key):
        self._on_key_pressed(key.note)
        QTimer.singleShot(300, lambda: self._on_key_released(key.note))
    
    def _init_ui(self):
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        

        top_control_layout = QHBoxLayout()
        
        keyboard_info = QLabel("Use display keys to play")
        keyboard_info.setAlignment(Qt.AlignCenter)
        keyboard_info.setStyleSheet("background-color: #e6f7ff; padding: 5px; border-radius: 3px;")
        main_layout.addWidget(keyboard_info)
        

        info_layout = QVBoxLayout()
        self.status_label = QLabel("Piano ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.octaves_label = QLabel(f"Number of octaves: {self.octaves}")
        self.octaves_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.status_label)
        info_layout.addWidget(self.octaves_label)
    

        cheatsheet_button = CheatSheetButton(self)
        info_layout.addWidget(cheatsheet_button)
        
        top_control_layout.addLayout(info_layout)
        main_layout.addLayout(top_control_layout)



        self.piano_container = QFrame()
        self.piano_container.setFrameStyle(QFrame.StyledPanel)
        self.piano_container.setMinimumHeight(200)
        main_layout.addWidget(self.piano_container)

        self._create_keyboard()
        

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
    
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

                    for key in self.white_keys + self.black_keys:
                        if key.note == note:
                            key.set_pressed_style()
                            break
                    
                    frequency = note_to_frequency.get(note)
                    if frequency:
                        if isinstance(frequency, tuple):
                            frequency = frequency[0]
                        self.music_player.play_piano_tone(frequency, duration)
                    else:
                        time.sleep(duration)
                    

                    for key in self.white_keys + self.black_keys:
                        if key.note == note:
                            key.set_released_style()
                            break
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
    
    def keyPressEvent(self, event):
        print("Touche pressée :", event.key())
        key = event.key()
        if key in KEYBOARD_TO_NOTES:
            note = KEYBOARD_TO_NOTES[key]

            for key in self.white_keys + self.black_keys:
                if key.note == note:
                    self._on_key_pressed(note)
                    break
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        # Method called automatically when a keyboard key is released while the PianoWidget has the focus.
        # If the key corresponds to a note in the KEYBOARD_TO_NOTES dictionary,
        # the visual effect of the corresponding note is stopped.
        key = event.key() # Retrieves the code of the pressed key
        if key in KEYBOARD_TO_NOTES:
            note = KEYBOARD_TO_NOTES[key] # Retrieves the note associated with the released key
            self._on_key_released(note) # Stops the visual effect of the note
        super().keyReleaseEvent(event)  # Calls the parent class method to handle other events 
        
            
    def keyPressEvent(self, event):
        # Method called automatically when a keyboard key is pressed while the PianoWidget has the focus.
        # If the key corresponds to a note in the KEYBOARD_TO_NOTES dictionary,
        # the corresponding note is played (visual effect + sound).
        key = event.key() # Retrieves the code of the pressed key
        key = event.key()
        if key in KEYBOARD_TO_NOTES: # Retrieves the note associated with the pressed key
            note = KEYBOARD_TO_NOTES[key] # Plays the note (visual effect + sound)
            self._on_key_pressed(note) # Calls the parent class method to handle other events 
        super().keyPressEvent(event)
        
    def keyReleaseEvent(self, event):
        key = event.key()
        if key in KEYBOARD_TO_NOTES:
            note = KEYBOARD_TO_NOTES[key]
            self._on_key_released(note)
        super().keyReleaseEvent(event)


        
class InteractiveSongGuide(QWidget):

    
    def __init__(self, song_name, song_notes, piano_widget, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Guide interactif: {song_name}")
        self.song_name = song_name
        self.song_notes = self._parse_song_notes(song_notes)
        self.current_index = 0
        self.piano_widget = piano_widget
        self.initUI()
    
    def _parse_song_notes(self, song_notes):

        parsed_notes = []
        lines = song_notes.split('\n')
        for line in lines:
            notes = line.split()
            for note in notes:
                if note == "Do":
                    parsed_notes.append("C4")
                elif note == "Do#":
                    parsed_notes.append("C#4")
                elif note == "Ré":
                    parsed_notes.append("D4")
                elif note == "Ré#":
                    parsed_notes.append("D#4")
                elif note == "Mi":
                    parsed_notes.append("E4")
                elif note == "Fa":
                    parsed_notes.append("F4")
                elif note == "Fa#":
                    parsed_notes.append("F#4")
                elif note == "Sol":
                    parsed_notes.append("G4")
                elif note == "Sol#":
                    parsed_notes.append("G#4")
                elif note == "La":
                    parsed_notes.append("A4")
                elif note == "La#":
                    parsed_notes.append("A#4")
                elif note == "Si":
                    parsed_notes.append("B4")
                elif note == "Do'":  
                    parsed_notes.append("C5")
                elif note == "Ré'":
                    parsed_notes.append("D5")
                elif note == "Mi'":
                    parsed_notes.append("E5")
        return parsed_notes
    
    def initUI(self):
        layout = QVBoxLayout()
        

        title = QLabel(self.song_name)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        

        self.progress_label = QLabel(f"Note: 1/{len(self.song_notes)}")
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)
        

        self.current_note_label = QLabel("")
        self.current_note_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.current_note_label.setAlignment(Qt.AlignCenter)
        self.current_note_label.setStyleSheet("background-color: #e6f7ff; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.current_note_label)
        

        nav_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_note)
        nav_layout.addWidget(self.prev_button)
        
        self.play_button = QPushButton("Play this note")
        self.play_button.clicked.connect(self.play_current_note)
        self.play_button.setStyleSheet("background-color: #4CAF50; color: white;")
        nav_layout.addWidget(self.play_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_note)
        nav_layout.addWidget(self.next_button)
        
        layout.addLayout(nav_layout)
        

        self.play_all_button = QPushButton("Play the whole song")
        self.play_all_button.clicked.connect(self.play_all_notes)
        self.play_all_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        layout.addWidget(self.play_all_button)
        
        self.setLayout(layout)
        self.update_current_note()
    
    def update_current_note(self):
        if 0 <= self.current_index < len(self.song_notes):
            note = self.song_notes[self.current_index]

            display_note = note
            if note.startswith("C"):
                display_note = "Do" + ("'" if note.endswith("5") else "")
            elif note.startswith("D"):
                display_note = "Ré" + ("'" if note.endswith("5") else "")
            elif note.startswith("E"):
                display_note = "Mi" + ("'" if note.endswith("5") else "")
            elif note.startswith("F"):
                display_note = "Fa" + ("'" if note.endswith("5") else "")
            elif note.startswith("G"):
                display_note = "Sol" + ("'" if note.endswith("5") else "")
            elif note.startswith("A"):
                display_note = "La" + ("'" if note.endswith("5") else "")
            elif note.startswith("B"):
                display_note = "Si" + ("'" if note.endswith("5") else "")
            
            self.current_note_label.setText(display_note)
            self.progress_label.setText(f"Note: {self.current_index + 1}/{len(self.song_notes)}")
            

            self.prev_button.setEnabled(self.current_index > 0)
            self.next_button.setEnabled(self.current_index < len(self.song_notes) - 1)
            
    def next_note(self):
        if self.current_index < len(self.song_notes) - 1:
            self.current_index += 1
            self.update_current_note()
    
    def previous_note(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_current_note()
    
    def play_current_note(self):
        if 0 <= self.current_index < len(self.song_notes):
            note = self.song_notes[self.current_index]

            self.piano_widget._on_key_pressed(note)

            QTimer.singleShot(300, lambda: self.piano_widget._on_key_released(note))
    
    def play_all_notes(self):
        notes_with_duration = [(note, 0.5) for note in self.song_notes]
        self.piano_widget.play_music(notes_with_duration)