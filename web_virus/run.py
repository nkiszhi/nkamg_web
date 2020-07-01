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
from GetData import get_latest_data, get_latest_malware_data, get_latest_benign_data, get_latest_date, get_latest_market, get_latest_malware_date, get_latest_benign_date, get_samples_class, get_samples_filetype, get_malware_json_report, get_json_positives_report, get_samples_count

#HOST_IP = "60.205.204.64"
HOST_IP = "172.17.112.126"
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
    df = pd.read_csv("0000_latest.csv")
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
    j_df = pd.read_csv("jsoninfo.csv")
    j_df["sha256"]=j_df["sha256"].astype("str")
    df2 = df[j_df.sha256 == T]
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
    df = get_latest_data()
    df1 = get_latest_malware_data()
    df2 = get_latest_benign_data()
    result = df.merge(df1, how='left',on="apk_size")
    result1 = result.merge(df2,how='left',on='apk_size')
    #print(result1)
    chart1_data_list = list(result1["apk_size"])
    chart1_city_list = list(result1["count"])
    chart1_info = {}
    a = ['大小']
    b = ['全部']
    c = ['恶意']
    d = ['良性']
    chart1_info['x_name'] = a+ chart1_data_list
    chart1_confirm_list = b + list(result1['count'])
    chart1_suspect_list = c + list(result1['m_count'])
    chart1_heal_list = d + list(result1['b_count'])
    chart1_info['confirm'] = chart1_confirm_list
    chart1_info['suspect'] = chart1_suspect_list
    chart1_info['heal'] = chart1_heal_list
    print(777777)
    #print(chart1_info)
    return chart1_info


def get_chart2_data():
    df = get_latest_date()
    chart2_info = {}
    chart2_date_list = list(df["dex_date"])
    chart2_confirm_list = list(df["count"])
    chart2_info['x_name'] = chart2_date_list
    chart2_info['data'] = chart2_confirm_list
    return chart2_info



def get_chart3_1_data():
    chart3_1_list = []
    df = get_samples_class()
    chart3_class_list = list(df["fileclass"])
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
    df = get_latest_market()
    chart3_class_list = list(df["markets"])
    chart3_confirm_list = list(df["count"])
    for i in range(len(chart3_class_list)):
        confirm = {'value': chart3_confirm_list[i], 'name': chart3_class_list[i]}
        chart3_2_list.append(confirm)
    return chart3_2_list


def get_chart3_3_data():
    chart3_3_list = []
    df = get_samples_filetype()
    chart3_class_list = list(df["filetype"])
    chart3_confirm_list =list(df['count'])
    for i in range(len(chart3_class_list)):
        cured = {'value': chart3_confirm_list[i], 'name': chart3_class_list[i]}
        chart3_3_list.append(cured)
    return chart3_3_list

def get_chart4_data():
    df = get_latest_date()
    df1 = get_latest_malware_date()
    df2 = get_latest_benign_date()
    result = df.merge(df1, how='left',on="dex_date")
    result1 = result.merge(df2,how='left',on='dex_date')
    result1=result1.fillna(0)
    chart4_info = {}
    print(result1)
    chart4_date_list = list(result1['dex_date'])
    chart4_confirm_list = list(result1['count'])
    chart4_suspect_list = list(result1['m_count'])
    chart4_heal_list = list(result1['b_count'])
    chart4_info['x_name'] = chart4_date_list
    chart4_info['confirm'] = chart4_confirm_list
    chart4_info['suspect'] = chart4_suspect_list
    chart4_info['heal'] = chart4_heal_list
    return chart4_info

def get_chart5_data():
    df = get_json_positives_report()
    chart5_data_list = list(df['sha256'].apply(lambda x:x[:6]).tolist())
    chart5_city_list = list(df["positives"])
    chart5_info = {}
    chart5_info['x_name'] = chart5_data_list[:5]
    chart5_info['data'] = chart5_city_list[:5]
    return chart5_info

def get_chart5_1_data():
    chart5_dict = {}
    df = get_malware_json_report()
    l1 = list(df["company"])
    l2 = list(df["count"])
    chart5_dict = dict(zip(l1,l2))
    chart5_data_list = sorted(chart5_dict.items(), key=lambda x: x[1], reverse=True)
    chart5_city_list = [x[0] for x in chart5_data_list[:5]]
    chart5_1_info = {}
    chart5_1_info['x_name'] = chart5_city_list
    chart5_1_info['data'] = chart5_data_list[:5]
    return chart5_1_info


def get_chart_map_data():
    map_chart_list = []
    map_data = json.loads(rd.get('ncovcity_data'))
    for data in map_data['newslist']:
        map_chart_dict = {}
        map_chart_dict['name'] = data['provinceShortName']
        map_chart_dict['value'] = data['confirmedCount']
        map_chart_list.append(map_chart_dict)
    print(222222)
    #print(map_chart_list)
    return map_chart_list

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
    print(33333)
    #print(chart_info)
    return jsonify(chart_info)


if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, debug=True)
