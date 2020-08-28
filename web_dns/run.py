# -*-coding:utf-8 -*-
"""
@Author: liying
@Email: liying_china@163.com
@File: run.py
@Create Time: 2020/7/10 上午9:53
基于多模型的DGA检测
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pandas as pd
import sys
from importlib import reload
from DGA_detection import LSTM_classifier, XGBoost_classifier, RF_classifier, SVM_classifier
import os

reload(sys)
HOST_IP = "0.0.0.0"
PORT = 5000

app = Flask(__name__)

labels = None
content = None
jlabels = None
jcontent = None


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return int(obj)
        if isinstance(obj, str):
            return str(obj)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_result', methods=['GET', 'POST'])
def get_result():
    """
    获取文本框的输入值
    判断是否合格
    如果合格输入模型，返回结果
    :return:
    """
    url = request.form.get("input_val")
    l_lstm, p_lstm = LSTM_clf.predict_singleDN(url)
    l_lstm = str(l_lstm)
    p_lstm = str(format(p_lstm, '.4f'))
    l_xgb, p_xgb = XGBoost_clf.predict_singleDN(url)
    l_xgb = str(l_xgb)
    p_xgb = str(format(p_xgb, '.4f'))
    l_brf, p_brf = RF_clf.predict_singleDN(url)
    l_brf = str(l_brf)
    p_brf = str(format(p_brf, '.4f'))
    l_svm, p_svm = SVM_clf.predict_singleDN(url)
    l_svm = str(l_svm)
    p_svm = str(format(p_svm, '.4f'))

    return jsonify({"lstm": [l_lstm, p_lstm], "xgboost": [l_xgb, p_xgb], "brf": [l_brf, p_brf], "svm":[l_svm, p_svm]})


if __name__ == '__main__':
    RF_model_add = r"./model/RF_model.pkl"
    RF_standard_scaler_add = r"./model/RF_standardscalar.pkl"
    SVM_model_add = r"./model/SVM_model.pkl"
    SVM_standard_scaler_add = r"./model/RF_standardscalar.pkl"
    XGBoost_model_add = r"./model/XGBoost_model.pkl"
    XGBoost_standard_scaler_add = r"./model/RF_standardscalar.pkl"
    LSTM_model_add = r"./model/LSTM_model.json"
    LSTM_model_weight = r"./model/LSTM_model.h5"

    XGBoost_clf = XGBoost_classifier()
    XGBoost_clf.load(XGBoost_model_add, XGBoost_standard_scaler_add)

    RF_clf = RF_classifier()
    RF_clf.load(RF_model_add, RF_standard_scaler_add)

    SVM_clf = SVM_classifier()
    SVM_clf.load(SVM_model_add, SVM_standard_scaler_add)

    LSTM_clf = LSTM_classifier()
    LSTM_clf.load(LSTM_model_add, LSTM_model_weight)

    app.run(host=HOST_IP, port=PORT, debug=True)