import requests
from datetime import datetime, timezone, timedelta
from login.Utils import Utils

# 获取当前日期，格式为 2021-8-22
def getNowDate():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt.strftime("%Y-%m-%d %H:%M:%S")

# 消息通知类
class RlMessage:
    # 初始化类
    def __init__(self, sendKey):
        self.sendKey = sendKey

    # Server
    def sendServer(self, status, msg):
        title_text = '今日校园自动提交结果通知'
        print('正在发送Server酱。。。')
        res = requests.post(url='https://sc.ftqq.com/{0}.send'.format(self.sendKey),
                            data={'text': title_text, 'desp': Utils.getTimeStr() + "\n" + status+"  "+msg})
        code = res.json()['data']['error']
        if code == 'SUCCESS':
            print('发送Server酱通知成功。。。')
        else:
            print('发送Server酱通知失败。。。')
            print('Server酱返回结果' + code)

    # 其他通知方式待添加

    # 统一发送接口名
    def send(self, status, msg):
        self.sendServer(status, msg)
