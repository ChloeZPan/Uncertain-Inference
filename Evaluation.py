#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Li'

import InferenceByEnum as IEnum
import RejectionSampling as Rj
from xml.dom import minidom
import parseXML as Px
import sys


def exact_inf(f, query, *args):
    """Return the result of exact inference using inference by enumeration"""
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
    return IEnum.enumeration_ask(q, bn, e).prob


def approx_inf(f, n, query, *args):
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

    return Rj.rejection_sampling(q, e, bn, n)


if __name__ == "__main__":
    initial = int(sys.argv[1])  # Initial number of samples
    delta = int(sys.argv[2])  # Loop increment
    filename = sys.argv[3]
    query_variable = sys.argv[4]
    exact = exact_inf(filename, query_variable, sys.argv[5:])
    answer_true = exact.get(True)  # Exact value
    answer_false = exact.get(False)  # Exact value
    while True:
        total_true = 0
        total_false = 0
        total_err = 0
        for y in range(10):
            approx = approx_inf(filename, initial, query_variable, sys.argv[5:])
            prob_true = approx.get(True)
            prob_false = approx.get(False)
            total_err += (prob_true - answer_true) / answer_true
            total_true += prob_true
            total_false += prob_false
        avg_true = total_true / 10  # Average conditional probability when the query variable is true
        avg_false = total_false / 10  # Average conditional probability when the query variable is false
        err = min(abs((avg_true - answer_true) / answer_true), abs((avg_false - answer_false) / answer_false))
        print('True:', avg_true, 'False:', avg_false, '| error:', err, '| number of samples:', initial)
        if err < 0.01:
            print(initial,
                  'samples are necessary for rejection sampling to be within 1% of the exact value in this case.')
            break
        initial += delta
