#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Zeyi Pan'

import InferenceByEnum as I
from xml.dom import minidom
import parseXML as p
import sys


def start(f, query, *args):
    file = minidom.parse(f)
    if f == "dog-problem.xml":
        bn = p.dog_build_bn(file)
    else:
        bn = p.build_bn(file)
    if len(args[0]) == 0 or len(args[0])%2 != 0:
        raise Exception('Please enter correct evidence')

    e = {}  # Store evidence variables and related value in a dictionary
    for i in range(int(len(args[0]) / 2)):
        if args[0][i * 2 + 1] == 'true':
            e[args[0][i * 2]] = True
        else:
            e[args[0][i * 2]] = False

    q = str(query)
    return I.enumeration_ask(q, bn, e).prob


# e = {'J': True, 'M': True}

# print(i.enumeration_ask('B', bn, e).prob)


if __name__ == "__main__":
    f = sys.argv[1]
    query = sys.argv[2]
    print(', '.join("{}: {}".format(k, v) for k, v in start(f, query, sys.argv[3:]).items()))
