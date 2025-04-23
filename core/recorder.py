import os
import time
from datetime import datetime

class Recorder: 

    def __init__(self):
        self.is_recording = False
        self.notes = []
        self.start_time = None
        self.last_note_time = None
        self.output_file = None

    def start_recording(self, output_file):
        try:
            if self.is_recording:
                print("Already recording. Stop the current recording first.")
                return False
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            self.is_recording = True
            self.notes = []
            self.start_time = time.time()
            self.last_note_time = self.start_time  
            self.output_file = output_file

            print(f"Started recording to {output_file}")
            return True

        except Exception as e:
            print(f"Error starting recording: {e}")
            self.is_recording = False
            return False

    def stop_recording(self):
        try : 
            if not self.is_recording:
                print("Not currently recording.")
                return False
            
            self.is_recording = False

            if self.notes:
                self._save_recording()
                print(f"Recording saved to {self.output_file}")
                return True
            else:
                print("No notes were recorded.")
                return False
            
        except Exception as e: 
            print(f"Error stopping recording: {e}")
            self.is_recording = False
            return False
    
    def add_note(self, note, duration=None):
        try:
            if not self.is_recording:
                print("Not currently recording. Start recording first.")
                return False
            
            current_time = time.time()

            if duration is None:
                duration = current_time - self.last_note_time
                duration = round(duration, 3)
            
            self.notes.append((note, duration))
            self.last_note_time = current_time
            print(f"Added note: {note}, duration: {duration}")
            return True
        except Exception as e:
            print(f"Error adding note: {e}")
            return False
    
    def _save_recording(self):
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                for note, duration in self.notes:
                    file.write(f"{note} {duration}\n")
            return True
        except Exception as e:
            print(f"Error saving recording: {e}")
            return False
    
    def is_currently_recording(self):
        return self.is_recording
    
    def get_recording_duration(self):
        if not self.is_recording:
            return 0
        
        return time.time() - self.start_time
    
    def get_default_filename(self):
        timestamp = f"{datetime.now().year}{datetime.now().month:02d}{datetime.now().day:02d}_{datetime.now().hour:02d}{datetime.now().minute:02d}{datetime.now().second:02d}"
        return f"recording_{timestamp}.txt"

_instance = None

def get_recorder():
    global _instance
    if _instance is None:
        _instance = Recorder()
    return _instance

if __name__ == "__main__":
    recorder = get_recorder()
    recorder.start_recording("test_recording.txt")
    
    recorder.add_note("C4", 0.5)
    time.sleep(0.5)

    recorder.add_note("E4", 0.3)
    time.sleep(0.3)

    recorder.add_note("G4", 0.7)
    time.sleep(0.7)

    recorder.stop_recording()
    print("Example recording completed.")