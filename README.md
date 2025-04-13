# Log Analyzer Tool

A simple Python tool for analyzing log files.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python main.py /path/to/logfile.log
```

Show statistics:
```bash
python main.py /path/to/logfile.log --stats
```

Specify log type:
```bash
python main.py /path/to/access.log --type nginx
```

Filter by log level:
```bash
python main.py /path/to/logfile.log --filter-level ERROR
```

Export results:
```bash
python main.py /path/to/logfile.log --export json
python main.py /path/to/logfile.log --export csv
```

## Supported Log Types

- generic (default) - Basic log parsing
- nginx - Nginx access logs  
- apache - Apache access logs

## Features

- Parse log files and extract key information
- Count log entries by severity level
- Display recent log entries
- Basic timestamp extraction
- Filter logs by severity level
- Export results to JSON or CSV format
- Nginx access log analysis with IP and status code statistics