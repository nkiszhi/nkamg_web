# encoding: utf-8

"""
@version: ??
@author: Andy
@file: GetData.py
@time: 20/2/4 20:57
"""


import requests
import json
import pandas as pd



def get_latest_data():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/0000_latest.csv")
    listBins = [0, 5, 10, 15, 20, 25, 30, 35, 10000]
    listLabels = ['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35以上']
    df["apk_size"]=df["apk_size"].apply(lambda x: x/1024/1024)
    df['apk_size'] = pd.cut(df['apk_size'], bins=listBins, labels=listLabels, include_lowest=True)
    apk_size = df['dex_size'].groupby(df['apk_size']).count()
    print(11111)
    print(22222)
    apk_size = pd.DataFrame({'count':apk_size})
    apk_size.reset_index(inplace=True)
   # print(apk_size)
    return apk_size

def get_latest_malware_data():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/malware_latest.csv")
    listBins = [0, 5, 10, 15, 20, 25, 30, 35, 10000]
    listLabels = ['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35以上']
    df["apk_size"]=df["apk_size"].apply(lambda x: x/1024/1024)
    df['apk_size'] = pd.cut(df['apk_size'], bins=listBins, labels=listLabels, include_lowest=True)
    apk_size = df['dex_size'].groupby(df['apk_size']).count()
    print(11111)
    print(22222)
    apk_size = pd.DataFrame({'m_count':apk_size})
    apk_size.reset_index(inplace=True)

   # print(apk_size)
    return apk_size

def get_latest_benign_data():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/benign_latest.csv")
    listBins = [0, 5, 10, 15, 20, 25, 30, 35, 10000]
    listLabels = ['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35以上']
    df["apk_size"]=df["apk_size"].apply(lambda x: x/1024/1024)
    df['apk_size'] = pd.cut(df['apk_size'], bins=listBins, labels=listLabels, include_lowest=True)
    apk_size = df['dex_size'].groupby(df['apk_size']).count()
    print(11111)
    print(22222)
    apk_size = pd.DataFrame({'b_count':apk_size})
    apk_size.reset_index(inplace=True)

   # print(apk_size)
    return apk_size

def get_latest_date():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/0000_latest.csv")
    df['dex_date'] = pd.to_datetime(df['dex_date'])
    df = df.set_index('dex_date')
    s = pd.Series(df['sha256'], index=df.index)
    pd.set_option('display.max_rows',None)
    count = s.resample('AS').count().to_period('A')# 按年统计并显示 
    date_size = pd.DataFrame({'count':count})
    date_size.reset_index(inplace=True)
    date_size["dex_date"] = date_size["dex_date"].astype("str")
    return date_size

def get_latest_market():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/0000_latest.csv")
    market = df['dex_size'].groupby(df['markets']).count()
    market = pd.DataFrame({'count':market})
    market.reset_index(inplace=True)
    market['markets']=market['markets'].str.replace("play.google.com","google")
    return market

def get_latest_malware_date():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/malware_latest.csv")
    df['dex_date'] = pd.to_datetime(df['dex_date'])
    df = df.set_index('dex_date')
    s = pd.Series(df['sha256'], index=df.index)
    pd.set_option('display.max_rows',None)
    count = s.resample('AS').count().to_period('A')# 按年统计并显示 
    date_size = pd.DataFrame({'m_count':count})
    date_size.reset_index(inplace=True)
    date_size["dex_date"] = date_size["dex_date"].astype("str")
    return date_size

def get_latest_benign_date():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/benign_latest.csv")
    df['dex_date'] = pd.to_datetime(df['dex_date'])
    df = df.set_index('dex_date')
    s = pd.Series(df['sha256'], index=df.index)
    pd.set_option('display.max_rows',None)
    count = s.resample('AS').count().to_period('A')# 按年统计并显示 
    date_size = pd.DataFrame({'b_count':count})
    date_size.reset_index(inplace=True)
    date_size["dex_date"] = date_size["dex_date"].astype("str")
    return date_size

def get_samples_class():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/myfiletype.csv")
    fileclass = df['sha256'].groupby(df['fileclass']).count()
    fileclass = pd.DataFrame({'count':fileclass})
    fileclass.reset_index(inplace=True)
    return fileclass

def get_samples_filetype():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/myfiletype.csv")
    filetype = df['sha256'].groupby(df['filetype']).count()
    filetype = pd.DataFrame({'count':filetype})
    filetype.reset_index(inplace=True)
    filetype['filetype']=filetype['filetype'].str.replace("Zip archive data  at least v2.0 to extract","Zip v2.0").str.replace(" Java archive data","")
    return filetype

def get_json_positives_report():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/jsoninfo.csv")
    positives = pd.DataFrame(df, columns=["sha256","positives"])
    b=positives.sort_values(by="positives" , ascending=False)
    return b


def get_malware_json_report():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv("./data/json.csv")
    df["detected"]=df["detected"].astype("str")
    df1 = df[df.detected == "True"]
    company = df1['sha256'].groupby(df['company']).count()
    company = pd.DataFrame({'count':company})
    company.reset_index(inplace=True)
    return company

def get_samples_count():
    df = pd.read_csv("./data/myfiletype.csv")
    #print(df.shape[0])
    df1 = pd.read_csv("./data/jsoninfo.csv")
    #print(df1.shape[0])
    return df.shape[0],df1.shape[0]


if __name__ == '__main__':
    #trend = get_trend_data()
    # print(trend['data']['areaTree'])
    #res = get_ncov_data()
    res2 = get_json_positives_report()
    #print(res2)
    # # print(res['newslist'][0]['provinceName'])










