# -*- coding: utf-8 -*-


def jaccard(a, b):
    """
    Calculate Jaccard similarity.
    :param a: sentence1, list of segmented words
    :param b: sentence2
    :return: similar score
    """
    a = set(a)
    b = set(b)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))
