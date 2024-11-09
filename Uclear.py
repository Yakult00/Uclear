import time
import requests
import base64
import json
import urllib3

def login():
    headers = {
        'Content-Length': '132',
        'Content-Type': 'application/json'
    }
    phone_number = input("手机号：")
    url = f"https://phoenix.ujing.online:443/api/v1/captcha?mobile={phone_number}&sessionId=AFS_SWITCH_OFF&sig=AFS_SWITCH_OFF&token=AFS_SWITCH_OFF&type=1"
    payload = {
  "aud": "your_api",
  "iss": "https://your_issuer.com"
}

    response0 = requests.request("GET",
                                 url,headers=headers, data=payload)
    data = response0.json()
    if data['code'] != 0:
        raise ValueError("验证码发送失败!", data)
    captcha = input("验证码发送成功！\n 请输入验证码：")

    retry_num = 3
    while retry_num > 0:
        url = f"https://phoenix.ujing.online:443/api/v1/login"
        data1 = f'{{"captcha": "{captcha}", "mobile": "{phone_number}"}}'
        response0 = requests.request("POST", "https://phoenix.ujing.online:443/api/v1/login", headers=headers, data=data1)
        data=response0.json()
        if data['code'] == 0:
            break
        else:
            print("登录失败!", data)
            captcha = input("验证码有误！\n 请重新输入验证码：")
            retry_num -= 1
            if retry_num == 0:
                ValueError("登录失败!", data)

    print("登录成功!")
    token = data['data']['token']
    return token


'''
5-普通洗
6-小件洗
7-超强洗
8-单脱水
 洗衣液      "wp_detergentGearId": 1 - 标准量,  3 - 大量, 0 - 不加
 除菌液      "wp_disinfectantGearId":  4 - 标准量, 6 - 大量, 0 - 不加
'''
def 下单():
    while True:
        floor = input('输入楼层（例：8）：')
        if floor == '8' or floor == '9' or floor == '10':
            break
        elif floor == '':
            floor = '10'
            break
        else:
            print('输入有误，请重新输入')
    while True:
        deviceWashModelId=input('''洗衣模式 5-普通洗 6-小件洗 7-超强洗 8-单脱水
：''')
        if deviceWashModelId == '5' or deviceWashModelId == '6' or deviceWashModelId == '7' or deviceWashModelId == '8':
            break
        elif deviceWashModelId == '':
            deviceWashModelId = '5'
            break
        else:
            print('输入有误，请重新输入')
    while True:
        wp_detergentGearId=input('''洗衣液规格 1-标准 3-大量 0-不加
:''')
        if wp_detergentGearId == '1' or wp_detergentGearId == '3' or wp_detergentGearId == '0':
            break
        elif wp_detergentGearId == '':
            wp_detergentGearId = '0'
            break
        else:
            print('输入有误，请重新输入')
    while True:
        wp_disinfectantGearId=input('''除菌液规格 4-标准 6-大量 0-不加
；''')
        if wp_disinfectantGearId == '4' or floor == '6' or floor == '0':
            break
        elif wp_disinfectantGearId == '':
            wp_disinfectantGearId = '0'
            break
        else:
            print('输入有误，请重新输入')


    match  floor:
        case '8':
            deviceId = '66ff5699d0b9c978ee5536439ad62a10'
            storeId = '62bbef1708d9121394844121'
            pass
        case '9':
            deviceId = '4733641ad73d494c66cf5cf612f5102c'
            storeId = '62bbef1708d9121394844122'
            pass
        case '10':
            deviceId = 'e9d6083f5b1ca04b67090feda4e94771'
            storeId = '62bbef1708d9121394844121'

    if deviceWashModelId == '8':
        wp_detergentGearId='0'
        wp_disinfectantGearId='0'

    payload = (f'{{"deviceId":"{deviceId}",'
               f'"wp_detergentGearId":{wp_detergentGearId},'
               f'"deviceTypeId":1,"deviceWashModelId":{deviceWashModelId},'
               f'"storeId":"{storeId}",'
               f'"type":1,'
               f'"wp_disinfectantGearId":{wp_disinfectantGearId}}}')
    return payload

def run(token):
    while True:
        response0 = requests.request("POST", "https://phoenix.ujing.online:443/api/v1/orders/create", headers=headers, data=payload)
        data = response0.json()
        if data['message'] == '您有未支付订单，请先支付':
            print(data['message'])
            break
        elif data['message'] == '':
            print('下单成功 请在三分钟内支付')
            break
        time.sleep(5)

while True:
    with open('token.json', 'r', encoding='utf-8') as f:
    # 加载JSON数据到Python字典
    loaded_dict = json.load(f)

    # 从字典中获取token值
    token = loaded_dict['token']
    Authorization = 'Bearer ' + token
    headers = {
        'Content-Length': '132',
        'Content-Type': 'application/json',
        'Authorization': f"{Authorization}"
    }
    if token != '':
        payload = 下单()
        if token != '':
            while True:
                run(token)
                time.sleep(30)
    else:
        token = login()
        data_dict = {
            'token': token
        }
        # 将字典保存到JSON文件
        with open('token.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

