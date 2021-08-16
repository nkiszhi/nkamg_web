"""
网页首页
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pandas as pd
import sys
from importlib import reload
import os

reload(sys)
#sys.setdefaultencoding('utf8')
#HOST_IP = "60.205.204.64"
HOST_IP = "0.0.0.0"
PORT = 5003

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


def data_pro(normal, abnormal):
    """
    返回json格式数据
    :param data:
    :return:
    """
    lss = []
    tmp = {}
    for i in range(len(normal)):
        dic = []
        dic.append(str(normal['0'][i]))
        dic.append(str(normal['1'][i]))
        dic.append(str(normal['2'][i]))
        dic.append(str(normal.index[i]))
        lss.append(dic)
    tmp['normal'] = lss

    lssd = []
    for i in range(len(abnormal)):
        dic = []
        dic.append(str(abnormal['0'][i]))
        dic.append(str(abnormal['1'][i]))
        dic.append(str(abnormal['2'][i]))
        dic.append(str(abnormal.index[i]))
        lssd.append(dic)
    tmp['abnormal'] = lssd
    print('safe:{}'.format(len(tmp['normal'])))
    print('danger:{}'.format(len(tmp['abnormal'])))
    return tmp


@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/knn')
def knn():
    return render_template('/knn_result.html')

@app.route('/get_knn')
def get_knn_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/KNN_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/KNN_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)


@app.route('/get_pca')
def get_pca_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/PCA_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/PCA_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)


@app.route('/get_vae')
def get_vae_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/VAE_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/VAE_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)

@app.route('/get_lof')
def get_lof_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/LOF_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/LOF_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)

@app.route('/get_iforest')
def get_iforest_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/IForest_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/IForest_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)

@app.route('/get_autoencoder')
def get_autoencoder_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/AutoEncoder_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/AutoEncoder_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)

@app.route('/get_feature')
def get_feature_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/FeatureBagging_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/FeatureBagging_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)


@app.route('/get_abod')
def get_abod_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/ABOD_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/ABOD_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)


@app.route('/get_hbos')
def get_hbos_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/HBOS_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/HBOS_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)


@app.route('/get_cblof')
def get_cblof_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/CBLOF_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/CBLOF_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)

@app.route('/get_loda_al')
def get_loda_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/LODA_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/LODA_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)


@app.route('/get_mcd')
def get_mcd_data():
    a = os.path.dirname(__file__)
    normal = pd.read_csv(a + '/data/MCD_normal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    abnormal = pd.read_csv(a + '/data/MCD_abnormal.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    response_info = data_pro(normal, abnormal)
    return jsonify(response_info)


if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, debug=True)