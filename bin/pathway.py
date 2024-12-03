#!/usr/bin/env python3
import re
import sys

descr2acc = {}
descr2type = {}

with open('pathlist.txt', 'r') as f:
    descr = ''
    for line in f:
        line = line.rstrip()
        if m := re.match(r'^ID\s+(.*)$', line):
            descr = m.group(1).lower()
            if descr.endswith('.'):
                descr = descr.rstrip('.')
            else:
                print('ERROR: description does not end with period: ' + descr, file=sys.stderr)
                sys.exit(1)                    
        if m := re.match(r'^AC\s+(.*)$', line):
            descr2acc[descr] = m.group(1)
        if m := re.match(r'^CL\s+(.*)\.$', line):
            descr2type[descr] = m.group(1)


def get_type(descr):
    if descr2type.get(descr) != None:
        ret = descr2type.get(descr)
        if m := re.match(r'^(.+): step \d+/\d+$', descr):
            ret = get_type(m.group(1)) + ';' + ret
        return ret
    else:
        return 'NULL'


def get_acc(descr):
    if descr2acc.get(descr) != None:
        acc = descr2acc.get(descr)
        if m := re.match(r'^(.+): step \d+/\d+$', descr):
            acc = get_acc(m.group(1)) + ';' + acc
        return acc
    else:
        print(f'AC_NULL\t{descr}', file=sys.stderr)
        return 'NULL'


def get_type_list(description):
    description = description.lower()
    if m := re.match(r'^(.+) \[regulation\]$', description):
        description = m.group(1)
    list = []
    for elem in description.split('; '):
        pathway_type = get_type(elem)
        if pathway_type != '':
            list.append(pathway_type)
    ret = ";".join(list)
    return ret


def get_acc_list(description):
    description = description.lower()
    reg = ''
    if m := re.match(r'^(.+) \[regulation\]$', description):
        description = m.group(1)
        reg = 'R'
    list = []
    for elem in description.split('; '):
        acc = get_acc(elem)
        if acc != '':
            list.append(acc)
    ret = ";".join(list)
    if reg != '':
        ret += ';' + reg
    return ret


with open('pathway.txt', 'r') as f:
    count = 0
    description = ''
    pathway_type = ''
    for line in f:
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
            line = line.lstrip().rstrip(',')
            arr = line.split(', ')
            for item in arr:
                item = item.rstrip()
                if matched := re.match(r'^(\S+)\s+\((\S+)\)$', item):
                    mnemonic, uniprot_id = matched.groups()
                    print(uniprot_id, mnemonic, acc_list, description, pathway_type, sep='\t')
                else:
                    print('ERROR: ' + item, file=sys.stderr)
                    sys.exit(1)
        elif matched := re.match(r'^(\S.*)\.$', line):
            description = matched.group(1)
            acc_list = get_acc_list(description)
            pathway_type = get_type_list(description)
        else:
            print('ERROR: ' + line, file=sys.stderr)
            sys.exit(1)
