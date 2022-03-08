#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
''' 修改自 https://www.t00ls.net/viewthread.php?tid=55689 '''
import requests
import json
import hashlib
import os

uname = os.environ['T00LS_USERNAME'] # 用户名
pswd = os.environ['T00LS_PASSWORD']  # 明文密码或密码MD5
password_hash = ("T00LS_MD5" in os.environ) and os.environ['T00LS_MD5']=='True' or False  # 密码为md5时设置为True
qesnum = ("T00LS_QID" in os.environ) and os.environ['T00LS_QID'] or '' # 安全提问 参考下面
qan = ("T00LS_QANS" in os.environ) and os.environ['T00LS_QANS'] or '' #安全提问答案
SCKEY = ("T00LS_SCKEY" in os.environ) and os.environ['T00LS_SCKEY'] or '' #Server酱申请的skey

if not password_hash:
    pswd = hashlib.md5(pswd.encode('utf-8')).hexdigest()

# 0 = 没有安全提问
# 1 = 母亲的名字
# 2 = 爷爷的名字
# 3 = 父亲出生的城市
# 4 = 您其中一位老师的名字
# 5 = 您个人计算机的型号
# 6 = 您最喜欢的餐馆名称
# 7 = 驾驶执照的最后四位数字

logindata = {
  'action': 'login',
  'username': uname,
  'password': pswd,
  'questionid': qesnum,
  'answer': qan
}

rlogin = requests.post('https://www.t00ls.com/login.json', data = logindata)
rlogj = json.loads(rlogin.text)
if (rlogj["status"] != "success"):
  print("登入失败，请检查输入资料是否正确！")
else :
  tscookie = requests.utils.dict_from_cookiejar(rlogin.cookies)
signdata = {
  'formhash': rlogj["formhash"],
  'signsubmit': "true"
}
rsign = requests.post('https://www.t00ls.com/ajax-sign.json', data = signdata, cookies = tscookie)
rsinj = json.loads(rsign.text)
datamsg={"text":"T00ls签到成功！","desp":rsign.text}
if (rsinj["status"] == "success"):
  print("签到成功！")
  if(SCKEY != ''):
    requests.post("https://sc.ftqq.com/"+SCKEY+".send",data=datamsg)
elif(rsinj["message"] == "alreadysign"):
  print("今天已经签到过了！")
else :
  raise Exception('签到失败', rsign.text)
