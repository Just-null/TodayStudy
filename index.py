import yaml
from todayLoginService import TodayLoginService
from actions.collection import Collection
from actions.rlMessage import RlMessage
from login.Utils import Utils



def getYmlConfig(yaml_file='config.yml'):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)

# 全局配置
config = getYmlConfig(yaml_file='config.yml')


def main():
    for index, user in enumerate(config['users']):
        sendkey = user['user']['sendKey']
        rl = RlMessage(sendkey)
        if config['debug']:
            msg = working(user,sendkey)
        else:
            try:
                msg = working(user,sendkey)
            except Exception as e:
                msg = str(e)
                print(Utils.getAsiaTime() + ' ' + msg)
                msg = rl.send('自动提交失败', msg)
                print(Utils.getAsiaTime() + ' ' + msg)
                continue
        rl.send('自动提交成功', msg)


def working(user,sendkey):
    print(f'{Utils.getAsiaTime()} 正在获取登录地址')
    today = TodayLoginService(user['user'],sendkey)

    print(f'{Utils.getAsiaTime()} 正在登录ing')
    today.login()
    # 登陆成功，通过type判断当前属于 信息收集、签到、查寝
    # 信息收集
    if user['user']['type'] == 0:
        # 以下代码是信息收集的代码
        print(f'{Utils.getAsiaTime()} 正在进行“信息收集”...')
        collection = Collection(today, user['user'],sendkey)
        collection.queryForm()
        collection.fillForm()
        msg = collection.submitForm()
        return msg


# 阿里云的入口函数
def handler(event, context):
    main()


if __name__ == '__main__':
    main()
