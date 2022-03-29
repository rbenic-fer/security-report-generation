#!/usr/bin/env python3

#import chardet
import sys

def readline_safe():
    line = None
    while line == None:
        try:
            line = sys.stdin.readline()
        except:
            pass
    return line

def main():
    line = readline_safe()
    while line:
        if not line.startswith('CVE-') or line.split(',')[1] != 'Entry':
            line = readline_safe()
            continue
        desc_begin = line.find('\"') + 1
        desc_len = line[desc_begin:].find('\"')
        while line[desc_begin + desc_len:desc_begin + desc_len + 2] == '\"\"':
            desc_len += line[desc_begin + desc_len + 2:].find('\"') + 2
        print(line[desc_begin:desc_begin + desc_len].replace('\"\"', '\"'))
        print()
        line = readline_safe()

main()
