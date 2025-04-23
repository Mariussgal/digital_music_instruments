import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QFileDialog, 
                            QSpinBox, QLabel, QVBoxLayout, QHBoxLayout, 
                            QWidget, QToolBar, QStatusBar, QStackedWidget)
from PyQt5.QtCore import QSize

from core.settings import get_settings
from core.music_parser import get_music_parser
from core.recorder import get_recorder

from ui.piano_widget import PianoWidget
from ui.xylophone_widget import XylophoneWidget
from ui.videogame_widget import VideogameWidget


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.settings = get_settings()
        self.music_parser = get_music_parser()
        self.recorder = get_recorder()
        self.setWindowTitle("Digital Musical Instruments")
        self.setMinimumSize(800, 500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self._create_actions()
        self._create_menus()
        self._create_toolbar()
        self._create_status_bar()
        self._create_controls()
        self._create_instrument_widgets()
        self._set_current_instrument(self.settings.get_instrument())
        self.status_bar.showMessage("Ready")
    
    def _create_actions(self):

        self.open_action = QAction("Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open a music file")
        self.open_action.triggered.connect(self._open_file)

        self.record_action = QAction("Record", self)
        self.record_action.setShortcut("Ctrl+R")
        self.record_action.setStatusTip("Start recording")
        self.record_action.triggered.connect(self._toggle_recording)
        
        self.stop_action = QAction("Stop", self)
        self.stop_action.setShortcut("Ctrl+S")
        self.stop_action.setStatusTip("Stop recording")
        self.stop_action.setEnabled(False) 
        self.stop_action.triggered.connect(self._stop_recording)
        
        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.setStatusTip("Quit application")
        self.quit_action.triggered.connect(self.close)
        
        self.piano_action = QAction("Piano", self)
        self.piano_action.setStatusTip("Switch to Piano")
        self.piano_action.setCheckable(True)
        self.piano_action.triggered.connect(lambda: self._set_current_instrument("piano"))
        
        self.xylophone_action = QAction("Xylophone", self)
        self.xylophone_action.setStatusTip("Switch to Xylophone")
        self.xylophone_action.setCheckable(True)
        self.xylophone_action.triggered.connect(lambda: self._set_current_instrument("xylophone"))
        
        self.videogame_action = QAction("Video Game", self)
        self.videogame_action.setStatusTip("Switch to Video Game instrument")
        self.videogame_action.setCheckable(True)
        self.videogame_action.triggered.connect(lambda: self._set_current_instrument("videogame"))
    
    def _create_menus(self):

        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.record_action)
        self.file_menu.addAction(self.stop_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_action)
        
        self.instrument_menu = self.menuBar().addMenu("Instrument")
        self.instrument_menu.addAction(self.piano_action)
        self.instrument_menu.addAction(self.xylophone_action)
        self.instrument_menu.addAction(self.videogame_action)
    
    def _create_toolbar(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)
        
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.record_action)
        self.toolbar.addAction(self.stop_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.piano_action)
        self.toolbar.addAction(self.xylophone_action)
        self.toolbar.addAction(self.videogame_action)
    
    def _create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
    
    def _create_controls(self):
        controls_layout = QHBoxLayout()
        
        self.octaves_label = QLabel("Number of octaves:")
        self.octaves_spinbox = QSpinBox()
        self.octaves_spinbox.setRange(1, 3)
        self.octaves_spinbox.setValue(self.settings.get_octaves())
        self.octaves_spinbox.valueChanged.connect(self._on_octaves_changed)
        
        controls_layout.addWidget(self.octaves_label)
        controls_layout.addWidget(self.octaves_spinbox)
        controls_layout.addStretch()
        
        self.main_layout.addLayout(controls_layout)
    
    def _create_instrument_widgets(self):
        self.instruments_stack = QStackedWidget()

        self.piano_widget = PianoWidget(octaves=self.settings.get_octaves())
        self.xylophone_widget = XylophoneWidget()
        self.videogame_widget = VideogameWidget()

        self.instruments_stack.addWidget(self.piano_widget)
        self.instruments_stack.addWidget(self.xylophone_widget)
        self.instruments_stack.addWidget(self.videogame_widget)
        
        self.main_layout.addWidget(self.instruments_stack)
    
    def _set_current_instrument(self, instrument):

        self.settings.set_instrument(instrument)

        self.piano_action.setChecked(instrument == "piano")
        self.xylophone_action.setChecked(instrument == "xylophone")
        self.videogame_action.setChecked(instrument == "videogame")

        self.octaves_label.setVisible(instrument == "piano")
        self.octaves_spinbox.setVisible(instrument == "piano")

        if instrument == "piano":
            self.instruments_stack.setCurrentWidget(self.piano_widget)
        elif instrument == "xylophone":
            self.instruments_stack.setCurrentWidget(self.xylophone_widget)
        else: 
            self.instruments_stack.setCurrentWidget(self.videogame_widget)

        self.status_bar.showMessage(f"Switched to {instrument.capitalize()}")
    
    def _on_octaves_changed(self, value):

        self.settings.set_octaves(value)
        self.piano_widget.set_octaves(value)
        self.status_bar.showMessage(f"Changed to {value} octaves")
    
    def _open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Music File", "","Text Files (*.txt);;All Files (*)")
        
        if file_path:
            notes = self.music_parser.parse_file(file_path)
            
            if notes:
                current_widget = self.instruments_stack.currentWidget()
                current_widget.play_music(notes)
                self.status_bar.showMessage(f"Playing music from {os.path.basename(file_path)}")
            else:
                self.status_bar.showMessage("Error loading music file")
    
    def _toggle_recording(self):
        if not self.recorder.is_currently_recording():
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Recording As", f"recordings/{self.recorder.get_default_filename()}", "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            if self.recorder.start_recording(file_path):
                self.record_action.setText("Recording...")
                self.record_action.setStatusTip("Recording in progress")
                self.stop_action.setEnabled(True)
                self.status_bar.showMessage(f"Recording to {os.path.basename(file_path)}")
                current_widget = self.instruments_stack.currentWidget()
                current_widget.recording_started()
    
    def _stop_recording(self):
        if self.recorder.is_currently_recording():
            if self.recorder.stop_recording():
                self.status_bar.showMessage(f"Recording saved to {os.path.basename(self.recorder.output_file)}")
            else:
                self.status_bar.showMessage("Recording stopped (no notes recorded)")

            self.record_action.setText("Record")
            self.record_action.setStatusTip("Start recording")
            self.stop_action.setEnabled(False)
            
            current_widget = self.instruments_stack.currentWidget()
            current_widget.recording_stopped()
    
    def closeEvent(self, event):
        if self.recorder.is_currently_recording():
            self.recorder.stop_recording()
        
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())