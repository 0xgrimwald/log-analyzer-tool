import re
from datetime import datetime
from collections import defaultdict

class LogParser:
    def __init__(self, log_type='generic'):
        self.log_type = log_type
        self.stats = defaultdict(int)
        
    def parse_file(self, filename):
        lines = []
        try:
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    entry = self._parse_line(line.strip(), line_num)
                    if entry:
                        lines.append(entry)
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
            
        return lines
    
    def _parse_line(self, line, line_num):
        if not line:
            return None
            
        entry = {
            'line_number': line_num,
            'raw': line,
            'timestamp': None,
            'level': 'INFO',
            'message': line
        }
        
        # Try to extract timestamp
        timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
        if timestamp_match:
            try:
                entry['timestamp'] = datetime.strptime(timestamp_match.group(), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
        
        # Try to extract log level
        level_match = re.search(r'\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\b', line, re.IGNORECASE)
        if level_match:
            entry['level'] = level_match.group().upper()
            
        self.stats[entry['level']] += 1
        
        return entry
    
    def get_stats(self):
        return dict(self.stats)