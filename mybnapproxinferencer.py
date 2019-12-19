#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Zeyi Pan'

import RejectionSampling as Rj
from xml.dom import minidom
import parseXML as Px
import sys


def approx_inf(f, num, query, *args):
    """Return the result of approximate inference using rejection sampling"""
    file = minidom.parse(f)
    if f == "dog-problem.xml":
        bn = Px.dog_build_bn(file)
    else:
        bn = Px.build_bn(file)
    if len(args[0]) == 0 or len(args[0]) % 2 != 0:
        raise Exception('Please enter correct evidence')

    e = {}  # Store evidence variables and related value in a dictionary
    for i in range(int(len(args[0]) / 2)):
        if args[0][i * 2 + 1] == 'true':
            e[args[0][i * 2]] = True
        else:
            e[args[0][i * 2]] = False

    q = str(query)

    return Rj.rejection_sampling(q, e, bn, num)


if __name__ == "__main__":
    filename = sys.argv[2]
    num = int(sys.argv[1])
    query_variable = sys.argv[3]
    # print(', '.join("{}: {}".format(k, v) for k, v in exact_inf(filename, query_variable, sys.argv[4:]).items()))
    print(', '.join("{}: {}".format(k, v) for k, v in approx_inf(filename, num, query_variable, sys.argv[4:]).items()))
