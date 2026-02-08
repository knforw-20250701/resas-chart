#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import io

# Force UTF-8 for consistency
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_log():
    result = subprocess.run(['git', 'log', '--pretty=format:%h | %s', '-n', '10'], 
                            capture_output=True, check=True)
    # Git log output might be UTF-8
    return result.stdout.decode('utf-8', errors='replace')

if __name__ == "__main__":
    print("--- Current Git Log ---")
    print(get_log())
