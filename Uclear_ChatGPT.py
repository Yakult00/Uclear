import time
import requests
import json
from contextlib import suppress

BASE_URL = "https://phoenix.ujing.online:443/api/v1"
HEADERS = {'Content-Type': 'application/json'}


def login():
    """登录并获取 token"""
    phone_number = input("手机号：")
    url = f"{BASE_URL}/captcha?mobile={phone_number}&sessionId=AFS_SWITCH_OFF&sig=AFS_SWITCH_OFF&token=AFS_SWITCH_OFF&type=1"

    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if data.get('code') != 0:
        raise ValueError("验证码发送失败!", data)

    captcha = input("验证码发送成功！\n 请输入验证码：")
    for attempt in range(3):
        response = requests.post(f"{BASE_URL}/login", headers=HEADERS,
                                 json={"captcha": captcha, "mobile": phone_number})
        data = response.json()

        if data.get('code') == 0:
            print("登录成功!")
            return data['data']['token']

        if attempt < 2:
            captcha = input("验证码有误！\n 请重新输入验证码：")

    raise ValueError("登录失败!", data)


def get_device_info(floor):
    """根据楼层获取设备信息"""
    devices = {
        '8': ('66ff5699d0b9c978ee5536439ad62a10', '62bbef1708d9121394844121'),
        '9': ('4733641ad73d494c66cf5cf612f5102c', '62bbef1708d9121394844122'),
        '10': ('e9d6083f5b1ca04b67090feda4e94771', '62bbef1708d9121394844121')
    }
    return devices.get(floor, ('', ''))


def place_order():
    """生成订单 payload"""
    floor = input('输入楼层（例：8）：') or '10'
    while floor not in {'8', '9', '10'}:
        floor = input('输入有误，请重新输入楼层（例：8）：') or '10'

    wash_mode = input('洗衣模式 5-普通洗 6-小件洗 7-超强洗 8-单脱水：') or '5'
    while wash_mode not in {'5', '6', '7', '8'}:
        wash_mode = input('输入有误，请重新输入洗衣模式：') or '5'

    detergent = input('洗衣液规格 1-标准 3-大量 0-不加：') or '0'
    while detergent not in {'1', '3', '0'}:
        detergent = input('输入有误，请重新输入洗衣液规格：') or '0'

    disinfectant = input('除菌液规格 4-标准 6-大量 0-不加：') or '0'
    while disinfectant not in {'4', '6', '0'}:
        disinfectant = input('输入有误，请重新输入除菌液规格：') or '0'

    device_id, store_id = get_device_info(floor)

    if wash_mode == '8':
        detergent, disinfectant = '0', '0'

    payload = json.dumps({
        "deviceId": device_id,
        "wp_detergentGearId": detergent,
        "deviceTypeId": 1,
        "deviceWashModelId": wash_mode,
        "storeId": store_id,
        "type": 1,
        "wp_disinfectantGearId": disinfectant
    })
    return payload


def create_order(token, payload):
    """发送下单请求，成功后切换请求频率"""
    headers = {**HEADERS, 'Authorization': f"Bearer {token}"}
    order_confirmed = False

    while True:
        response = requests.post(f"{BASE_URL}/orders/create", headers=headers, data=payload)
        data = response.json()

        if data.get('message') == '您有未支付订单，请先支付':
            print(data['message'])
            order_confirmed = True
        elif data.get('message') == '':
            print('下单成功 请在三分钟内支付')
            order_confirmed = True
        else:
            print("请求出错或订单状态异常:", data.get('message', '未知错误'))

        # 根据订单状态调整发送频率
        time.sleep(30 if order_confirmed else 5)


def load_token():
    """从文件加载 token"""
    with suppress(FileNotFoundError, json.JSONDecodeError):
        with open('token.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('token', '')


def save_token(token):
    """将 token 保存到文件"""
    with open('token.json', 'w', encoding='utf-8') as f:
        json.dump({'token': token}, f, ensure_ascii=False, indent=4)


def main():
    """主程序逻辑"""
    token = load_token() or login()
    save_token(token)

    payload = place_order()

    create_order(token, payload)  # 持续发送下单请求直到终止


if __name__ == "__main__":
    main()
