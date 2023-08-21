# -*- coding: utf-8 -*-
import os
import argparse


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dict', type=str, default='../data/seg_dict', help='Directory of dict file.')
    parser.add_argument('--lang', type=str, choices=['cn', 'en'], default='cn', help='Segmentor language setting.')
    args = parser.parse_args()
    return args


class Segmentor(object):
    """
    Wrapper for bilingual tokenizer
    """
    def __init__(self, args):
        if args.lang == 'cn':
            import jieba
            if args.dict:
                if not os.path.exists(args.dict):
                    print('Segmentor dictionary not found.')
                    exit(1)
                jieba.load_userdict(args.dict)
            self.cut = jieba.cut
        else:  # en
            from spacy.tokenizer import Tokenizer
            from spacy.lang.en import English
            nlp = English()
            self.tokenizer = Tokenizer(nlp.vocab)
            self.cut = self.cut_en

    def cut_en(self, sentence):
        words = self.tokenizer(sentence)
        words = [w.text for w in words]
        return words


if __name__ == '__main__':
    args = _get_parser()
    args.lang = 'cn'
    seg = Segmentor(args)
    res = list(seg.cut('你是李小龙吗？'))
    print(res)
    args.lang = 'en'
    seg = Segmentor(args)
    res = list(seg.cut('Are you Bruce Lee?'))
    print(res)
