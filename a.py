# -*- coding: utf-8 -*
import requests
import json
import os


def send(sckey,msg):
    serverUrl = 'http://sc.ftqq.com/'+sckey+'.send'
    data={'text':'冰灵云签到','desp':msg}
    r=requests.post(url=serverUrl,data=data)
    print(r.text)
def login():
    message = ''
    loginResult = requests.post(url=loginUrl, data=loginData)
    if loginResult.text=='{"ret":1,"msg":"\\u767b\\u5f55\\u6210\\u529f"}':#登录成功
        message+='登录成功！\n'

        cookieDic = loginResult.cookies.get_dict()
        email = cookieDic['email']
        expire_in = cookieDic['expire_in']
        key = cookieDic['key']
        uid = cookieDic['uid']

        cookie='uid='+uid+';email='+email+';expire_in='+expire_in+';key='+key
        header={'cookie':cookie}

        checkinResult = requests.post(url=checkinUrl, headers=header).text
        checkinResultDic = json.loads(checkinResult)

        if checkinResultDic['ret'] == 1:#今日首次签到
            message += checkinResultDic['msg'] + '\n' + '剩余流量：' + checkinResultDic['unUsedTraffic']
            print(message)
            send(sckey, message)
        if checkinResultDic['ret'] == 0:#今日非首次签到
            message += '今天已经签到过了！\n'
            userInfo = requests.get(url=userUrl, headers=header).text
            if userInfo.find('id="remain">') != -1:  # 获取剩余流量成功
                remain = userInfo.split('id="remain">')[1].split('</code>')[0]
                message+='剩余流量：' + remain
                print(message)
                send(sckey, message)
            else:
                message+='未获取到剩余流量！'
                print(message)
                send(sckey,message)

if __name__=='__main__':
    username = os.environ['email']
    passwd = os.environ['passwd']
    sckey = os.environ['sckey']

    loginData = {'email': username, 'passwd': passwd, 'code': ''}

    loginUrl = 'https://www.cssr.vip/auth/login'
    userUrl = 'https://www.cssr.vip/user'
    checkinUrl = 'https://www.cssr.vip/user/checkin'

    login()

