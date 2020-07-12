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
PORT = 5001

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


if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, debug=True)
