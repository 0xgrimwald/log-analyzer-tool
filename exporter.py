import json
import csv
from datetime import datetime

class LogExporter:
    def __init__(self):
        pass
    
    def export_to_json(self, entries, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"log_analysis_{timestamp}.json"
        
        # Convert datetime objects to strings for JSON serialization
        export_data = []
        for entry in entries:
            export_entry = entry.copy()
            if export_entry.get('timestamp'):
                export_entry['timestamp'] = export_entry['timestamp'].isoformat()
            export_data.append(export_entry)
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"Exported {len(entries)} entries to {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return None
    
    def export_to_csv(self, entries, filename=None):
        if not entries:
            print("No data to export")
            return None
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"log_analysis_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as f:
                # Get all possible field names
                fieldnames = set()
                for entry in entries:
                    fieldnames.update(entry.keys())
                fieldnames = sorted(list(fieldnames))
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for entry in entries:
                    export_entry = entry.copy()
                    # Convert datetime to string
                    if export_entry.get('timestamp'):
                        export_entry['timestamp'] = export_entry['timestamp'].isoformat()
                    writer.writerow(export_entry)
            
            print(f"Exported {len(entries)} entries to {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None