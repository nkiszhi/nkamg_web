#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on 2022/1/3 13:35

__author__ = "Ying Li"
__copyright__ = "Copyright (c) 2021 NKAMG"
__license__ = "GPL"
__contact__ = ""

Description:

"""

from flask import Flask, render_template, request
import json
import sys
import imp
import re
from configparser import ConfigParser
from dga_detection import MultiModelDetection

cp = ConfigParser()
cp.read('config.ini')
HOST_IP = cp.get('ini', 'ip')
PORT = int(cp.get('ini', 'port'))
ROW_PER_PAGE = int(cp.get('ini', 'row_per_page'))
detector = MultiModelDetection()

imp.reload(sys)
app = Flask(__name__)


list_info = []

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return int(obj)
        if isinstance(obj, str):
            return str(obj)


def get_page_info(list_info, offset=0, per_page=ROW_PER_PAGE):
    return list_info[offset: offset + per_page]


@app.route('/')
def show_index():
    return render_template('malware_url_query.html')


@app.route('/malware_url')
def show_malUrl():
    return render_template("malware_url_query.html")


@app.route('/malware_reuslt', methods=["POST"])
def detect_url():
    # 1. get url string
    url_str = request.form["url"].strip()
    # 2. validate string
    if url_str == '':
        return render_template("malware_url_result.html",
                           status=400, url=url_str,
                           message="域名不可为空!!")
    validate = re.match(r"^[A-Za-z0-9._\-]*$", url_str)
    if validate == None:
        return render_template("malware_url_result.html",
                               status=401, url=url_str,
                               message="域名格式不正确，域名中只能包含下划线、短横线、点、字母、数字，请输入正确域名！！")


    results = detector.multi_predict_single_dname(url_str)
    return render_template("malware_url_result.html", status=200, url=url_str, base_result=results[0],
                           result=results[1])


if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, threaded=True)

