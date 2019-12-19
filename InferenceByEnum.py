#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Zeyi Pan'

import numpy


class ProbDist:
    """A discrete probability distribution
    eg. True: 0.5, False: 0.5
    """
    def __init__(self, var_name=''):
        self.prob = {}
        self.var_name = var_name
        self.values = []

    def __getitem__(self, val):
        """Given a value, return P(value)."""
        try:
            return self.prob[val]
        except KeyError:
            return 0

    def __setitem__(self, val, p):
        """Set P(val) = p."""
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        total = sum(self.prob.values())
        if not numpy.isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self


def extend(v, value1, value2):
    """use value2 to replace value1"""
    v_new = v.copy()
    v_new[value1] = value2
    return v_new


def enumeration_ask(X, bn, e):
    """
    Return the conditional probability distribution of variable X
    given evidence e, from BayesNet bn.
    """
    while str(X) not in e:
        Q = ProbDist(X)
        for xi in bn.variable_values:
            Q[xi] = enumerate_all(bn.variables, extend(e, X, xi), bn)
        return Q.normalize()
    print("Query variable is evident variables")


def enumerate_all(variables, e, bn):
    if len(variables) == 0:
        return 1.0
    Y = variables[0]
    rest = variables[1:]
    if Y in e:
        return float(bn.variable_node(Y).prob(e.get(Y), e)) * enumerate_all(rest, e, bn)
    else:
        return sum(float(bn.variable_node(Y).prob(y, e)) * enumerate_all(rest, extend(e, Y, y), bn)
                   for y in bn.variable_values)


