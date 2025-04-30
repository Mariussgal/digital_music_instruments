# **🎹 Digital Musical Instruments**

**📚 Overview**
As part of an academic assignment I had to build a digital music application developed with PyQt5, allowing users to play different virtual instruments.

**🚀 Features**
* Play multiple digital instruments (Piano, Xylophone, Video Game sounds)
* Customize number of octaves (1-3)
* Record and save musical compositions
* Play musical scores from files
* Visual feedback when pressing keys/notes
* Volume control for all instruments
* Settings persistence between sessions

**🎵 Instruments**
The application includes three different instruments:
1. **Classical Piano**: Traditional keyboard with white and black keys
2. **Colorful Xylophone**: With rainbow-colored bars
3. **Video Game**: 8-bit sounds with colorful interface

**🧰 Requirements**
* Python 3.6+
* PyQt5
* Pygame
* NumPy
* SciPy

**🛠️ Installation**
1. Clone the repository
```
git clone https://github.com/Mariussgal/digital_music_instruments.git
cd digital-musical-instruments
```

2. Install required dependencies
```
pip install PyQt5 pygame numpy scipy
```

**▶️ Usage**
Run the main script to launch the application:
```
python main.py
```

**📋 Menu Options**
* **File**: Open music scores, Record, Stop recording, Quit
* **Instrument**: Select between different instruments
* **Help**: About information

**🗂️ Project Structure**
```
project-root/
│
├── main.py                    # Application entry point
├── instruments.py             # Sound and frequency management
├── settings.json              # init settings for instruments
│
├── core/                      # Core modules
│   ├── __init__.py
│   ├── settings.py            # Settings management
│   ├── music_parser.py        # Score file parsing
│   └── recorder.py            # Note recording
│
├── ui/                        # User interface
    ├── __init__.py
    ├── main_window.py         # Main window
    ├── piano_widget.py        # Piano instrument
    ├── xylophone_widget.py    # Xylophone instrument
    ├── videogame_widget.py    # Video game instrument
```

**🔧 Key Functions**
* `play_piano_tone()`: Generate piano sound
* `play_xylophone_tone()`: Generate xylophone sound
* `play_videoGame_tone()`: Generate 8-bit sound
* `parse_file()`: Read music score files
* `record_note()`: Save notes during recording
* `set_octaves()`: Change instrument octave range
* `play_music()`: Play a sequence of notes from a file

**🎯 Learning Objectives**
* Design interactive user interfaces with PyQt5
* Implement sound generation and processing
* Create a modular, maintainable application structure
* Apply object-oriented programming concepts

**🎼 Music Score Format**
Music scores are simple text files with one note per line:
```
C4
D4
E4
F4
G4
```

**🤝 Contributing**
Contributions, issues, and feature requests are welcome! Feel free to fork the repo and submit a pull request.
