# -*- coding: utf-8 -*-
import requests
import random
import json,os,time,sys
from hashlib import md5
import pandas as pd

#copyright:likai

# 中文：zh 英文：en 日语：jp  韩语：kor
def getBaiduTransResult(query,from_lang,to_lang):
    # Set your own appid/appkey.
    appid = '20210311000723302'
    appkey = 'OxA_shUkpA6mAvYdjKlH'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    result_dst = ''
    try:
        result_dst = result['trans_result'][0]['dst']
    except:
        result_dst = 'ERROR'
    # Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    print(result_dst)

    return result_dst

path = sys.argv[1]
from_lang = sys.argv[2]
to_lang = sys.argv[3]

if __name__=='__main__':
    # from_lang = 'zh'
    # to_lang = 'en'
    IN = os.path.join(path,'IN')
    OUT = os.path.join(path,'OUT')
    time_now = time.strftime("%m%d%H%M%S")
    print(time_now)
    folderlist = os.listdir(IN)
    for f in folderlist:
        ori_file = os.path.join(os.path.abspath(IN),f)
        savepath = os.path.join(OUT,f[:f.rfind('.')]+'_out_'+to_lang+time_now+'.xlsx')
        writer = pd.ExcelWriter(savepath)# pylint: disable=abstract-class-instantiated
        dataFrame = pd.read_excel(ori_file, 'TestCase')
        nrows = dataFrame.index
        print(len(nrows))
        
        for i in range(len(nrows)):#填写开始行数
            print(i)
            case = dataFrame.loc[i,'CASE']#case获取
            print(case)
            baiduResult = getBaiduTransResult(case, from_lang, to_lang)
            dataFrame.loc[i,'baidu_'+str(to_lang)] = baiduResult
            recase = getBaiduTransResult(baiduResult, to_lang, from_lang)
            dataFrame.loc[i,'recase'] = recase

        dataFrame.to_excel(writer,"TestCase",index = None)
        writer.save()