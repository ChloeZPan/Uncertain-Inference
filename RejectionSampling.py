#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Li'


def prior_sample(bn):
    """Randomly generates events from a given Bayesian network"""
    event_x = {}
    for node in bn.nodes:
        event_x[node.variable] = node.sample(event_x)
    return event_x


def rejection_sampling(query_x, observed_e, bn, num=100):
    """Estimate the probability distribution of query_x given evidence observed_e
    in BayesNet bn, using num samples"""
    counter = {x: 0 for x in bn.variable_values}
    for j in range(num):
        sample = prior_sample(bn)
        if consistent_with(sample, observed_e):
            counter[sample[query_x]] += 1
    # print("Value : %s" % counter.items())  # TODO: need to be deleted
    return normalize(counter)


def consistent_with(sample, evidence):
    """Return True if the given sample is consistent with the given evidence"""
    return all(sample.get(k) == v for k, v in evidence.items())


def normalize(counter):
    total = 0
    for result, counts in counter.items():
        total += counts
    for result, counts in counter.items():
        counter[result] = counts / total
    return counter
