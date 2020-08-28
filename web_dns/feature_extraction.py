# -*- coding: utf-8 -*-
"""
Created on 2020/8/13 10:01

@author : dengcongyi0701@163.com

Description:

"""
import tld
import re
import math
import pandas as pd
import numpy as np
import pickle
import wordfreq
import string
from collections import defaultdict, Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

dgaTLD_list = ["cf", "recipes", "email", "ml", "gq", "fit", "cn", "ga", "rest", "tk"]
standard_scaler_add = r"./model/RF_standardscalar.pkl"

accepted_chars = 'abcdefghijklmnopqrstuvwxyz '
pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])


def get_name(url):
    """
    用python自带库进行域名提取
    :param url: url
    :return: 二级域名，顶级域名
    """
    url = url.strip(string.punctuation)
    try:
        TLD = tld.get_tld(url, as_object=True, fix_protocol=True)
        SLD = tld.get_tld(url, as_object=True, fix_protocol=True).domain

    except Exception as e:
        na_list = url.split(".")
        TLD = na_list[-1]
        SLD = na_list[-2]
    return str(TLD), str(SLD)


def cal_rep_cart(SLD):
    """
    计算字符串中重复出现的字符个数
    :param SLD: 字符串
    :return: 重复字符个数
    """
    dic = dict()
    for s in SLD:
        dic[s] = SLD.count(s)
    for d in list(dic.keys()):
        if dic[d] == 1:
            del dic[d]
    return len(dic)


def cal_ent_gni_cer(SLD):
    """
    计算香农熵, Gini值, 字符错误的分类
    :param url:
    :return:
    """
    f_len = float(len(SLD))
    count = Counter(i for i in SLD).most_common()  # unigram frequency
    ent = -sum(float(j / f_len) * (math.log(float(j / f_len), 2)) for i, j in count)  # shannon entropy
    gni = 1 - sum(float(j / f_len) * float(j / f_len) for i, j in count)
    cer = 1 - max(float(j/ f_len) for i, j in count)
    return ent, gni, cer


def cal_gram_med(SLD, n):
    """
    计算字符串n元频率中位数
    :param SLD: 字符串
    :param n: n
    :return:
    """
    grams = [SLD[i:i + n] for i in range(len(SLD) - n+1)]
    fre = list()
    for s in grams:
        fre.append(wordfreq.zipf_frequency(s, 'en'))
    return np.median(fre)


def get_feature(url):
    TLD, SLD = get_name(url)
    url = SLD+"."+TLD
    url_rm = re.sub(r"\.|_|-", "", url)
    TLD_rm = re.sub(r"\.|_|-", "", TLD)
    SLD_rm = re.sub(r"\.|_|-", "", SLD)

    # 1. 域名总长度
    domain_len = len(url)

    # 2. SLD长度
    sld_len = len(SLD)

    # 3. TLD长度
    tld_len = len(TLD)

    # 4. 域名不重复字符数
    uni_domain = len(set(url_rm))

    # 5. SLD不重复字符数
    uni_sld = len(set(SLD_rm))

    # 6. TLD不重复字符数
    uni_tld = len(set(TLD_rm))

    # 7. 是否包含某些恶意顶级域名 https://www.spamhaus.org/statistics/tlds/
    flag_dga = 0
    for t in dgaTLD_list:
        if t in url:
            flag_dga = 1

    # 8. 是否以数字开头
    flag_dig = 0
    if re.match("[0-9]", url) != None:
        flag_dig = 1

    # 9. 特殊符号在SLD中占比
    sym = len(re.findall(r"\.|_|-", SLD))/sld_len

    # 10. 十六进制字符在SLD中占比
    hex = len(re.findall(r"[0-9]|[a-f]", SLD))/sld_len

    # 11. 数字在SLD中占比
    dig = len(re.findall(r"[0-9]", SLD))//sld_len

    # 12. 元音字母在SLD中占比
    vow = len(re.findall(r"a|e|i|o|u", SLD))/sld_len

    # 13. 辅音字母在SLD中占比
    con = len(re.findall(r"b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z", SLD))/sld_len

    # 14. 重复字符在SLD不重复字符中占比
    rep_char_ratio = cal_rep_cart(SLD_rm)/uni_sld

    # 15. 域名中连续辅音占比
    con_list = re.findall(r"[b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z]{2,}", url)
    con_len = [len(con) for con in con_list]
    cons_con_ratio = sum(con_len)/domain_len

    # 16. 域名中连续数字占比
    dig_list = re.findall(r"[0-9]{2,}", url)
    dig_len = [len(dig) for dig in dig_list]
    cons_dig_ratio = sum(dig_len)/domain_len

    # 17. SLD中由'-'分割的令牌数
    tokens_sld = len(SLD.split('-'))

    # 18. SLD中数字总数
    digits_sld = len(re.findall(r"[0-9]", SLD))

    # 19. SLD中字符的归一化熵值
    # 20. SLD的Gini值
    # 21. SLD中字符分类的错误
    ent, gni, cer = cal_ent_gni_cer(SLD)

    # 22. SLD中2元频次的中位数
    gram2_med = cal_gram_med(SLD, 2)

    # 23. SLD中3元频次的中位数
    gram3_med = cal_gram_med(SLD, 3)

    # 24. 重复SLD中2元频次中位数
    gram2_cmed = cal_gram_med(SLD+SLD, 2)

    # 25. 重复SLD中3元频次中位数
    gram3_cmed = cal_gram_med(SLD+SLD, 3)

    # # 26. 域名的hmm成文概率
    # hmm_prob = cal_hmm_prob(url)
    #
    # # 27. gib判断SLD是否成文
    # sld_gib = cal_gib(SLD)

    feature = [domain_len, sld_len, tld_len, uni_domain, uni_sld, uni_tld, flag_dga, flag_dig, sym, hex, dig, vow,
               con, rep_char_ratio, cons_con_ratio, cons_dig_ratio, tokens_sld, digits_sld, ent, gni, cer, gram2_med,
               gram3_med, gram2_cmed, gram3_cmed]
    return feature


def normalize(df):
    """
    按列归一化
    :param df:
    :return:
    """
    col = ["domain_len", "sld_len", "tld_len", "uni_domain", "uni_sld", "uni_tld", "flag_dga",
           "flag_dig", "sym", "hex", "dig", "vow","con", "rep_char_ratio", "cons_con_ratio", "cons_dig_ratio",
           "tokens_sld", "digits_sld", "ent", "gni", "cer", "gram2_med","gram3_med", "gram2_cmed", "gram3_cmed"]
    for c in col:
        d = df[c]
        MAX = d.max()
        MIN = d.min()
        df.drop(c, axis=1)
        df[c] = ((d - MIN) / (MAX - MIN)).tolist()
    return df


def RF_feature_extraction(df):
    """
    特征提取, 归一化
    :param df:
    :return:
    """
    col = ["domain_name", "label", "domain_len", "sld_len", "tld_len", "uni_domain", "uni_sld", "uni_tld", "flag_dga",
           "flag_dig", "sym", "hex", "dig", "vow", "con", "rep_char_ratio", "cons_con_ratio", "cons_dig_ratio",
           "tokens_sld", "digits_sld", "ent", "gni", "cer", "gram2_med", "gram3_med", "gram2_cmed", "gram3_cmed"]
    fea_list = list()
    for ind in df.index:
        fea = df.loc[ind].tolist()
        if ind % 1000 == 0:
            print("{}...".format(ind))
        fea.extend(get_feature(df.at[ind, 0]))
        fea_list.append(fea)

    fea_df = pd.DataFrame(fea_list, columns=col)
    return fea_df


