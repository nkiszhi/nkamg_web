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


@app.route('/get_name')
def get_name_data():
    name_df = pd.read_csv('./data/focus_name.csv')
    ls = {}
    lss = []
    for i in range(0, len(name_df)):
        dic = {}
        dic['name'] = str(name_df['name'][i])
        dic['category'] = str(name_df['category'][i])
        dic['symbolSize'] = str(name_df['symbolSize'][i])
        lss.append(dic)
    ls['key'] = lss
    return jsonify(ls)


@app.route('/get_link')
def get_link_data():
    link_df = pd.read_csv('./data/focus_links.csv')
    ls = {}
    lss = []
    for i in range(0, len(link_df)):
        dic = {}
        dic['source'] = str(link_df['source'][i])
        dic['target'] = str(link_df['target'][i])
        lss.append(dic)
    ls['key'] = lss
    return jsonify(ls)


if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, debug=True)
