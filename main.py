#!/usr/bin/env python3

import sys
import argparse
from parser import LogParser
from nginx_parser import NginxParser

def main():
    parser = argparse.ArgumentParser(description='Log Analyzer Tool')
    parser.add_argument('logfile', help='Path to log file')
    parser.add_argument('-t', '--type', choices=['nginx', 'apache', 'generic'], 
                       default='generic', help='Log file type')
    parser.add_argument('-s', '--stats', action='store_true',
                       help='Show statistics summary')
    
    args = parser.parse_args()
    
    print(f"Analyzing {args.logfile} as {args.type} log...")
    
    if args.type == 'nginx':
        log_parser = NginxParser()
        entries = log_parser.parse_file(args.logfile)
        
        if not entries:
            print("No valid log entries found.")
            return
        
        print(f"\nParsed {len(entries)} nginx log entries")
        
        if args.stats:
            stats = log_parser.get_stats()
            print(f"\nNginx Log Statistics:")
            print(f"  Total requests: {stats['total_requests']}")
            print(f"  Unique IPs: {stats['unique_ips']}")
            print(f"\n  Top IPs:")
            for ip, count in list(stats['top_ips'].items())[:5]:
                print(f"    {ip}: {count} requests")
            print(f"\n  Status codes:")
            for status, count in sorted(stats['status_codes'].items()):
                print(f"    {status}: {count}")
        
        # Show recent entries
        print(f"\nLast 5 entries:")
        for entry in entries[-5:]:
            print(f"  {entry['ip']} - {entry['method']} {entry['url']} - {entry['status']}")
    else:
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