import re
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from login.Utils import Utils
from login.Rsa import Rsa
from actions.rlMessage import RlMessage
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class kmuLogin:
    # 初始化昆明学院的登陆类
    def __init__(self, username, password, login_url, host, session,sendkey):
        self.username = username
        self.password = password
        self.login_url = login_url
        self.host = host
        self.session = session
        self.rl = RlMessage(sendkey)

    # 登陆方法
    def login(self):

        html = self.session.get(self.login_url, verify=False).text
        soup = BeautifulSoup(html, 'lxml')
        form = soup.select('#fm1')
        if len(form) == 0:
            self.rl.send("失败","出错啦！网页中没有找到LoginForm")
            raise Exception('出错啦！网页中没有找到LoginForm')
        soup = BeautifulSoup(str(form[0]), 'lxml')
        # 填充数据
        params = {}
        form = soup.select('input')
        for item in form:
            if None != item.get('name') and len(item.get('name')) > 0:
                if item.get('name') != 'rememberMe':
                    if None == item.get('value'):
                        params[item.get('name')] = ''
                    else:
                        params[item.get('name')] = item.get('value')
        params['username'] = self.username

        pattern = 'RSAKeyPair\((.*?)\);'
        publicKey = re.findall(pattern, html)

        publicKey = publicKey[0].replace('"', "").split(',')
        en = Rsa(publicKey[0],publicKey[2]);
        params['password'] = en.encrypt(self.password)

        #验证码
        imgUrl = self.host + 'lyuapServer/captcha.jsp'
        params['captcha'] = Utils.getCodeFromImg(self.session, imgUrl)


        #发送请求
        data = self.session.post(self.login_url, params=params, allow_redirects=False)
        # 如果等于302强制跳转，代表登陆成功

        if data.status_code == 302:
            jump_url = data.headers['Location']
            res = self.session.post(jump_url, verify=False)

            if res.url.find('campusphere.net/') == -1:
                self.rl.send("失败", "昆明学院登陆失败,未能成功跳转今日校园!")
                raise Exception('昆明学院登陆失败,未能成功跳转今日校园!')
            return self.session.cookies
        elif data.status_code == 200:
            data = data.text
            soup = BeautifulSoup(data, 'lxml')
            msg = soup.select('#msg')[0].get_text()
            raise Exception(msg)
        else:
            self.rl.send("失败", "昆明学院登陆失败！返回状态码：" + str(data.status_code))
            raise Exception('昆明学院登陆失败！返回状态码：' + str(data.status_code))
