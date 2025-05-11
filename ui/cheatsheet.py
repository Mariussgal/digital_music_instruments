from PyQt5.QtWidgets import QPushButton, QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Ajoutez ce dictionnaire au début de votre fichier, par exemple juste après les imports
SIMPLE_SONGS = {
    "Au Clair de la Lune": """Do Do Do Ré
Mi Ré Do Mi
Ré Ré Do""",

    "Frère Jacques": """Do Ré Mi Do
Do Ré Mi Do
Mi Fa Sol
Mi Fa Sol""",

    "Joyeux Anniversaire": """Do Do Ré Do Fa Mi
Do Do Ré Do Sol Fa""",
    
    "Twinkle Twinkle": """Do Do Sol Sol La La Sol
Fa Fa Mi Mi Ré Ré Do"""
}

# Ajoutez ces classes à votre fichier
class SongCheatSheetDialog(QDialog):
    """Fenêtre de dialogue montrant les antisèches pour jouer une chanson"""
    
    def __init__(self, song_name, song_notes, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Comment jouer : {song_name}")
        self.resize(400, 300)
        self.initUI(song_name, song_notes)
    
    def initUI(self, song_name, song_notes):
        layout = QVBoxLayout()
        
        # Titre
        title_label = QLabel(song_name)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instructions
        instructions = QLabel("Suivez les notes ci-dessous pour jouer ce morceau :")
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Notes
        notes_text = QTextEdit()
        notes_text.setReadOnly(True)
        notes_text.setFont(QFont("Arial", 12))
        notes_text.setPlainText(song_notes)
        notes_text.setStyleSheet("background-color: #f8f8f8; border: 1px solid #ddd;")
        layout.addWidget(notes_text)
        
        # Bouton pour fermer
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
        
        self.setLayout(layout)


# MÉTHODE 1: Ajoutez cette fonction à votre classe PianoWidget existante
def add_cheatsheet_button(self):
    """
    Ajoute un bouton d'antisèches à l'interface du piano.
    Appelez cette fonction depuis votre __init__ ou après avoir configuré l'interface principale
    """
    # Créer le bouton d'antisèches
    cheatsheet_button = QPushButton("Antisèches", self)
    cheatsheet_button.setStyleSheet("background-color: #e6f7ff; border: 1px solid #99d6ff;")
    cheatsheet_button.clicked.connect(self.show_cheatsheet_dialog)
    
    # Ajouter le bouton au layout (si votre classe a un layout)
    if hasattr(self, 'layout') and self.layout() is not None:
        self.layout().addWidget(cheatsheet_button)
    else:
        # Si pas de layout, on positionne manuellement le bouton
        # Ajustez ces valeurs selon votre interface
        cheatsheet_button.setFixedSize(120, 30)
        cheatsheet_button.move(10, 10)

def show_cheatsheet_dialog(self):
    """
    Affiche la boîte de dialogue pour sélectionner une chanson
    """
    # Créer un dialogue pour sélectionner la chanson
    dialog = QDialog(self)
    dialog.setWindowTitle("Antisèches de piano")
    dialog.resize(300, 200)
    
    layout = QVBoxLayout()
    
    # Instructions
    instructions = QLabel("Sélectionnez un morceau à apprendre :")
    layout.addWidget(instructions)
    
    # Sélecteur de chanson
    song_selector = QComboBox()
    for song_name in SIMPLE_SONGS.keys():
        song_selector.addItem(song_name)
    layout.addWidget(song_selector)
    
    # Boutons
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    
    dialog.setLayout(layout)
    
    # Montrer le dialogue
    if dialog.exec_() == QDialog.Accepted:
        selected_song = song_selector.currentText()
        if selected_song in SIMPLE_SONGS:
            song_notes = SIMPLE_SONGS[selected_song]
            cheatsheet = SongCheatSheetDialog(selected_song, song_notes, self)
            cheatsheet.exec_()


# MÉTHODE 2: Si vous préférez une approche plus directe sans modifier votre classe PianoWidget,
# vous pouvez appeler cette fonction en passant votre widget piano comme paramètre

def add_cheatsheet_button_to_piano(piano_widget):
    """
    Ajoute un bouton d'antisèches à un widget piano existant.
    Appelez cette fonction après avoir créé votre objet PianoWidget
    """
    # Créer le bouton d'antisèches
    cheatsheet_button = QPushButton("Antisèches", piano_widget)
    cheatsheet_button.setStyleSheet("background-color: #e6f7ff; border: 1px solid #99d6ff;")
    
    # Définir la fonction de callback
    def show_dialog():
        # Créer un dialogue pour sélectionner la chanson
        dialog = QDialog(piano_widget)
        dialog.setWindowTitle("Antisèches de piano")
        dialog.resize(300, 200)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("Sélectionnez un morceau à apprendre :")
        layout.addWidget(instructions)
        
        # Sélecteur de chanson
        song_selector = QComboBox()
        for song_name in SIMPLE_SONGS.keys():
            song_selector.addItem(song_name)
        layout.addWidget(song_selector)
        
        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        # Montrer le dialogue
        if dialog.exec_() == QDialog.Accepted:
            selected_song = song_selector.currentText()
            if selected_song in SIMPLE_SONGS:
                song_notes = SIMPLE_SONGS[selected_song]
                cheatsheet = SongCheatSheetDialog(selected_song, song_notes, piano_widget)
                cheatsheet.exec_()
    
    # Connecter le bouton à la fonction
    cheatsheet_button.clicked.connect(show_dialog)
    
    # Ajouter le bouton au layout ou le positionner manuellement
    if piano_widget.layout() is not None:
        piano_widget.layout().addWidget(cheatsheet_button)
    else:
        # Positionnement manuel - ajustez ces valeurs selon votre interface
        cheatsheet_button.setFixedSize(120, 30)
        cheatsheet_button.move(10, 10)
    
    return cheatsheet_button