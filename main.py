#!/usr/bin/env python3

import sys
import argparse
from parser import LogParser

def main():
    parser = argparse.ArgumentParser(description='Log Analyzer Tool')
    parser.add_argument('logfile', help='Path to log file')
    parser.add_argument('-t', '--type', choices=['nginx', 'apache', 'generic'], 
                       default='generic', help='Log file type')
    parser.add_argument('-s', '--stats', action='store_true',
                       help='Show statistics summary')
    
    args = parser.parse_args()
    
    print(f"Analyzing {args.logfile} as {args.type} log...")
    
    log_parser = LogParser(args.type)
    entries = log_parser.parse_file(args.logfile)
    
    if not entries:
        print("No valid log entries found.")
        return
    
    print(f"\nParsed {len(entries)} log entries")
    
    if args.stats:
        stats = log_parser.get_stats()
        print("\nLog Level Statistics:")
        for level, count in sorted(stats.items()):
            print(f"  {level}: {count}")
    
    # Show recent entries
    print(f"\nLast 5 entries:")
    for entry in entries[-5:]:
        print(f"  Line {entry['line_number']}: [{entry['level']}] {entry['message'][:80]}...")
    
if __name__ == '__main__':
    main()