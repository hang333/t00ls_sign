#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 2020年3月17日
'''
import requests
import re #正则模块
import time
import hashlib
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

url_login = 'https://www.t00ls.net/login.html'
url_checklogin = 'https://www.t00ls.net/checklogin.html'
url_signin = 'https://www.t00ls.net/ajax-sign.json'

# questionid
# 1 母亲的名字
# 2 爷爷的名字
# 3 父亲出生的城市
# 4 您其中一位老师的名字
# 5 您个人计算机的型号
# 6 您最喜欢的餐馆名称
# 7 驾驶执照的最后四位数字

username = os.environ['T00LS_USERNAME'] # 用户名
password = os.environ['T00LS_PASSWORD']  # 明文密码或密码MD5
password_hash = ("T00LS_MD5" in os.environ) and os.environ['T00LS_MD5']=='True' or False  # 密码为md5时设置为True
questionid = ("T00LS_QID" in os.environ) and os.environ['T00LS_QID'] or ''  # 问题ID，参考上面注释，没有可不填
answer = ("T00LS_QANS" in os.environ) and os.environ['T00LS_QANS'] or ''   # 问题答案，没有可不填
SCKEY = ("T00LS_SCKEY" in os.environ) and os.environ['T00LS_SCKEY'] or '' #Server酱申请的skey

def get_formhash(session):
    res = session.get(url=url_login, headers=headers)
    formhash_1 = re.findall('value=\"[0-9a-f]{8}\"', res.text)
    formhash = re.findall('[0-9a-f]{8}', formhash_1[0])[0]
#    print(formhash)
    time.sleep(1)
    return formhash
def get_current_user(session):
    current_user = re.findall('<a href="members-profile-[\d+].*\.html" target="_blank">{username}</a>'.format(username=username), session)
    print(''.join(current_user))
    cuser = re.findall('[\d+]{4,5}', ''.join(current_user))[0]
    print("用户ID:"+cuser)
    return cuser
def login_t00ls(session):
    formhash=get_formhash(session)
    if password_hash:
        passwords = password
    else:
        passwords = hashlib.md5(password.encode('utf-8')).hexdigest()
    data = {
        'username': username,
        'password': passwords,                                 
        'questionid': questionid,                                    
        'answer': answer,                                         
        'formhash': formhash,
        'loginsubmit': '登录',
        'redirect': 'https://www.t00ls.net',
        'cookietime': '2592000'
    }

    censored_data = data.copy()
    censored_data['password'] = '***'
    print(censored_data)

    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    headers['Referer'] = 'https://www.t00ls.net/login.html'
    res = session.post(url=url_login, headers=headers, data=data)
    #print(res.headers)
    time.sleep(1)
    #res2=session.get("https://www.t00ls.net/checklogin.html");
    #print(res2.text)
    return res, formhash
def get_formhash_1(session):
    res = session.get(url=url_checklogin, headers=headers)
    #print("检查登录："+res.text)
    uid = get_current_user(res.text)
    #formhash = re.findall('[0-9a-f]{8}', res.text)[0]
    formhash=re.findall(re.compile('formhash=(.*?)">'), res.text)[0]#20200318修复来源不正确问题
    return formhash, uid
def signin_t00ls(session):
    formhash, uid = get_formhash_1(session)
    print("formhash:"+formhash+"----", "用户ID:"+uid )
    data = {
        'formhash': formhash,
        'signsubmit': 'apply'
    }
    headers['Referer'] = 'https://www.t00ls.net/members-profile-{uid}.html'.format(uid=uid)
    res = session.post(url=url_signin, data=data, headers=headers)
    return res
def main():
    session = requests.session()# 定义全局session
    get_formhash(session)#第一步----获取formhash
    login_t00ls(session)#登录T00ls
    res_signin = signin_t00ls(session)#签到
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), res_signin.text)
    datamsg={"text":"T00ls签到成功！","desp":res_signin.text}
    if "success" in res_signin.text:
      if(SCKEY != ''):
        requests.post("https://sc.ftqq.com/"+SCKEY+".send",data=datamsg)
        
def main_handler(event, context):
  return main()
if __name__ == '__main__':
  main()