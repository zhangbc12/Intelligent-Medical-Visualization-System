#!/usr/bin/env python3
# coding: utf-8
import os
import ahocorasick
import jieba
import numpy as np
from QASystem.intention_predict import predict as class_predict

class EntityExtractor:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 路径
        self.vocab_path = os.path.join(cur_dir, 'data/vocab.txt')
        self.stopwords_path =os.path.join(cur_dir, 'data/stop_words.utf8')
        self.word2vec_path = os.path.join(cur_dir, 'data/merge_sgns_bigram_char300.txt')
        self.stopwords = [w.strip() for w in open(self.stopwords_path, 'r', encoding='utf8') if w.strip()]

        data_dir = "data/"

        self.disease_path = data_dir + 'disease_vocab.txt'
        self.symptom_path = data_dir + 'symptom_vocab.txt'
        self.alias_path = data_dir + 'alias_vocab.txt'
        self.complication_path = data_dir + 'complications_vocab.txt'

        self.disease_entities = [w.strip() for w in open(self.disease_path, encoding='utf8') if w.strip()]
        self.symptom_entities = [w.strip() for w in open(self.symptom_path, encoding='utf8') if w.strip()]
        self.alias_entities = [w.strip() for w in open(self.alias_path, encoding='utf8') if w.strip()]
        self.complication_entities = [w.strip() for w in open(self.complication_path, encoding='utf8') if w.strip()]

        self.region_words = list(set(self.disease_entities+self.alias_entities+self.symptom_entities))

        # 构造领域actree
        self.disease_tree = self.build_actree(list(set(self.disease_entities)))
        self.alias_tree = self.build_actree(list(set(self.alias_entities)))
        self.symptom_tree = self.build_actree(list(set(self.symptom_entities)))
        self.complication_tree = self.build_actree(list(set(self.complication_entities)))

        self.symptom_qwds = ['什么症状', '哪些症状', '症状有哪些', '症状是什么', '什么表征', '哪些表征', '表征是什么',
                             '什么现象', '哪些现象', '现象有哪些', '症候', '什么表现', '哪些表现', '表现有哪些',
                             '什么行为', '哪些行为', '行为有哪些', '什么状况', '哪些状况', '状况有哪些', '现象是什么',
                             '表现是什么', '行为是什么']  # 询问症状
        self.cureway_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片', '吃什么药', '用什么药', '怎么办',
                             '买什么药', '怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治',
                             '医治方式', '疗法', '咋治', '咋办', '咋治', '治疗方法']  # 询问治疗方法
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时',
                              '几个小时', '多少年', '多久能好', '痊愈', '康复']  # 询问治疗周期
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例',
                              '可能性', '能治', '可治', '可以治', '可以医', '能治好吗', '可以治好吗', '会好吗',
                              '能好吗', '治愈吗']  # 询问治愈率
        self.check_qwds = ['检查什么', '检查项目', '哪些检查', '什么检查', '检查哪些', '项目', '检测什么',
                           '哪些检测', '检测哪些', '化验什么', '哪些化验', '化验哪些', '哪些体检', '怎么查找',
                           '如何查找', '怎么检查', '如何检查', '怎么检测', '如何检测']  # 询问检查项目
        self.belong_qwds = ['属于什么科', '什么科', '科室', '挂什么', '挂哪个', '哪个科', '哪些科']  # 询问科室
        self.disase_qwds = ['什么病', '啥病', '得了什么', '得了哪种', '怎么回事', '咋回事', '回事',
                            '什么情况', '什么问题', '什么毛病', '啥毛病', '哪种病']  # 询问疾病

    def build_actree(self, wordlist):
        """
        构造actree，加速过滤
        :param wordlist:
        :return:
        """
        actree = ahocorasick.Automaton()
        # 向树中添加单词
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def entity_reg(self, question):
        """
        模式匹配, 得到匹配的词和类型。如疾病，疾病别名，并发症，症状
        :param question:str
        :return:
        """
        self.result = {}

        for i in self.disease_tree.iter(question):
            word = i[1][1]
            if "Disease" not in self.result:
                self.result["Disease"] = [word]
            else:
                self.result["Disease"].append(word)

        for i in self.alias_tree.iter(question):
            word = i[1][1]
            if "Alias" not in self.result:
                self.result["Alias"] = [word]
            else:
                self.result["Alias"].append(word)

        for i in self.symptom_tree.iter(question):
            wd = i[1][1]
            if "Symptom" not in self.result:
                self.result["Symptom"] = [wd]
            else:
                self.result["Symptom"].append(wd)

        for i in self.complication_tree.iter(question):
            wd = i[1][1]
            if "Complication" not in self.result:
                self.result["Complication"] = [wd]
            else:
                self.result["Complication"].append(wd)

    def check_words(self, wds, sent):
        """
        基于特征词分类
        :param wds:
        :param sent:
        :return:
        """
        for wd in wds:
            if wd in sent:
                return True
        return False

    def tfidf_features(self, text, vectorizer):
        """
        提取问题的TF-IDF特征
        :param text:
        :param vectorizer:
        :return:
        """
        jieba.load_userdict(self.vocab_path)
        words = [w.strip() for w in jieba.cut(text) if w.strip() and w.strip() not in self.stopwords]
        sents = [' '.join(words)]

        tfidf = vectorizer.transform(sents).toarray()
        return tfidf

    def other_features(self, text):
        """
        提取问题的关键词特征
        :param text:
        :return:
        """
        features = [0] * 7
        for d in self.disase_qwds:
            if d in text:
                features[0] += 1

        for s in self.symptom_qwds:
            if s in text:
                features[1] += 1

        for c in self.cureway_qwds:
            if c in text:
                features[2] += 1

        for c in self.check_qwds:
            if c in text:
                features[3] += 1
        for p in self.lasttime_qwds:
            if p in text:
                features[4] += 1

        for r in self.cureprob_qwds:
            if r in text:
                features[5] += 1

        for d in self.belong_qwds:
            if d in text:
                features[6] += 1

        m = max(features)
        n = min(features)
        normed_features = []
        if m == n:
            normed_features = features
        else:
            for i in features:
                j = (i - n) / (m - n)
                normed_features.append(j)

        return np.array(normed_features)

        # 实体抽取主函数

    def extractor(self, question):
        self.entity_reg(question)

        types = []  # 实体类型
        for v in self.result.keys():
            types.append(v)

        intentions = []  # 查询意图

        # 已知疾病，查询症状
        if self.check_words(self.symptom_qwds, question) and ('Disease' in types or 'Alia' in types):
            intention = "query_symptom"
            intentions.append(intention)
        # 已知疾病或症状，查询治疗方法
        if self.check_words(self.cureway_qwds, question) and \
                ('Disease' in types or 'Symptom' in types or 'Alias' in types or 'Complication' in types):
            intention = "query_cureway"
            intentions.append(intention)
        # 已知疾病或症状，查询治疗周期
        if self.check_words(self.lasttime_qwds, question) and ('Disease' in types or 'Alias' in types):
            intention = "query_period"
            intentions.append(intention)
        # 已知疾病，查询治愈率
        if self.check_words(self.cureprob_qwds, question) and ('Disease' in types or 'Alias' in types):
            intention = "query_rate"
            intentions.append(intention)
        # 已知疾病，查询检查项目
        if self.check_words(self.check_qwds, question) and ('Disease' in types or 'Alias' in types):
            intention = "query_checklist"
            intentions.append(intention)
        # 查询科室
        if self.check_words(self.belong_qwds, question) and \
                ('Disease' in types or 'Symptom' in types or 'Alias' in types or 'Complication' in types):
            intention = "query_department"
            intentions.append(intention)
        # 已知症状，查询疾病
        if self.check_words(self.disase_qwds, question) and ("Symptom" in types or "Complication" in types):
            intention = "query_disease"
            intentions.append(intention)

        # 若没有检测到意图，且已知疾病，则返回疾病的描述
        if not intentions and ('Disease' in types or 'Alias' in types or 'Symptom' in types):
            # 使用文本分类模型
            for k in self.result.values():
                for v in k:
                    question = question.replace(v, "")

            intentions = class_predict.get_probability(question)
            if not intentions:
                intention = "disease_describe"
                if intention not in intentions:
                    intentions.append(intention)

        self.result["intentions"] = intentions

        return self.result
