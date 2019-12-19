#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random


class BayesianNet:
    def __init__(self, node_sets):
        """node_set: [[X1, parents1, cp_table1],
        [X2, parents2, cp_table2]]"""
        self.nodes = []
        self.variables = []
        self.variable_values = [True, False]
        # for node_set in node_sets:
        #     self.add(node_set)
        while len(self.nodes) < len(node_sets):
            for node_set in node_sets:
                self.add(node_set)

    def variable_node(self, var):
        for node in self.nodes:
            if node.variable == var:
                return node

    def add(self, node_set):
        node = BayesNode(node_set)
        while (node.variable not in self.variables) & (all((parent in self.variables) for parent in node.parents)):
            self.nodes.append(node)
            self.variables.append(node.variable)
            for parent in node.parents:
                self.variable_node(parent).children.append(node)


def event_values(event, variables):
    """event = {'Earthquake': True, 'Burglary': False}
    return a list of values of variables in event"""
    l = []
    for var in variables:
        l.append(event.get(var))
    return l


class BayesNode:
    """A conditional probability distribution"""

    def __init__(self, node_set):
        """X: a variable name
        parents: a sequence of variable names
        cp_tablet: the conditional probability table. A dictionary in the form:
        {(v1, v2, ...): p, ...}
        the distribution P(X=true | parent1=v1, parent2=v2, ...)
        X = BayesNode('X', '', 0.2)
        Y = BayesNode('Y', 'P', {T: 0.2, F: 0.7})
        Z = BayesNode('Z', 'P Q',
        ...    {(T, T): 0.2, (T, F): 0.3, (F, T): 0.5, (F, F): 0.7})
        """
        self.variable = node_set[0]
        self.parents = node_set[1]
        self.cp_table = node_set[2]
        self.children = []

    def prob(self, value, event):
        """Return the conditional probability when query variable has value given event
        value must be True or False
        event: a dictionary such as {'Burglary': False, 'Earthquake': True}

        bn = BayesNode('X', 'Burglary', {T: 0.2, F: 0.625})
        bn.prob(False, {'Burglary': False, 'Earthquake': True})
        0.375"""
        if self.parents:
            if len(event_values(event, self.parents)) == 1:
                ptrue = float(self.cp_table.get(event_values(event, self.parents)[0]))
            else:
                ptrue = float(self.cp_table.get(tuple(event_values(event, self.parents))))
        else:
            ptrue = float(self.cp_table.get(None))

        if value:
            return ptrue
        else:
            return 1 - ptrue

    def sample(self, event):
        """Return True/False at random according with the conditional probability
        given the parents."""
        return self.prob(True, event) > random.uniform(0.0, 1.0)
