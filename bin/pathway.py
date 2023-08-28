#!/usr/bin/env python3
import argparse
import sys
import re

descr2acc = {}
descr2type = {}
def read_pathlist():
    with open('pathlist.txt', 'r') as f:
        count = 0
        descr = ''
        acc = ''
        for line in f:
            line = line.rstrip()
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
                descr2acc[descr] = acc
            m = re.match(r'^CL\s+(.*)\.$', line)
            if m:
                type = m.groups()[0]
                descr2type[descr] = type


def get_type_from_dict(description):
    if descr2type.get(description) != None:
        ret = descr2type.get(description)
        m = re.match(r'^(.+): step \d+/\d+$', description)
        if m:
            core_descr = m.groups()[0]
            ret = get_type_from_dict(core_descr) + ';' + ret
        return ret
    else:
        return 'NULL'


def get_acc_from_dict(description):
    if descr2acc.get(description) != None:
        ret = descr2acc.get(description)
        m = re.match(r'^(.+): step \d+/\d+$', description)
        if m:
            core_descr = m.groups()[0]
            ret = get_acc_from_dict(core_descr) + ';' + ret
        return ret
    else:
        print(description, file=sys.stderr)
        return 'NULL'


def get_type_list_from_line(line):
    line = line.lower()
    m = re.match(r'^(.+) \[regulation\]$', line)
    if m:
        line = m.groups()[0]
    arr = line.split('; ')
    list = []
    for i in arr:
        type = get_type_from_dict(i)
        if type != '':
            list.append(type)
    ret = ";".join(list)
    return ret


def get_acc_list_from_line(line):
    line = line.lower()
    m = re.match(r'^(.+) \[regulation\]$', line)
    reg = ''
    if m:
        line = m.groups()[0]
        reg = 'R'
    arr = line.split('; ')
    list = []
    for i in arr:
        acc = get_acc_from_dict(i)
        if acc != '':
            list.append(acc)
    ret = ";".join(list)
    if reg != '':
        ret += ';' + reg
    return ret


read_pathlist()
with open('pathway.txt', 'r') as f:
    count = 0
    description = ''
    type = ''
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
            line = line.lstrip()
            line = line.rstrip(',')
            arr = line.split(', ')
            for i in arr:
                i = i.rstrip()
                m = re.match(r'^(\S+)\s+\((\S+)\)$', i)
                if m:
                    [mnemonic, uniprot_id] = m.groups()
                    print(uniprot_id, mnemonic, acc_list, description, type, sep='\t')
                else:
                    print('ERROR: ' + i, file=sys.stderr)
                    sys.exit(1)
        else:
            ma = re.match(r'^(\S.*)\.$', line)
            if ma:
                description = ma.groups()[0]
                acc_list = get_acc_list_from_line(description)
                type = get_type_list_from_line(description)
            else:
                print('ERROR: ' + line, file=sys.stderr)
                sys.exit(1)
