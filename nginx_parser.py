import re
from datetime import datetime
from collections import defaultdict

class NginxParser:
    def __init__(self):
        self.stats = defaultdict(int)
        self.ip_stats = defaultdict(int)
        self.status_stats = defaultdict(int)
        
        # Common nginx log format pattern
        self.log_pattern = re.compile(
            r'(?P<ip>[\d.]+)\s+-\s+-\s+'
            r'\[(?P<timestamp>[^\]]+)\]\s+'
            r'"(?P<method>\w+)\s+(?P<url>\S+)\s+HTTP/[\d.]+"\s+'
            r'(?P<status>\d+)\s+'
            r'(?P<size>\d+)\s+'
            r'"(?P<referer>[^"]*)"\s+'
            r'"(?P<user_agent>[^"]*)"'
        )
    
    def parse_file(self, filename):
        entries = []
        try:
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    entry = self._parse_line(line.strip(), line_num)
                    if entry:
                        entries.append(entry)
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
            
        return entries
    
    def _parse_line(self, line, line_num):
        if not line:
            return None
            
        match = self.log_pattern.match(line)
        if not match:
            # Fallback for non-standard format
            return {
                'line_number': line_num,
                'raw': line,
                'ip': 'unknown',
                'timestamp': None,
                'method': 'unknown',
                'url': 'unknown',
                'status': '000',
                'size': 0
            }
        
        groups = match.groupdict()
        
        # Parse timestamp
        timestamp = None
        try:
            timestamp = datetime.strptime(groups['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
        except ValueError:
            try:
                # Try without timezone
                timestamp = datetime.strptime(groups['timestamp'][:20], '%d/%b/%Y:%H:%M:%S')
            except ValueError:
                pass
        
        entry = {
            'line_number': line_num,
            'raw': line,
            'ip': groups['ip'],
            'timestamp': timestamp,
            'method': groups['method'],
            'url': groups['url'],
            'status': groups['status'],
            'size': int(groups['size']) if groups['size'].isdigit() else 0,
            'referer': groups['referer'],
            'user_agent': groups['user_agent']
        }
        
        # Update statistics
        self.ip_stats[entry['ip']] += 1
        self.status_stats[entry['status']] += 1
        
        return entry
    
    def get_stats(self):
        return {
            'total_requests': sum(self.ip_stats.values()),
            'unique_ips': len(self.ip_stats),
            'top_ips': dict(sorted(self.ip_stats.items(), key=lambda x: x[1], reverse=True)[:10]),
            'status_codes': dict(self.status_stats)
        }