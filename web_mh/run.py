# -*-coding:utf-8 -*-
"""
@Author: liying
@Email: liying_china@163.com
@File: run.py
@Create Time: 2020/7/10 上午9:53
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
def graph_ip():
    return render_template('/graph_ip.html')


def map_rate(x, to_min, to_max, max_num, min_num):
    """
    将指定的访问次数映射到区间范围，作为点的大小
    :param x:
    :return:
    """
    return round(to_min + ((to_max - to_min) / (max_num - min_num)) * (x - min_num), 1)


@app.route('/get_name')
def get_name_data():
    """
    设置点
    分段设置点size:
        因为一共有200个网段，网段的访问次数最小为1,最大为1千万，因此进行划分
        访问次数<100，size均为20
        100~一千万， 进行啦分段映射
        大于一千万，size为110
    category按照访问次数进行划分
    :return:
    """
    a = os.path.dirname(__file__)
    file_dir = a + '/data/IP_merge.csv'
    name_df = pd.read_csv(file_dir)
    ls = {}
    lss = []

    max_num = max(name_df['total'])
    min_num = min(name_df['total'])

    for i in range(0, len(name_df)):
        dic = {}
        symbol = 0
        dic['name'] = str(name_df.iloc[:, 0][i])
        ###########点被划分为5类，看total访问数###############
        if name_df['total'][i] <= 100:
            symbol = str(10)
            dic['category'] = "访问量：小于100"
            # dic['itemStyle'] = {"normal": {'color': '#FFCC99'}}
        elif name_df['total'][i] > 100 and name_df['total'][i] <= 10000:
            symbol = str(map_rate(name_df['total'][i], 15, 25, max_num, min_num))
            dic['category'] = "访问量：100～1万"
        elif name_df['total'][i] > 10000 and name_df['total'][i] <= 100000:
            symbol = str(map_rate(name_df['total'][i], 30, 40, max_num, min_num))
            dic['category'] = "访问量：1万～10万"
        elif name_df['total'][i] > 100000 and name_df['total'][i] <= 1000000:
            symbol = str(map_rate(name_df['total'][i], 45, 55, max_num, min_num))
            dic['category'] = "访问量：10万～100万"
        elif name_df['total'][i] > 10000 and name_df['total'][i] <= 10000000:
            symbol = str(map_rate(name_df['total'][i], 60, 70, max_num, min_num))
            dic['category'] = "访问量：100万～1000万"
        elif name_df['total'][i] > 10000000 and name_df['total'][i] <= 100000000:
            symbol = str(75)
            dic['category'] = "访问量：1000万～1亿"
        elif name_df['total'][i] > 100000000:
            symbol = str(90)
            dic['category'] = "访问量：大于1亿"

        dic['symbolSize'] = symbol

        lss.append(dic)

    ################按照访问total分为5类############
    category_list = []
    category_list.append({'name': "访问量：大于1亿"})
    category_list.append({'name': "访问量：1000万～1亿"})
    category_list.append({'name': "访问量：100万～1000万"})
    category_list.append({'name': "访问量：10万～100万"})
    category_list.append({'name': "访问量：1万～10万"})
    category_list.append({'name': "访问量：100～1万"})
    category_list.append({'name': "访问量：小于100"})
    ls['key'] = lss
    ls['cat'] = category_list

    return jsonify(ls)


@app.route('/get_link')
def get_link_data():
    """
    设置边
    :return:
    """
    a = os.path.dirname(__file__)
    file_dir = a + '/data/IP_relation_total.csv'
    link_df = pd.read_csv(file_dir)
    ls = {}
    lss = []
    for i in range(0, len(link_df)):
        dic = {}
        dic['source'] = str(link_df['src_IP'][i])
        dic['target'] = str(link_df['des_IP'][i])
        dic['value'] = str(link_df['count_re'][i])
        lss.append(dic)
    ls['key'] = lss
    return jsonify(ls)


@app.route('/get_knn')
def get_knn_data():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    safe = pd.read_csv(a + '/data/KNN_safe.csv')
    dangerous = pd.read_csv(a + '/data/KNN_dangerous.csv')
    lss = []
    tmp = {}
    for i in range(len(safe)):
        dic = []
        dic.append(str(safe['0'][i]))
        dic.append(str(safe['1'][i]))
        dic.append(str(safe['2'][i]))
        dic.append(str(safe['IP'][i]))
        lss.append(dic)
    tmp['safe'] = lss

    lssd = []
    for i in range(len(dangerous)):
        dic = []
        dic.append(str(dangerous['0'][i]))
        dic.append(str(dangerous['1'][i]))
        dic.append(str(dangerous['2'][i]))
        dic.append(str(dangerous['IP'][i]))
        lssd.append(dic)
    tmp['dangerous'] = lssd

    sus = dangerous['IP'][:]
    top10 = sus.value_counts()[:10]
    lse = []
    sum_n = 0
    for i in range(len(top10)):
        sum_n += top10[i]
        dic = {"name": str(top10.index[i]), 'value': str(top10[i])}
        lse.append(dic)
    other_sum = len(lssd) - sum_n
    lse.append({"name": "其他IP", 'value': str(other_sum)})
    tmp['knn_bing'] = lse

    return jsonify(tmp)


@app.route('/get_pca')
def get_pca_data():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    safe = pd.read_csv(a + '/data/PCA_safe.csv')
    dangerous = pd.read_csv(a + '/data/PCA_dangerous.csv')
    lss = []
    tmp = {}
    for i in range(len(safe)):
        dic = []
        dic.append(str(safe['0'][i]))
        dic.append(str(safe['1'][i]))
        dic.append(str(safe['2'][i]))
        dic.append(str(safe['IP'][i]))
        lss.append(dic)
    tmp['safe'] = lss

    lssd = []
    for i in range(len(dangerous)):
        dic = []
        dic.append(str(dangerous['0'][i]))
        dic.append(str(dangerous['1'][i]))
        dic.append(str(dangerous['2'][i]))
        dic.append(str(dangerous['IP'][i]))
        lssd.append(dic)
    tmp['dangerous'] = lssd

    sus = dangerous['IP'][:]
    top10 = sus.value_counts()[:10]
    lse = []
    sum_n = 0
    for i in range(len(top10)):
        sum_n += top10[i]
        dic = {"name": str(top10.index[i]), 'value': str(top10[i])}
        lse.append(dic)
    other_sum = len(lssd) - sum_n
    lse.append({"name": "其他IP", 'value': str(other_sum)})
    tmp['pca_bing'] = lse

    return jsonify(tmp)


@app.route('/get_lof')
def get_lof_data():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    safe = pd.read_csv(a + '/data/LOF_safe.csv')
    dangerous = pd.read_csv(a + '/data/LOF_dangerous.csv')
    lss = []
    tmp = {}
    for i in range(len(safe)):
        dic = []
        dic.append(str(safe['0'][i]))
        dic.append(str(safe['1'][i]))
        dic.append(str(safe['2'][i]))
        dic.append(str(safe['IP'][i]))
        lss.append(dic)
    tmp['safe'] = lss

    lssd = []
    for i in range(len(dangerous)):
        dic = []
        dic.append(str(dangerous['0'][i]))
        dic.append(str(dangerous['1'][i]))
        dic.append(str(dangerous['2'][i]))
        dic.append(str(dangerous['IP'][i]))
        lssd.append(dic)
    tmp['dangerous'] = lssd

    sus = dangerous['IP'][:]
    top10 = sus.value_counts()[:10]
    lse = []
    sum_n = 0
    for i in range(len(top10)):
        sum_n += top10[i]
        dic = {"name": str(top10.index[i]), 'value': str(top10[i])}
        lse.append(dic)
    other_sum = len(lssd) - sum_n
    lse.append({"name": "其他IP", 'value': str(other_sum)})
    tmp['pca_bing'] = lse

    return jsonify(tmp)


@app.route('/get_vae')
def get_vae_data():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    safe = pd.read_csv(a + '/data/VAE_safe.csv')
    dangerous = pd.read_csv(a + '/data/VAE_dangerous.csv')
    lss = []
    tmp = {}
    for i in range(len(safe)):
        dic = []
        dic.append(str(safe['0'][i]))
        dic.append(str(safe['1'][i]))
        dic.append(str(safe['2'][i]))
        dic.append(str(safe['IP'][i]))
        lss.append(dic)
    tmp['safe'] = lss

    lssd = []
    for i in range(len(dangerous)):
        dic = []
        dic.append(str(dangerous['0'][i]))
        dic.append(str(dangerous['1'][i]))
        dic.append(str(dangerous['2'][i]))
        dic.append(str(dangerous['IP'][i]))
        lssd.append(dic)
    tmp['dangerous'] = lssd

    sus = dangerous['IP'][:]
    top10 = sus.value_counts()[:10]
    lse = []
    sum_n = 0
    for i in range(len(top10)):
        sum_n += top10[i]
        dic = {"name": str(top10.index[i]), 'value': str(top10[i])}
        lse.append(dic)
    other_sum = len(lssd) - sum_n
    lse.append({"name": "其他IP", 'value': str(other_sum)})
    tmp['pca_bing'] = lse

    return jsonify(tmp)


@app.route('/get_scan_230')
def get_scan_data():
    """
        427个点
    10.12.1.230:235
    10.12.80.87:155
    :return:
    """
    a = os.path.dirname(__file__)
    file_dir = a + '/data/scan_1_230.csv'
    name_df = pd.read_csv(file_dir)
    src_ip = name_df['src_ip']  #.groupby('src_ip')
    dst_ip = name_df['dst_ip']

    count_data = src_ip.value_counts()[:5]
    count_data = count_data.index  # 联系数量排名前5的ip
    dst_count_list = []  # 前5的ip涉及到的所有点
    for i in range(len(src_ip)):
        if src_ip[i] in count_data:
            dst_count_list.append(dst_ip[i])
    dst_count_list.append(count_data[0])
    dst_count_list.append(count_data[1])
    dst_count_list.append(count_data[2])
    dst_count_list.append(count_data[3])
    dst_count_list.append(count_data[4])
    all_ip = list(set(dst_count_list))

    lss = {}
    ls = []
    for i in range(len(all_ip)):
        dic = {}
        dic['name'] = str(all_ip[i])
        if str(all_ip[i]) == '10.12.1.230':
            dic['category'] = '10.12.1.230(可疑IP)'
            dic['symbolSize'] = '30'
        elif str(all_ip[i]) in count_data:
            dic['category'] = str(all_ip[i])
            dic['symbolSize'] = '25'
        else:
            dic['category'] = 'other'
            dic['symbolSize'] = '10'
        ls.append(dic)
    lss['key'] = ls
    li = []
    for i in range(len(src_ip.values)):
        if str(src_ip[i]) in count_data:
            dic = {}
            dic['source'] = str(src_ip[i])
            dic['target'] = str(dst_ip[i])
            li.append(dic)
    lss['link'] = li

    lsc = []
    for i in count_data:
        dic = {}
        if str(i) == '10.12.1.230':
            dic['name'] = str(i) + '(可疑IP)'
        else:
            dic['name'] = str(i)
        lsc.append(dic)
    lsc.append({'name': 'other'})
    lss['cat'] = lsc
    return jsonify(lss)


@app.route('/get_scan_37')
def get_scan_data_37():
    """
    389个点
    10.12.1.37:194
    10.12.80.87:160
    :return:
    """
    a = os.path.dirname(__file__)
    file_dir = a + '/data/scan_1_37.csv'
    name_df = pd.read_csv(file_dir)
    src_ip = name_df['src_ip']  # .groupby('src_ip')
    dst_ip = name_df['dst_ip']

    count_data = src_ip.value_counts()[:5]
    count_data = count_data.index  # 联系数量排名前5的ip
    dst_count_list = []  # 前5的ip涉及到的所有点
    for i in range(len(src_ip)):
        if src_ip[i] in count_data:
            dst_count_list.append(dst_ip[i])
    dst_count_list.append(count_data[0])
    dst_count_list.append(count_data[1])
    dst_count_list.append(count_data[2])
    dst_count_list.append(count_data[3])
    dst_count_list.append(count_data[4])
    all_ip = list(set(dst_count_list))

    lss = {}
    ls = []
    for i in range(len(all_ip)):
        dic = {}
        dic['name'] = str(all_ip[i])
        if str(all_ip[i]) == '10.12.1.37':
            dic['category'] = '10.12.1.37(可疑IP)'
            dic['symbolSize'] = '30'
        elif str(all_ip[i]) in count_data:
            dic['category'] = str(all_ip[i])
            dic['symbolSize'] = '25'
        else:
            dic['category'] = 'other'
            dic['symbolSize'] = '10'
        ls.append(dic)
    lss['key'] = ls
    li = []
    for i in range(len(src_ip.values)):
        if str(src_ip[i]) in count_data:
            dic = {}
            dic['source'] = str(src_ip[i])
            dic['target'] = str(dst_ip[i])
            li.append(dic)
    lss['link'] = li

    lsc = []
    for i in count_data:
        dic = {}
        if str(i) == '10.12.1.37':
            dic['name'] = str(i) + '(可疑IP)'
        else:
            dic['name'] = str(i)
        lsc.append(dic)
    lsc.append({'name': 'other'})
    lss['cat'] = lsc
    return jsonify(lss)

if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, debug=True)
