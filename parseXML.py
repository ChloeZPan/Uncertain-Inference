#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Zeyi Pan'

import BayesianNet as b


def get_child(node, name):
    """get child node in XML"""
    for child in node.childNodes:
        if child.localName == name:
            return child


def get_node(node, name):
    clist = []
    for child in node.childNodes:
        if child.localName == name:
            clist.append(child)
    return clist


def get_query(file):
    variable = file.getElementsByTagName("VARIABLE")
    var_list = []
    for node in variable:
        n = get_child(node, "NAME")
        var_list.append(n.childNodes[0].nodeValue)
    return var_list


def build_bn(file):
    """build bayesian networks"""
    prob_dist = file.getElementsByTagName("DEFINITION")
    node_sets = []

    for node in prob_dist:
        parents = []
        temp_cp = []
        conp_table = {}
        # get query
        X = get_child(node, "FOR").childNodes[0].nodeValue

        # get parents
        if get_child(node, "GIVEN"):
            for p in get_node(node, "GIVEN"):
                parents.append(p.childNodes[0].nodeValue)
        else:
            parents = []

        # get conditional prob table
        for t in get_child(node, "TABLE").childNodes:
            if t.nodeType == t.TEXT_NODE and t.data.strip():
                temp_cp.append(t.data.strip().split()[0])
        if len(temp_cp) == 1:
            conp_table = {None: temp_cp[0]}
        elif len(temp_cp) == 2:
            conp_table = {True: temp_cp[0], False: temp_cp[1]}
        elif len(temp_cp) == 4:
            conp_table = {(True, True): temp_cp[0], (True, False): temp_cp[1],
                        (False, True): temp_cp[2], (False, False): temp_cp[3]}

        node_set = [X, parents, conp_table]
        node_sets.append(node_set)
    # build bayesian networks
    bn = b.BayesianNet(node_sets)
    return bn


# For dog problem
def dog_build_bn(file):
    """build bayesian networks"""
    prob_dist = file.getElementsByTagName("DEFINITION")
    node_sets = []

    for node in prob_dist:
        parents = []
        temp_cp = []
        conp_table = {}
        # get query
        X = get_child(node, "FOR").childNodes[0].nodeValue
        # get parents
        if get_child(node, "GIVEN"):
            for p in get_node(node, "GIVEN"):
                parents.append(p.childNodes[0].nodeValue)
        else:
            parents = []
        # get conditional prob table
        for t in get_child(node, "TABLE").childNodes:
            if t.data.strip():
                temp_cp = t.data.strip().split()
        if len(temp_cp) == 2:
            conp_table = {None: temp_cp[0]}
        elif len(temp_cp) == 4:
            conp_table = {True: temp_cp[0], False: temp_cp[2]}
        elif len(temp_cp) == 8:
            conp_table = {(True, True): temp_cp[0], (True, False): temp_cp[2],
                        (False, True): temp_cp[4], (False, False): temp_cp[6]}
        node_set = [X, parents, conp_table]

        node_sets.append(node_set)
    # build bayesian networks
    bn = b.BayesianNet(node_sets)
    return bn
