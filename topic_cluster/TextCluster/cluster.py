# -*- coding: utf-8 -*-
from ast import arg
import os
import argparse
import pickle
import re
from typing import Optional
from collections import defaultdict

from tqdm import tqdm

from .utils.similar import jaccard
from .utils.segmentor import Segmentor
from .utils.utils import check_file, ensure_dir, clean_dir, sample_file, get_stop_words, line_counter, Range

import argparse

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except Warning:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()

# Constants
DEFAULT_INFILE = os.path.join(ROOT_DIR, 'data/infile')
DEFAULT_OUTPUT = os.path.join(ROOT_DIR, 'data/output')
DEFAULT_DICT = os.path.join(ROOT_DIR, 'data/seg_dict')
DEFAULT_STOP_WORDS = os.path.join(ROOT_DIR, 'data/stop_words')
DEFAULT_SAMPLE_NUMBER = 5
DEFAULT_THRESHOLD = 0.07  # Default 0.3
DEFAULT_NAME_LEN = 4
DEFAULT_NAME_LEN_UPDATE = False
DEFAULT_LANG = 'cn'


class ClusterArgs(object):
    def __init__(self):
        self.infile = DEFAULT_INFILE
        self.output = DEFAULT_OUTPUT
        self.dict = DEFAULT_DICT
        self.stop_words = DEFAULT_STOP_WORDS
        self.sample_number = DEFAULT_SAMPLE_NUMBER
        self.threshold = DEFAULT_THRESHOLD
        self.name_len = DEFAULT_NAME_LEN
        self.name_len_update = DEFAULT_NAME_LEN_UPDATE
        self.lang = DEFAULT_LANG


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', type=str, default=DEFAULT_INFILE, help='Directory of input file.')
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT, help='Directory to save output file.')
    parser.add_argument('--dict', type=str, default=DEFAULT_DICT, help='Directory of dict file.')
    parser.add_argument('--stop_words', type=str, default=DEFAULT_STOP_WORDS, help='Directory of stop words.')
    parser.add_argument('--sample_number', type=int, default=DEFAULT_SAMPLE_NUMBER, choices=range(1), help='Sample number for each bucket.')
    parser.add_argument('--threshold', type=float, default=DEFAULT_THRESHOLD, choices=range(0.0, 1.0), help='Threshold for matching.')
    parser.add_argument('--name_len', type=int, default=DEFAULT_NAME_LEN, choices=range(2), help='Filename length.')
    parser.add_argument('--name_len_update', type=bool, default=DEFAULT_NAME_LEN_UPDATE, help='To update file name length.')
    parser.add_argument('--lang', type=str, choices=['cn', 'en'], default=DEFAULT_LANG, help='Segmentor language setting.')
    args = parser.parse_args()
    return args


def cluster(args, input: Optional[list] = None, ret_output=True):
    '''
    description: 
    param {*} args - origin args
    param {*} input - If input is not None, then args.infile will be ignored.
    param {*} ret_output - If ret_output is True, then return output list.
    return {*}
    '''
    # preliminary work
    check_file(args.infile)
    ensure_dir(args.output)

    if args.name_len_update:
        line_cnt = line_counter(args.infile)
        args.name_len = len(str(line_cnt)) + 1

    clean_dir(args.output, args.name_len)
    # end preliminary work

    p_bucket = defaultdict(list)
    save_idx = 0
    id_name = '{0:0' + str(args.name_len) + 'd}'
    # load stop words
    stop_words = get_stop_words(args.stop_words) if os.path.exists(args.stop_words) else list()
    # load tokenizer
    seg = Segmentor(args)

    # print('Splitting sentence into different clusters ...')
    if input:
        data = input
    else:
        infile = open(args.infile, 'r', encoding="utf-8")
        data = tqdm(infile)
        
    for inline in data:
        # Skip empty line
        if not inline:
            continue
        inline = inline.rstrip()
        line = inline.split(':::')[0]
        is_match = False
        seg_list = list(seg.cut(line))
        if stop_words:
            seg_list = list(filter(lambda x: x not in stop_words, seg_list))
        for wd in seg_list:
            if is_match:
                break
            w_bucket = p_bucket[wd]
            for bucket in w_bucket:
                bucket_path = os.path.join(args.output, bucket)
                check_file(bucket_path)
                selected = sample_file(bucket_path, args.sample_number)
                selected = list(map(lambda x: x.split(':::')[0], selected))
                selected = list(map(lambda x: list(seg.cut(x)), selected))
                # remove stop words
                if stop_words:
                    filt_selected = list()
                    for sen in selected:
                        sen = list(filter(lambda x: x not in stop_words, sen))
                        filt_selected.append(sen)
                    selected = filt_selected
                # calculate similarity with each bucket
                if all(jaccard(seg_list, cmp_list) > args.threshold for cmp_list in selected):
                    is_match = True
                    with open(bucket_path, 'a', encoding='utf-8') as outfile:
                        outfile.write(line+'\n')
                    for w in seg_list:
                        if bucket not in p_bucket[w]:
                            p_bucket[w].append(bucket)
                    break
        if not is_match:
            bucket_name = ('tmp' + id_name).format(save_idx)
            bucket_path = os.path.join(args.output, bucket_name)
            with open(bucket_path, 'a', encoding='utf-8') as outfile:
                outfile.write(line+'\n')
            for w in seg_list:
                p_bucket[w].append(bucket_name)
            save_idx += 1
    if not input:
        infile.close()

    # sort and rename file
    file_list = os.listdir(args.output)
    file_list = list(filter(lambda x: x.startswith('tmp'), file_list))
    cnt = dict()
    for file in file_list:
        file_path = os.path.join(args.output, file)
        cnt[file] = line_counter(file_path)

    sorted_cnt = sorted(cnt.items(), key=lambda kv: kv[1], reverse=True)
    name_map = dict()
    for idx, (file_name, times) in enumerate(sorted_cnt):
        origin_path = os.path.join(args.output, file_name)
        new_name = id_name.format(idx)
        new_path = os.path.join(args.output, new_name)
        os.rename(origin_path, new_path)
        name_map[file_name] = new_name

    for k, v in p_bucket.items():
        p_bucket[k] = list(map(lambda x: name_map[x], v))

    p_bucket_path = os.path.join(args.output, 'p_bucket.pickle')
    with open(p_bucket_path, 'wb') as outfile:
        pickle.dump(p_bucket, outfile, protocol=pickle.HIGHEST_PROTOCOL)

    # print('All is well')
    if ret_output:
        return get_clustered_data()


def get_clustered_data():
    data = []
    for root, folder, file in os.walk(DEFAULT_OUTPUT):
        for f in file:
            if re.match(r'^\d+$', f):
                file_data = []
                file_path = os.path.join(root, f)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        file_data.append(line.rstrip())
                data.append(file_data)
    return data

def main():
    args = _get_parser()
    cluster(args)

if __name__ == '__main__':
    # Python
    args = ClusterArgs()
    cluster(args)
    
    # CLI
    # main()
