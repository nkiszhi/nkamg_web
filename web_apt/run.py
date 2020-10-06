# -*-coding:utf-8 -*-
"""
@Author: liying
@Email: liying_china@163.com
@File: run.py
@Create Time: 2020/7/10 上午9:53
基于多模型的DGA检测
"""
import os

from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pandas as pd
import sys
from importlib import reload
from APT_detection import LSTM_classifier, XGBoost_classifier



reload(sys)
HOST_IP = "0.0.0.0"
PORT = 5004

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
    url = url.lower()
    print(url)
    l_lstm, pro_lstm, pval_lstm = LSTM_clf.predict_singleDN(url)
    l_lstm = str(l_lstm)
    pro_lstm = str(format(pro_lstm, '.4f'))
    pval_lstm = str(format(pval_lstm, '.4f'))
    l_xgb = 0
    pro_xgb = 0
    pval_xgb = 0
    try:
        l_xgb, pro_xgb, pval_xgb = XGBoost_clf.predict_singleDN(phishing_model_folder, url)
        l_xgb = str(l_xgb)
        pro_xgb = str(format(pro_xgb, '.4f'))
        pval_xgb = str(format(pval_xgb, '.4f'))
    except Exception as e:
        l_brf = '???'
        p_brf = '???'
        pval_xgb = '???'

    return jsonify({"lstm": [l_lstm, pro_lstm, pval_lstm], "xgboost": [l_xgb, pro_xgb, pval_xgb]})


if __name__ == '__main__':
    XGBoost_model_add = r"./model/XGBoost_model.pkl"
    XGBoost_standard_scaler_add = r"./model/RF_standardscalar.pkl"
    LSTM_model_add = r"./model/LSTM_model.json"
    LSTM_model_weight = r"./model/LSTM_model.h5"
    phishing_model_folder = r"./model/phishing"

    LSTM_clf = LSTM_classifier()
    LSTM_clf.load(LSTM_model_add, LSTM_model_weight)

    XGBoost_clf = XGBoost_classifier()

    app.run(host=HOST_IP, port=PORT, debug=True)
