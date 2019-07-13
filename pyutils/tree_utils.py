# -*- coding: utf-8 -*-
"""
    utils.tree_utils
    ~~~~~~~~~~~~~~

    树相关

    :create by: lyncir
    :date: 2018-11-17 15:38:13 (+0800)
    :last modified date: 2018-11-17 15:39:52 (+0800)
    :last modified by: lyncir
"""
from collections import defaultdict


def tree():
    """
    构造一颗字典树
    """
    return defaultdict(tree)
