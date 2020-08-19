#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import argparse
import os
import time, datetime
import hashlib



def file(path, algorithm):
    global start, end  # 声明全局变量
    start = time.time()  # 获取当前时间，用于记录计算过程的耗时
    size = os.path.getsize(path)  # 获取文件大小，单位是字节（byte）
    with open(path, 'rb') as f:  # 以二进制模式读取文件
        while size >= 1024 * 1024:  # 当文件大于1MB时将文件分块读取
            algorithm.update(f.read(1024 * 1024))
            size -= 1024 * 1024
        algorithm.update(f.read())
    end = time.time()  # 获取计算结束后的时间
    return algorithm.hexdigest()  # 输出计算结果

def get_sha256_info(s):
    folder = "../DATA/" + s[0] + "/"+ s[1] + "/"+ s[2]+ "/" + s[3] + "/"
    f_path = folder + s
    if not os.path.exists(os.path.abspath(f_path)):
        fileinfo = s+"?"+"Cyber攻击代码库没有此文件"
        print(fileinfo)
        return 

    str_cmd = "file {}".format(f_path)
    filetype =  os.popen(str_cmd).read().strip().split("/")[-1]
    filetype = filetype.split(":")[-1]
		
    md5 = file(f_path, hashlib.md5())
    sha1 = file(f_path, hashlib.sha1())
    filesize = os.stat(f_path).st_size
    filesize = filesize/1024
    filesize = str(filesize)+"KB"
    accesstime = os.stat(f_path).st_atime
    modifytime = os.stat(f_path).st_mtime
    changetime = os.stat(f_path).st_ctime
    dateArray = datetime.datetime.fromtimestamp(accesstime)
    accesstime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    dateArray = datetime.datetime.fromtimestamp(modifytime)
    modifytime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    dateArray = datetime.datetime.fromtimestamp(changetime)
    changetime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    filelocation = os.path.abspath(folder)
    fileinfo = "SHA256?"+s+"?"+"MD5?"+md5+"?"+"SHA1?"+sha1+"?"+"filelocation?"+filelocation+"?"+"filetype?"+filetype+"?"+"filesize?"+str(filesize)+"?"+"accesstime?"+str(accesstime)+"?"\
    +"modifytime?"+str(modifytime)
    print(fileinfo)

def parseargs():
    parser = argparse.ArgumentParser(description = "to get samples info from sha256")
    parser.add_argument("-s", "--sha256", help="input sha256", type=str, required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    Args = parseargs()
    get_sha256_info(Args.sha256)

