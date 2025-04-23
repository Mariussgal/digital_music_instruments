import os
import json

class Settings:
    
    DEFAULT_OCTAVES = 2
    DEFAULT_INSTRUMENT = "piano"
    OCTAVES_KEY = "octaves"
    INSTRUMENT_KEY = "instrument"


    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.settings = {
            self.OCTAVES_KEY: self.DEFAULT_OCTAVES,
            self.INSTRUMENT_KEY: self.DEFAULT_INSTRUMENT
        }
        self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as file:
                    loaded_settings = json.load(file)
                    self.settings.update(loaded_settings)
                    self._validate_settings()
                    print(f"Parameters loaded from {self.settings_file}")
            else:
                print(f"Configuration file not found. defaut values used.")
        except Exception as e:
            print(f"Error while loading settings: {e}")
            print("Using default values.")

    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as file:
                json.dump(self.settings, file, indent=4)
                print(f"Parameters savec in {self.settings_file}")
        except Exception as e:
            print(f"Error while saving parameters: {e}")

    def _validate_settings(self):
    
        if self.OCTAVES_KEY in self.settings:
            octaves = self.settings[self.OCTAVES_KEY]
            if not isinstance(octaves, int) or octaves < 1 or octaves > 3:
                self.settings[self.OCTAVES_KEY] = self.DEFAULT_OCTAVES
    
    
        if self.INSTRUMENT_KEY in self.settings:
            instrument = self.settings[self.INSTRUMENT_KEY]
            valid_instruments = ["piano", "xylophone", "videogame"]
            if instrument not in valid_instruments:
                self.settings[self.INSTRUMENT_KEY] = self.DEFAULT_INSTRUMENT

    def get_octaves(self):
        return self.settings.get(self.OCTAVES_KEY, self.DEFAULT_OCTAVES)

    def set_octaves(self, octaves):
        if not isinstance(octaves, int) or octaves < 1 or octaves > 3:
            print(f"Invalid octave number: {octaves}")
            return False
 
        self.settings[self.OCTAVES_KEY] = octaves
        self.save_settings()
        return True

    def get_instrument(self):
        return self.settings.get(self.INSTRUMENT_KEY, self.DEFAULT_INSTRUMENT)

    def set_instrument(self, instrument):
        valid_instruments = ["piano", "xylophone", "videogame"]
        if instrument not in valid_instruments:
            print(f"Invalid instrument: {instrument}")
            return False

        self.settings[self.INSTRUMENT_KEY] = instrument
        self.save_settings()
        return True

_instance = None

def get_settings():
    global _instance
    if _instance is None:
        _instance = Settings()
    return _instance

if __name__ == "__main__":
    settings = get_settings()
    
    print(f"Octave number: {settings.get_octaves()}")
    print(f"Instrument: {settings.get_instrument()}")
    
    settings.set_octaves(3)
    settings.set_instrument("xylophone")
    
    print(f"New settings - Octaves: {settings.get_octaves()}, Instrument: {settings.get_instrument()}")