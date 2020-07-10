#!/usr/bin/env python
# --*-- encoding: utf-8

"""
@version: ??
@author: Andy
@file: run.py
@time: 20/2/7 14:49
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/detail')
def detail():
    return render_template('detail.html', labels=labels, \
            content=content, jlabels=jlabels, jcontent=jcontent)

@app.route('/search_data', methods=['post', 'get'])
def search_data():
    global labels
    global content
    global jlabels
    global jcontent
    S = request.get_data()
    # get annual sales rank
    print(S)
    T = bytes.decode(S)
    print(999999)
    print(T)
    df = pd.read_csv("./data/local_latest.csv")
    df["sha256"]=df["sha256"].astype("str")    
    df1 = df[df.sha256 == T]
    if df1.empty:
        labels = [T]
        content = ["病毒库没有此sha256数据"]
        jlabels = [T]
        jcontent = ["病毒库没有此json数据"] 
        return jsonify({"labels":labels,"content":content,"jlabels":jlabels,"jcontent":jcontent})
    labels = list(df1.columns.values)
    print(type(labels))
    print(labels)
    df1.reset_index(inplace=True)
    print(df1)
    print(66666)
    print(df1.loc[0,:])
    content = list(df1.loc[0,:])
    content = content[1:]
    print(type(content))
    print(content)
    print(8888888)
    j_df = pd.read_csv("./data/local_jsoninfo.csv")
    j_df["sha256"]=j_df["sha256"].astype("str")
    df2 = j_df[j_df.sha256 == T]
    if df2.empty:
        jlabels = [T]
        jcontent = ["病毒库没有此json数据"]
        return jsonify({"labels":labels,"content":content,"jlabels":jlabels,"jcontent":jcontent})
    jlabels = list(df2.columns.values)
    print(type(jlabels))
    print(jlabels)
    df2.reset_index(inplace=True)
    jcontent = list(df2.loc[0,:])
    jcontent = jcontent[1:]
    print(type(jcontent))
    print(jcontent)
    print(8888888)
    content=[str(i) for i in content]
    jcontent=[str(i) for i in jcontent]
    #return redirect(url_for('detail',labels=labels,content=content,jlabels=jlabels,jcontent=jcontent))
    return jsonify({"labels":labels,"contents":content,"jlabels":jlabels,"jcontents":jcontent})

def get_chart1_data():
    df = pd.read_csv('./data/size.csv')
    listBins = [0, 5, 10, 15, 20, 25, 30, 35, 10000]
    listLabels = ['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35以上']
    df['apk_size'] = pd.cut(df['apk_size'], bins=listBins, labels=listLabels, include_lowest=True)
    all_ = df.groupby(df['apk_size'])['all'].sum()
    malware = df.groupby(df['apk_size'])['malware'].sum()
    benign = df.groupby(df['apk_size'])['benign'].sum()
    print(8888)
    apk_size = pd.DataFrame({'all':all_,"malware":malware,"benign":benign})
    apk_size.reset_index(inplace=True)
    print(apk_size)
    chart1_data_list = list(apk_size["apk_size"])
    chart1_city_list = list(apk_size["all"])
    chart1_info = {}
    a = ['大小']
    b = ['全部']
    c = ['恶意']
    d = ['良性']
    chart1_info['x_name'] = a+ chart1_data_list
    chart1_confirm_list = b + list(apk_size['all'])
    chart1_suspect_list = c + list(apk_size['malware'])
    chart1_heal_list = d + list(df['benign'])
    chart1_info['confirm'] = chart1_confirm_list
    chart1_info['suspect'] = chart1_suspect_list
    chart1_info['heal'] = chart1_heal_list
    #print(chart1_info)
    return chart1_info


def get_chart2_data():
    chart2_dict = {}
    df = pd.read_csv('./data/vendors.csv')
    l1 = list(df["company"])
    l2 = list(df["count"])
    chart2_dict = dict(zip(l1,l2))
    chart2_data_list = sorted(chart2_dict.items(), key=lambda x: x[1], reverse=False)
    chart2_city_list = [x[0] for x in chart2_data_list[:5]]
    chart2_1_info = {}
    chart2_1_info['x_name'] = chart2_city_list
    chart2_1_info['data'] = chart2_data_list[:5]
    return chart2_1_info

def get_chart3_1_data():
    chart3_1_list = []
    df = pd.read_csv('./data/count.csv')
    chart3_class_list = list(df["vt_class"])
    chart3_confirm_list = list(df["count"])
    confirm = {'value': chart3_confirm_list[0], 'name': "良性"}
    dead = {'value': chart3_confirm_list[1], 'name': "恶意"}
    suspect = {'value': chart3_confirm_list[2], 'name': "未知"}
    chart3_1_list.append(confirm)
    chart3_1_list.append(dead)
    chart3_1_list.append(suspect)
    return chart3_1_list


def get_chart3_2_data():
    chart3_2_list = []
    df = pd.read_csv('./data/market.csv')
    chart3_class_list = list(df["markets"])[:5]
    chart3_confirm_list = list(df["count"])[:5]
    for i in range(len(chart3_class_list)):
        confirm = {'value': chart3_confirm_list[i], 'name': chart3_class_list[i]}
        chart3_2_list.append(confirm)
    return chart3_2_list


def get_chart3_3_data():
    chart3_3_list = []
    df = pd.read_csv('./data/type.csv')
    chart3_class_list = list(df["filetype"])
    chart3_confirm_list =list(df['count'])
    for i in range(len(chart3_class_list)):
        cured = {'value': chart3_confirm_list[i], 'name': chart3_class_list[i]}
        chart3_3_list.append(cured)
    return chart3_3_list

def get_chart4_data():
    df = pd.read_csv('./data/time.csv')
    df = df.loc[(df['date']>2010)&(df['date']<2021)]
    df = df.fillna(0)
    chart4_info = {}
    print(df)
    chart4_date_list = list(df['date'])
    chart4_confirm_list = list(df['all'])
    chart4_suspect_list = list(df['malware'])
    chart4_heal_list = list(df['benign'])
    chart4_info['x_name'] = chart4_date_list
    chart4_info['confirm'] = chart4_confirm_list
    chart4_info['suspect'] = chart4_suspect_list
    chart4_info['heal'] = chart4_heal_list
    return chart4_info

def get_chart5_data():
    df = pd.read_csv('./data/positives.csv')
    chart5_data_list = list(df['sha256'].apply(lambda x:x[:6]).tolist())
    chart5_city_list = list(df["positives"])
    chart5_info = {}
    chart5_info['x_name'] = chart5_data_list[:5]
    chart5_info['data'] = chart5_city_list[:5]
    return chart5_info

def get_chart5_1_data():
    chart5_dict = {}
    df = pd.read_csv('./data/vendors.csv')
    l1 = list(df["company"])
    l2 = list(df["count"])
    chart5_dict = dict(zip(l1,l2))
    chart5_data_list = sorted(chart5_dict.items(), key=lambda x: x[1], reverse=True)
    chart5_city_list = [x[0] for x in chart5_data_list[:5]]
    chart5_1_info = {}
    chart5_1_info['x_name'] = chart5_city_list
    chart5_1_info['data'] = chart5_data_list[:5]
    return chart5_1_info

@app.route('/get_ncov_totalcount')
def ncov_totalcount():
    df = pd.read_csv('./data/number.csv') 
    confirmedCount = df.iloc[0,2]
    print(989898)
    print(confirmedCount)
    suspectedCount = df.iloc[0,1]
    print(suspectedCount)
    return jsonify({'confirmedCount': confirmedCount, 'suspectedCount': suspectedCount})

@app.route('/get_chart_data')
def get_chart_data():
    chart_info = {}
    chart1_data = get_chart1_data()
    chart2_data = get_chart2_data()
    chart4_data = get_chart4_data()
    chart5_data = get_chart5_data()
    chart5_1_data = get_chart5_1_data()
    chart3_1_data = get_chart3_1_data()
    chart3_2_data = get_chart3_2_data()
    chart3_3_data = get_chart3_3_data()
    chart_info['chart1'] = chart1_data
    chart_info['chart2'] = chart2_data
    chart_info['chart5'] = chart5_data
    chart_info['chart4'] = chart4_data
    chart_info['chart5_1'] = chart5_1_data
    chart_info['chart3_1'] = chart3_1_data
    chart_info['chart3_2'] = chart3_2_data
    chart_info['chart3_3'] = chart3_3_data
    # print(33333)
    # print(chart_info)
    # print(type(chart_info))
    # a = jsonify(chart_info)
    return jsonify(chart_info)


if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, debug=True)
