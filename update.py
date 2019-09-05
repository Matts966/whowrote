import math
import sys
import MeCab
from collections import defaultdict


class NaïveBayes:
    def __init__(self):
        self.vocabulary = set()
        self.book_counter = defaultdict(int)  # '夏目漱石': 16, ... など
        self.word_counter = defaultdict(lambda: defaultdict(int))  # '夏目漱石': {'人生': 4, 'ハッピー': 2,...}  など

    def to_words(self, sentence):
        """
        学習、分類で共通の単語化メソッド
        """
        tagger = MeCab.Tagger('mecabrc')
        mecab_result = tagger.parse(sentence)
        info_of_words = mecab_result.split('\n')
        words = []
        for info in info_of_words:
            # 文末を除く
            if info == 'EOS' or info == '':
                break
            # info には '文豪\t名詞,一般,*,*,*,*,文豪,ブンゴウ,ブンゴー'等が入る
            info_elems = info.split(',')
            # インデックス6に、原型が入っている。'*'の場合0番目を入れる
            if info_elems[6] == '*':
                # info_elems[0] には '文豪\t名詞' といったタグ付き単語が入る
                # 品詞の違う同単語を弁別する
                # 弁別しない場合は、次の1行の一部をアンコメントアウトする。その方が精度が良い？
                words.append(info_elems[0]) #[:-3])
                continue
            words.append(info_elems[6])
        return tuple(words)

    def update_counter(self, words, writer):
        """
        カウンター更新メソッド
        """
        for word in words:
            self.word_counter[writer][word] += 1
            self.vocabulary.add(word)
        self.book_counter[writer] += 1

    def train(self, doc, writer):
        """
        学習メソッド
        """
        words = self.to_words(doc)
        self.update_counter(words, writer)

    def prior_prob(self, writer):
        """
        事前確率計算メソッド
        """
        writers_count = sum(self.book_counter.values())
        num_of_docs_of_the_writer = self.book_counter[writer]
        return num_of_docs_of_the_writer / writers_count

    # ベイズの法則で単語ごとに計算し、後から合わせて尤度を計算する。
    def word_prob(self, word, writer):
        """
        単語ごとの登場確率を計算するメソッド
        """
        # ラプラススムージング
        c = self.word_counter[writer][
            word] if word in self.word_counter[writer] else 0 + 1
        s = sum(self.word_counter[writer].values()) + len(
            self.vocabulary)
        prob = c / s
        return prob

    def classify(self, doc):
        """
        分類メソッド
        """
        # 非常に0に近い数値を扱うため、logを取る。
        # logを取っているため、マイナスに大きな値になる。
        max_probability = -sys.maxsize
        fit_writer = None
        words = self.to_words(doc)

        # logを取っているため、以下のように加算となる。
        for writer in self.book_counter.keys():
            prob = math.log(self.prior_prob(writer))
            for word in words:
                prob += math.log(self.word_prob(word, writer))

            if prob > max_probability:
                max_probability = prob
                fit_writer = writer

        return fit_writer