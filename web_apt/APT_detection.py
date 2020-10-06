# -*- coding: utf-8 -*-
"""
Created on 2020/8/16 12:38

@author : dengcongyi0701@163.com

Description:

"""
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import pickle
import numpy as np
import string
import tld
import os
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve
from sklearn.svm import SVC
from xgboost import XGBClassifier
from keras.models import model_from_json
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from sklearn.metrics import precision_score, recall_score, classification_report, accuracy_score, f1_score
from feature_extraction import wash_tld, phishing_get_feature

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class XGBoost_classifier:

    def __init__(self):
        self.XGBoost_clf = XGBClassifier(max_depth=5, learning_rate=0.1, n_estimator=100, silent=True,
                                         objective='binary:logistic')
        self.standardScaler = StandardScaler()
        self.train_score = None
        self.isload_ = False

    def train(self, model_folder, train_feature_add):
        """
        XGBoost算法训练数据
        :param train_feature_add: 训练数据路径
        :param model_add:  模型存储路径
        :return:
        """
        train_df = pd.read_csv(train_feature_add, index_col=['domain_name'])
        train_df = train_df.fillna('0.0')
        x_train = train_df.drop(['label'], axis=1).values
        y_train = train_df['label'].values
        print("_______XGBoost Training_______")
        self.XGBoost_clf.fit(x_train, y_train)
        mal_scores = np.array(self.XGBoost_clf.predict_proba(x_train))[:, 1]
        mal_scores = sorted(mal_scores)
        np.save(r"{}/XGBoost_train_scores.npy".format(model_folder), mal_scores)
        pickle.dump(self.XGBoost_clf, open("{}/XGBoost_model.pkl".format(model_folder), 'wb'))

    def load(self, model_folder):
        """
        将模型文件和归一化尺度读取到内存中
        :param model_add: 模型存储路径
        :param standard_scaler_add: 归一化scaler存储路径
        :return:
        """
        self.XGBoost_clf = pickle.load(open("{}/XGBoost_model.pkl".format(model_folder), 'rb'))
        self.standardScaler = pickle.load(open("{}/standardscalar.pkl".format(model_folder), 'rb'))
        self.train_score = np.load(r"{}/XGBoost_train_scores.npy".format(model_folder))
        self.isload_ = True

    def predict(self, model_folder, test_feature_add):
        """
        测试集进行测试，计算准确率等
        :param test_feature_add: 测试数据路径
        :return:
        """
        self.load(model_folder)
        test_df = pd.read_csv(test_feature_add, index_col=['domain_name'])
        test_df = test_df.fillna('0.0')
        x_test = test_df.drop(['label'], axis=1).values
        y_test = test_df['label'].values
        print("_______XGBoost Predicting_______")
        y_predict = self.XGBoost_clf.predict(x_test)
        print("XGBoost accuracy: ", self.XGBoost_clf.score(x_test, y_test))
        print("XGBoost precision: ", precision_score(y_test, y_predict, average='macro'))
        print("XGBoost recall: ", recall_score(y_test, y_predict, average='macro'))
        print("XGBoost F1: ", f1_score(y_test, y_predict, average='macro'))
        print("XGBoost TPR, FPR, thresholds: ", roc_curve(y_test, y_predict, pos_label=1))

        plot_roc_curve(self.XGBoost_clf, x_test, y_test)
        plt.show()

    def predict_singleDN(self, model_folder, dname):
        """
        对单个域名进行检测，输出检测结果及恶意概率
        :param dname: 域名
        :return:
        """
        if not self.isload_:
            self.load(model_folder)
        dname = dname.strip('/').strip('.')
        dname = dname.replace("http://", '')        
        dname = dname.replace("www.", "")
        dname = wash_tld(dname)
        if dname == "":
            label = 0
            prob = 0.0000
            p_value = 1.0000
            print("\nxgboost sld:", dname)
            # print("label:", label)
            # print("mal_prob:", prob)
            # print("p_value:", p_value)
            print('label:{}, pro:{}, p_value:{}'.format(label, prob, p_value))
            return label, prob, p_value
        else:
            feature = self.standardScaler.transform(pd.DataFrame([phishing_get_feature(dname)]))
            label = self.XGBoost_clf.predict(feature)
            prob = self.XGBoost_clf.predict_proba(feature)
            p_value = cal_pValue(self.train_score, prob[0][1], label[0])
            print("\nxgboost sld:", dname)
            # print("label:", label[0])
            # print("mal_prob:", prob[0][1])
            # print("p_value:", p_value)
            print('label:{}, pro:{}, p_value:{}'.format(label[0], prob[0][1], p_value))
            return label[0], prob[0][1], p_value


def cal_pValue(score_list, key, label):
    """
    计算p_value
    :param score_list: 训练集得分列表
    :param key: 测试样本得分
    :param label: 测试样本标签
    :return: p_value, 保留四位小数
    """
    count = 0
    if label == 0:
        temp = sorted(score_list, reverse=1)
        score_list = [i for i in temp if i <= 0.5]
        left = 0
        right = len(score_list) - 1
        while left <= right:
            middle = (left+right)//2
            if key < score_list[middle]:
                left = middle + 1
            elif key > score_list[middle]:
                right = middle - 1
            else:
                count = middle + 1
                break
        count = left
    elif label == 1:
        temp = sorted(score_list, reverse=0)
        score_list = [i for i in temp if i > 0.5]
        left = 0
        right = len(score_list) - 1
        while left <= right:
            middle = (left+right)//2
            if key > score_list[middle]:
                left = middle + 1
            elif key < score_list[middle]:
                right = middle - 1
            else:
                count = middle + 1
                break
        count = left
    p_value = count/len(score_list)
    return round(p_value, 4)


class LSTM_classifier:
    def __init__(self):
        self.model = None
        self.valid_chars = {'q': 17, '0': 27, 'x': 24, 'd': 4, 'l': 12, 'm': 13, 'v': 22, 'n': 14, 'c': 3, 'g': 7, '7': 34, 'u': 21, '5': 32, 'p': 16, 'h': 8, 'b': 2, '6': 33, '-': 38, 'z': 26, '3': 30, 'f': 6, 't': 20, 'j': 10, '1': 28, '4': 31, 's': 19, 'o': 15, 'w': 23, '9': 36, 'r': 18, 'i': 9, 'e': 5, 'y': 25, 'a': 1, '.': 37, '2': 29, '_': 39, '8': 35, 'k': 11}
        self.maxlen = 178
        self.max_features = 40
        self.max_epoch = 20
        self.batch_size = 128
        self.tld_list = []
        with open(r'./data/tld.txt', 'r', encoding='utf8') as f:
            for i in f.readlines():
                self.tld_list.append(i.strip()[1:])

        score_df = pd.read_csv(r"./data/lstm_score_rank.csv", names=['score'])
        self.score_l = score_df['score'].tolist()

    def build_binary_model(self):
        """Build LSTM model for two-class classification"""
        self.model = Sequential()
        self.model.add(Embedding(self.max_features, 128, input_length=self.maxlen))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
        self.model.compile(loss='binary_crossentropy',optimizer='rmsprop')

    def load(self, model_add, model_weight_add):
        """
        将模型文件和权重值读取
        :param model_add: 模型存储路径
        :param model_weight_add: 权重存储路径
        :return:
        """
        with open(model_add, 'r') as json_file:
            model = json_file.read()
        self.model = model_from_json(model)
        self.model.load_weights(model_weight_add)

    def data_pro(self, url):
        """
        预处理字符串
        :param url:
        :return:
        """
        url = url.strip().strip('.').strip('/')
        url = url.replace("http://", '')
        print(url)
        url = url.split('/')[0]
        url = url.split('?')[0]
        url = url.split('=')[0]
        dn_list = url.split('.')
        for i in reversed(dn_list):
            if i in self.tld_list:
                dn_list.remove(i)
            elif i == 'www':
                dn_list.remove(i)
            else:
                continue
        short_url = ''.join(dn_list)
        short_url = short_url.replace('[', '').replace(']', '')
        short_url = short_url.lower()
        return short_url

    def cal_p(self, s):
        """
        计算p_value, 二分查找
        :param s: float
        :return:
        """
        flag = 0  # score偏da的对应的
        for i in range(len(self.score_l)):
            if self.score_l[i] <= 0.5000000000000000:
                flag = i - 1
                break
        # print("flag:{}".format(flag))
        if s >= self.score_l[0]:
            return 1.0
        if s <= self.score_l[-1]:
            return 1.0
        if s == self.score_l[flag]:
            # return 1 / ((flag + 1) * 1.0)
            return 0.0

        high_index = len(self.score_l)
        low_index = 0
        while low_index < high_index:
            mid = int((low_index + high_index) / 2)
            if s > self.score_l[mid]:
                high_index = mid - 1
            elif s == self.score_l[mid]:
                if s > 0.5:
                    return (flag - mid + 1) / ((flag + 1) * 1.0)
                else:
                    # return (len(self.score_l) - mid) / ((len(self.score_l) - flag - 1) * 1.0)
                    return (mid - flag) / ((len(self.score_l) - flag - 1) * 1.0)
            else:
                low_index = mid + 1
        if s > 0.5:
            # print(low_index, (flag - low_index), ((flag + 1) * 1.0))
            return (flag - low_index) / ((flag + 1) * 1.0)
        else:
            # print(low_index, len(score_l) - low_index, (len(score_l) - flag - 1) * 1.0)
            # return (len(self.score_l) - low_index) / ((len(self.score_l) - flag - 1) * 1.0)
            return (low_index - flag) / ((len(self.score_l) - flag - 1) * 1.0)

    def predict_singleDN(self, dname):
        """
        对单个域名进行检测，输出检测结果及恶意概率
        :param dname: 域名
        :return:
        """
        dname = dname.strip(string.punctuation)
        short_url = self.data_pro(dname)
        print("\nlstm sld-----{}".format(short_url))

        sld_int = [[self.valid_chars[y] for y in x] for x in [short_url]]
        sld_int = sequence.pad_sequences(sld_int, maxlen=self.maxlen)
        sld_np = np.array(sld_int)
        # 编译模型
        self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')
        if short_url == '':
            score = 0.0
            p_value = 1.0
            label = 0
            print('label:{}, pro:{}, p_value:{}'.format(label, score, p_value))
            return label, score, p_value
        else:
            scores = self.model.predict(sld_np)
            score = scores[0][0]
            p_value = self.cal_p(score)

            if score > 0.5:
                label = 1
            else:
                label = 0
            print('label:{}, pro:{}, p_value:{}'.format(label, score, p_value))
            return label, score, p_value


if __name__ == "__main__":
    XGBoost_model_add = r"./model/XGBoost_model.pkl"
    standard_scaler_add = r"./model/standardscalar.pkl"
    LSTM_model_add = r"./model/LSTM_model.json"
    LSTM_model_weight = r"./model/LSTM_model.h5"
    tld_path = r'./data/tld.txt'
    score_path = r"./data/lstm_score_rank.csv"
    phishing_train_add = r"./features/phishing_train_features.csv"
    phishing_test_add = r"./features/phishing_test_features.csv"
    phishing_model_folder = r"./model/phishing"


    LSTM_clf = LSTM_classifier()
    LSTM_clf.load(LSTM_model_add, LSTM_model_weight)
    # while True:
    #     a = input("请输入。。")
    #     re = LSTM_clf.predict_singleDN(a)
    #     print(re)

    XGBoost_clf = XGBoost_classifier()
    while True:
        a = input("请输入。。")
        print(a)
        re = XGBoost_clf.predict_singleDN(phishing_model_folder, a)
        # print(re)/
        LSTM_clf.predict_singleDN(a)

    # RF_clf.predict(test_add)
    # RF_clf.predict_singleDN("baijiahao.dsalkswjgoijdslk.com")
    # RF_clf.predict_singleDN("baijiahao.cnblog.org")

    # SVM_clf = SVM_classifier()
    # SVM_clf.load(SVM_model_add, SVM_standard_scaler_add)
    # SVM_clf.predict(test_add)
    # SVM_clf.predict_singleDN("baijiahao.dsalkswjgoijdslk.com")

    # XGBoost_clf = XGBoost_classifier()
    # XGBoost_clf.load(XGBoost_model_add, XGBoost_standard_scaler_add)
    # XGBoost_clf.predict(test_add)
    # XGBoost_clf.predict_singleDN("baijiahao.dsalkswjgoijdslk.com")
    # XGBoost_clf.predict_singleDN("baijiahao.cinblog.org")

    # LSTM_clf = LSTM_classifier()
    # LSTM_clf.load(LSTM_model_add, LSTM_model_weight)
    # LSTM_clf.predict_singleDN("baijiahao.dsalkswjgoijdslk.com")
    # LSTM_clf.predict_singleDN("baijiahao.cnblog.org")

