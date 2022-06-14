#!/usr/bin/env python3

import sys

def page_number(s):
    for ch in s:
        if ch < '0' or ch > '9':
            return False
    return True

def numeric(s):
    for ch in s:
        if ch != '.' and ch != '(' and ch != ')' and (ch < '0' or ch > '9'):
            return False
    return True

def alphanum(s):
    for ch in s:
        if ch != '.' and (ch < '0' or ch > '9') and (ch < 'A' or ch > 'Z') and (ch < 'a' or ch > 'z'):
            return False
    return True

remove_strings = ['' + str(i) + ' of 57' for i in range(1, 58)] + ['© SANS Institute 2005', 'Author retains full rights']

lines = sys.stdin.read().splitlines()

blank = False
prefix = ''
sentence = ''
for line in lines:
    line = line.strip()
    line = line.replace('•', '-')
    line = line.replace('–', '-')
    while line.find('....') != -1:
        line = line.replace('....', '...')
    while line.find('……') != -1:
        line = line.replace('……', '…')
    for s in remove_strings:
        while line.find(s) != -1:
            line = line.replace(s, '')
    if len(line) > 0 and alphanum(line) and not page_number(line) and (numeric(line) or len(line) < 5):
        if len(sentence) >= 80 and sentence[0] >= 'A' and sentence[0] <= 'Z':
            if blank:
                print()
            else:
                blank = True
            if len(prefix) > 0:
                print(prefix, sentence)
                prefix = ''
            else:
                print(sentence)
        sentence = ''
        #prefix = line
        #if len(prefix) > 0:
        #    prefix += ' '
        #prefix += line
        #if numeric(line) and line[-1] != '.':
        #    prefix += '.'
    else:
        if len(line) < 5:
            blank = True
        else:
            if (line[0] >= 'a' and line[0] <= 'z') or (len(prefix) == 0 and len(sentence) > 0 and sentence[-1] != '.') and line[:7] != 'Chapter' and line[:8] != 'Appendix' and line[:4] != 'Item':
                if len(sentence) > 0:
                    sentence += ' '
                sentence += line
            else:
                if len(sentence) >= 80 and sentence[0] >= 'A' and sentence[0] <= 'Z':
                    if blank:
                        print()
                    else:
                        blank = True
                    if len(prefix) > 0:
                        print(prefix, sentence)
                        prefix = ''
                    else:
                        print(sentence)
                sentence = line
