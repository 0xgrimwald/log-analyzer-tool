import json
import os

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.default_config = {
            'max_lines_display': 5,
            'default_export_format': 'json',
            'timestamp_formats': [
                '%Y-%m-%d %H:%M:%S',
                '%d/%b/%Y:%H:%M:%S',
                '%b %d %H:%M:%S'
            ],
            'log_levels': ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL']
        }
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    config = self.default_config.copy()
                    config.update(user_config)
                    return config
            except (json.JSONDecodeError, IOError):
                print(f"Warning: Could not load {self.config_file}, using defaults")
        
        return self.default_config.copy()
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config: {e}")
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value