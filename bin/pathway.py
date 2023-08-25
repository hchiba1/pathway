#!/usr/bin/env python3
import argparse
import sys
import re

parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', '--cores', type=int, default=1, help='')
parser.add_argument('-v', '--verbose', action='store_true', help='')
args = parser.parse_args()

def read_patylist():
    with open('pathlist.txt', 'r') as f:
        count = 0
        descr = ''
        acc = ''
        dict = {}
        for line in f:
            line = line.rstrip()
            if line.startswith('---'):
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
    return dict


def get_acc_from_dict(dict, description):
    if dict.get(description) != None:
        return dict.get(description)
    else:
        print(description, file=sys.stderr)
        return ''


def get_acc_list_from_line(dict, line):
    arr = line.split('; ')
    acc_list = []
    for i in arr:
        acc = get_acc_from_dict(dict, i)
        if acc != '':
            acc_list.append(acc)
    return ";".join(acc_list)


def main():
    dict = read_patylist()
    count = 0
    description = ''
    for line in sys.stdin:
        line = line.rstrip()
        if len(line) == 0:
            continue
        if line.startswith('---'):
            count += 1
            if count == 3:
                continue
            if count == 4:
                break
        if count <= 2:
            continue
        if line.startswith(' '):
            line = line.lstrip()
            line = line.rstrip(',')
            arr = line.split(', ')
            for i in arr:
                i = i.rstrip()
                m = re.match(r'^(\S+)\s+\((\S+)\)$', i)
                if m:
                    [mnemonic, uniprot_id] = m.groups()
                    print(uniprot_id, mnemonic, acc_list, description, sep='\t')
                else:
                    print('ERROR: ' + i, file=sys.stderr)
                    sys.exit(1)
        else:
            ma = re.match(r'^(\S.*)\.$', line)
            if ma:
                description = ma.groups()[0]
                description = description.lower()
                acc_list = get_acc_list_from_line(dict, description)
            else:
                print('ERROR: ' + line, file=sys.stderr)
                sys.exit(1)


if __name__ == '__main__':
    main()
