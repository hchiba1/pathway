#!/usr/bin/env python3
import argparse
import re

parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', '--cores', type=int, default=1, help='')
parser.add_argument('-v', '--verbose', action='store_true', help='')
args = parser.parse_args()

def main():
    with open('pathlist.txt', 'r') as f:
        count = 0
        descr = ''
        acc = ''
        dict = {}
        for line in f:
            line = line.rstrip()
            if line.startswith('___'):
                count += 1
                if count == 1:
                    continue
            if count == 0:
                continue
            m = re.match(r'^ID\s+(.*)$', line)
            if m:
                descr = m.groups()[0]
                descr = descr.lower()
                if descr.endswith('.'):
                    descr = descr.rstrip('.')
                else:
                    print('ERROR: description does not end with period: ' + descr, file=sys.stderr)
                    sys.exit(1)                    
            m = re.match(r'^AC\s+(.*)$', line)
            if m:
                acc = m.groups()[0]
                dict[descr] = acc
                print(acc, descr, sep='\t')


if __name__ == '__main__':
    main()
