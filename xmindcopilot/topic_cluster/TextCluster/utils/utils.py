# -*- coding: utf-8 -*-
import os
import re
import random


class Range(object):
    def __init__(self, start, end=None):
        self.start = start
        self.end = end

    def __eq__(self, other):
        if self.end:
            return self.start <= other <= self.end
        else:
            return self.start <= other


def check_file(file):
    if file is not None and not os.path.exists(file):
        print("File {} does not exist. Exit.".format(file))
        exit(1)


def ensure_dir(d, verbose=True):
    if not os.path.exists(d):
        if verbose:
            print("Directory {} do not exist; creating...".format(d))
        os.makedirs(d)


def clean_dir(d, l=9):
    """
    should be identical to file naming pattern
    """
    file_list = os.listdir(d)
    name_pattern = '[0-9]{' + str(l) + '}$'
    file_list = list(filter(lambda x: re.search(name_pattern, x), file_list))
    for fname in file_list:
        file_path = os.path.join(d, fname)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def line_counter(d):
    with open(d, 'r', encoding='utf-8') as infile:
        line_cnt = sum(1 for _ in infile)
    return line_cnt


def sample_file(filename, k=5):
    """
    Random select k lines from input file.
    :param filename: input file directory.
    :param k: selected number.
    :return: list of lines
    """
    selected = list()
    line_cnt = line_counter(filename)
    with open(filename, 'r', encoding='utf-8') as infile:
        if line_cnt <= k:
            selected = list(map(lambda x: x.rstrip(), infile.readlines()))

        else:
            # generate k random number and sort them
            random_index = sorted(random.sample(range(line_cnt), k), reverse=True)
            select_index = random_index.pop()
            for idx, line in enumerate(infile):
                if idx == select_index:
                    selected.append(line.rstrip())
                    if len(random_index) > 0:
                        select_index = random_index.pop()
                    else:
                        break

        return selected


def get_stop_words(d):
    with open(d, 'r', encoding='utf-8') as infile:
        data = infile.readlines()
    data = list(map(lambda x: x.rstrip(), data))
    data.append(' ')  # manual insert
    return data


if __name__ == '__main__':
    res = sample_file('../data/infile')
    print(res)
    res = sample_file('../data/seg_dict')
    print(res)

