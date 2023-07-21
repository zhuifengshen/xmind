# -*- coding: utf-8 -*-
import os
import argparse
import pickle

from utils.similar import jaccard
from utils.segmentor import Segmentor
from utils.utils import check_file, get_stop_words, Range


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', type=str, default='./data/output', help='Directory of input file.')
    parser.add_argument('--dict', type=str, default='./data/seg_dict', help='Directory of dict file.')
    parser.add_argument('--stop_words', type=str, default='./data/stop_words', help='Directory of stop words.')
    parser.add_argument('--top_k', type=int, default=3, help='Return k item.')
    parser.add_argument('--sim_th', type=float, default=1.0, choices=[Range(0.5, 1.0)],
                        help='Threshold for word similarity.')
    parser.add_argument('--threshold', type=float, default=0.3, choices=[Range(0.0, 1.0)],
                        help='Threshold for matching.')
    parser.add_argument('--lang', type=str, choices=['cn', 'en'], default='cn', help='Segmentor language setting.')
    args = parser.parse_args()
    return args


class Searcher(object):
    def __init__(self, args=_get_parser()):
        p_bucket_path = os.path.join(args.infile, 'p_bucket.pickle')
        with open(p_bucket_path, 'rb') as infile:
            self.p_bucket = pickle.load(infile)
        self.seg = Segmentor(args)
        self.path = args.infile
        self.sim_th = args.sim_th
        self.stop_words = get_stop_words(args.stop_words)
        self.args = args

    def search(self, sentence):
        if not sentence or type(sentence) != str:
            return None
        res = list()
        c_bucket = list()
        seg_sen = list(self.seg.cut(sentence))
        seg_sen = list(filter(lambda x: x not in self.stop_words, seg_sen))
        for w in seg_sen:
            if w in self.p_bucket:
                c_bucket += self.p_bucket[w]
        c_bucket = list(set(c_bucket))
        cmp, score = list(), list()
        for bucket in c_bucket:
            bucket_path = os.path.join(self.path, bucket)
            check_file(bucket_path)
            infile = open(bucket_path, 'r', encoding="utf-8")
            for inline in infile:
                inline = inline.rstrip()
                line = inline.split(':::')[0]
                seg_list = list(self.seg.cut(line))
                seg_list = list(filter(lambda x: x not in self.stop_words, seg_list))
                sc = jaccard(seg_sen, seg_list)
                if sc < self.args.threshold:
                    continue
                cmp.append(inline)
                score.append(sc)
            infile.close()

        zipped = zip(cmp, score)
        zipped = sorted(zipped, key=lambda x: x[1], reverse=True)
        right = None if self.args.top_k <= 0 else self.args.top_k
        for (cp, sc) in zipped[:right]:
            res.append(cp)
        return res


if __name__ == '__main__':
    sea = Searcher()
    res = sea.search('我是')
    print(res)
