import os

class MusicParser:

    def __init__(self):
        self.notes = []
        
    def parse_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Error: File not found: {file_path}")
                return []
            
            self.notes = []

            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        parts = line.split()
                        if len(parts) != 2:
                            print(f"Warning: Invalid format at line {line_number}: {line}")
                            continue
                        
                        note = parts[0]
                        duration = float(parts[1])
                        
                        if duration <= 0:
                            print(f"Warning: Invalid duration at line {line_number}: {duration}")
                            continue
                        
                        self.notes.append((note, duration))
                        
                    except ValueError as e:
                        print(f"Warning: Error parsing line {line_number}: {line} - {e}")
                        continue
            
            print(f"Successfully parsed {len(self.notes)} notes from {file_path}")
            return self.notes
            
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return []
    
    def get_total_duration(self):
        return sum(duration for _, duration in self.notes)
    
    def get_notes(self):
        return self.notes
    
    def filter_for_instrument(self, instrument_type):
        return self.notes

_instance = None

def get_music_parser():
    global _instance
    if _instance is None:
        _instance = MusicParser()
    return _instance

if __name__ == "__main__":
    parser = get_music_parser()
    notes = parser.parse_file("../assets/bella_ciao.txt")
    
    if notes:
        print("First 5 notes:")
        for i, (note, duration) in enumerate(notes[:5]):
            print(f"Note {i+1}: {note}, Duration: {duration}s")
        print(f"Total music duration: {parser.get_total_duration():.2f} seconds")