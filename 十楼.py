import time
import requests
import base64
import json
import time
import urllib3

headers = {
 'Content-Length':'132',
 'Content-Type':'application/json',
 'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBVc2VySWQiOjIyMjE3MzE4LCJleHAiOjE3MzgxNTMxNDksImlhdCI6MTczMDExNzk0OSwiaWQiOjMwMTU2NTY3LCJuYW1lIjoiMTU5Nzk4MTc1MzEifQ.EoS4LWoBuWJGVMNidWpHR989Zd3b9SvtgTICHW9oS-Q',
 'x-user-geo':'113.462046,22.553483',
 'Accept':'*/*',
 'weex-version':'1.1.48',
 'x-mobile-brand':'apple',
 'Accept-Language':'zh-Hans-CN;q=1, en-CN;q=0.9',
 'Accept-Encoding':'gzip, deflate, br',
 'x-app-code':'BI',
 'x-mobile-id':'F5DCA7FD-00ED-4B9F-82AA-48D83750593E',
 'User-Agent':'U jing/2.4.3 (iPhone; iOS 16.7.2; Scale/3.00)',
 'x-app-version':'2.4.3',
 'Connection':'keep-alive',
 'Cookie':'acw_tc=976d5f46552a8fa2f9948cfb20abc31897efd7adf18e0fce60edff8092c9a634',
 'x-mobile-model':'iPhone 11 Pro Max'}

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
    # wp_detergentGearId='0'
    # wp_disinfectantGearId='0'
    # deviceWashModelId='6'


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
payload=下单()
def run():
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
    run()
    time.sleep(30)
# u.get_headers()
# u.login()