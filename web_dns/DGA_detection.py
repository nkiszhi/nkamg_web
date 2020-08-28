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

from feature_extraction import get_feature

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 二分类随机森林(B_RF)算法
class RF_classifier:

    def __init__(self):
        self.RF_clf = RandomForestClassifier(n_estimators=100, criterion='entropy',
                                             random_state=23, n_jobs=-1, max_features=20)
        self.standardScaler = StandardScaler()


    def load(self, model_add, standard_scaler_add):
        """
        将模型文件和归一化尺度读取到内存中
        :param model_add: 模型存储路径
        :param standard_scaler_add: 归一化scaler存储路径
        :return:
        """
        self.RF_clf = pickle.load(open(model_add, 'rb'))
        self.standardScaler = pickle.load(open(standard_scaler_add, 'rb'))

    def predict(self, test_feature_add):
        """
        测试集进行测试，计算准确率等
        :param test_feature_add: 测试数据路径
        :return:
        """
        test_df = pd.read_csv(test_feature_add, index_col=['domain_name'])
        test_df = test_df.fillna('0.0')
        x_test = test_df.drop(['label'], axis=1).values
        y_test = test_df['label'].values
        print("_______RF Predicting_______")
        y_predict = self.RF_clf.predict(x_test)
        print("RF accuracy: ", self.RF_clf.score(x_test, y_test))
        print("RF precision: ", precision_score(y_test, y_predict, average='macro'))
        print("RF recall: ", recall_score(y_test, y_predict, average='macro'))
        print("RF F1: ", f1_score(y_test, y_predict, average='macro'))
        print("RF TPR, FPR, thresholds: ", roc_curve(y_test, y_predict, pos_label=1))

    def predict_singleDN(self, dname):
        """
        对单个域名进行检测，输出检测结果及恶意概率
        :param dname: 域名
        :return:
        """
        feature = self.standardScaler.transform(pd.DataFrame([get_feature(dname)]))
        label = self.RF_clf.predict(feature)
        prob = self.RF_clf.predict_proba(feature)
        return label[0], prob[0][1]


# SVM算法
class SVM_classifier:

    def __init__(self):
        # 目前先用RF特征
        self.SVM_clf = SVC(kernel='linear', probability=True, random_state=23)
        self.standard_scaler_add = StandardScaler()
        
    def load(self, model_add, standard_scaler_add):
        """
        将模型文件和归一化尺度读取到内存中
        :param model_add: 模型存储路径
        :param standard_scaler_add: 归一化scaler存储路径
        :return:
        """
        self.SVM_clf = pickle.load(open(model_add, 'rb'))
        self.standardScaler = pickle.load(open(standard_scaler_add, 'rb'))		
    
    def predict(self):
        """
        对测试集进行测试，计算准确率等
        :return:
        """
        test_df = pd.read_csv(self.test_feature_add, index_col=['domain_name'])
        test_df = test_df.fillna('0.0')
        x_test = test_df.drop(['label'], axis=1).values
        y_test = test_df['label'].values
        self.SVM_clf = pickle.load(open(self.model_add, 'rb'))
        print("_______SVM Predicting_______")
        y_predict = self.SVM_clf.predict(x_test)
        print("SVM accuracy: ", self.SVM_clf.score(x_test, y_test))
        print("SVM precision: ", precision_score(y_test, y_predict, average='macro'))
        print("SVM recall: ", recall_score(y_test, y_predict, average='macro'))
        print("SVM F1: ", f1_score(y_test, y_predict, average='macro'))
        print("SVM TPR, FPR, thresholds: ", roc_curve(y_test, y_predict, pos_label=1))

    def predict_singleDN(self, dname):
        """
        对单个域名进行检测，输出检测结果及恶意概率
        :param dname: 域名
        :return:
        """
        #self.SVM_clf = pickle.load(open(self.model_add, 'rb'))
        #standardScaler = pickle.load(open(self.standard_scaler_add, 'rb'))
        feature = self.standardScaler.transform(pd.DataFrame([get_feature(dname)]))
        label = self.SVM_clf.predict(feature)
        prob = self.SVM_clf.predict_proba(feature)
        print("label:", label[0])
        print("mal_prob:", prob[0][1])
        return label[0], prob[0][1]
		
		
# XGBoost算法
class XGBoost_classifier:

    def __init__(self):
        # 目前先用RF特征
        self.XGBoost_clf = XGBClassifier(max_depth=5, learning_rate=0.1, n_estimator=100, silent=True,
                                         objective='binary:logistic')
        self.standardScaler = StandardScaler()


    def load(self, model_add, standard_scaler_add):
        """
        将模型文件和归一化尺度读取到内存中
        :param model_add: 模型存储路径
        :param standard_scaler_add: 归一化scaler存储路径
        :return:
        """
        self.XGBoost_clf = pickle.load(open(model_add, 'rb'))
        self.standardScaler = pickle.load(open(standard_scaler_add, 'rb'))

    def predict(self, test_feature_add):
        """
        测试集进行测试，计算准确率等
        :param test_feature_add: 测试数据路径
        :return:
        """
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

    def predict_singleDN(self, dname):
        """
        对单个域名进行检测，输出检测结果及恶意概率
        :param dname: 域名
        :return:
        """
        feature = self.standardScaler.transform(pd.DataFrame([get_feature(dname)]))
        label = self.XGBoost_clf.predict(feature)
        prob = self.XGBoost_clf.predict_proba(feature)
        return label[0], prob[0][1]


class LSTM_classifier:
    def __init__(self):
        self.model = None
        self.valid_chars = valid_chars = {'q': 17, '0': 27, 'x': 24, 'd': 4, 'l': 12, 'm': 13, 'v': 22, 'n': 14, 'c': 3, 'g': 7, '7': 34, 'u': 21, '5': 32, 'p': 16, 'h': 8, 'b': 2, '6': 33, '-': 38, 'z': 26, '3': 30, 'f': 6, 't': 20, 'j': 10, '1': 28, '4': 31, 's': 19, 'o': 15, 'w': 23, '9': 36, 'r': 18, 'i': 9, 'e': 5, 'y': 25, 'a': 1, '.': 37, '2': 29, '_': 39, '8': 35, 'k': 11}
        self.maxlen = 63
        self.max_features = 40
        self.max_epoch = 20
        self.batch_size = 128

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

    def predict_singleDN(self, dname):
        """
        对单个域名进行检测，输出检测结果及恶意概率
        :param dname: 域名
        :return:
        """
        dname = dname.strip(string.punctuation)
        sld = ''
        try:
            sld = str(tld.get_tld(dname, as_object=True, fix_protocol=True).domain)
        except Exception as e:
            na_list = dname.split(".")
            sld = str(na_list[-2])
        print(sld)
        # 编译模型
        self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')

        sld_int = [[self.valid_chars[y] for y in x] for x in [sld]]
        sld_int = sequence.pad_sequences(sld_int, maxlen=self.maxlen)
        sld_np = np.array(sld_int)
        # predict
        scores = self.model.predict(sld_np)
        label = [0 if scores[0][0] <= 0.5 else 1]
        return label[0], scores[0][0]


if __name__ == "__main__":
    RF_model_add = r"./model/RF_model.pkl"
    RF_standard_scaler_add = r"./model/RF_standardscalar.pkl"
    SVM_model_add = r"./model/SVM_model.pkl"
    SVM_standard_scaler_add = r"./model/RF_standardscalar.pkl"
    XGBoost_model_add = r"./model/XGBoost_model.pkl"
    XGBoost_standard_scaler_add = r"./model/RF_standardscalar.pkl"
    LSTM_model_add = r"./model/LSTM_model.json"
    LSTM_model_weight = r"./model/LSTM_model.h5"


    LSTM_clf = LSTM_classifier()
    LSTM_clf.load(LSTM_model_add, LSTM_model_weight)
    while True:
        a = input("请输入。。")
        re = LSTM_clf.predict_singleDN(a)
        print(re)
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

