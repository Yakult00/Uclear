import os
import requests
from pyzbar.pyzbar import decode
from PIL import Image
import json

BASE_URL = "https://phoenix.ujing.online:443/api/v1/devices/scanWasherCode"
HEADERS = {'Content-Type': 'application/json'}


def load_token():
    """从文件加载 JWT token"""
    try:
        with open('token.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('token', '')  # 获取 token
    except (FileNotFoundError, json.JSONDecodeError):
        print("无法加载 token，请确保 token.json 文件存在且格式正确。")
        return ''


def save_device_ids(device_data):
    """保存设备ID到 data.json 文件"""
    try:
        # 尝试加载现有的 data.json 文件
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}

        # 更新数据，将文件名和对应的 deviceId 存入
        data['deviceIds'] = device_data

        # 将更新后的数据保存回 data.json 文件
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("洗衣机ID保存成功")
    except Exception as e:
        print(f"保存设备ID时出错: {e}")


def scan_and_request_qr_codes(directory="Photo"):
    """扫描指定目录中的所有二维码图片并发送请求"""
    if not os.path.isdir(directory):
        print(f"目录 '{directory}' 不存在。")
        return

    # 加载 JWT token
    token = load_token()
    if not token:
        print("没有有效的 token，无法继续请求。")
        return

    # 更新头部信息，加入 Authorization 头部
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'  # 加入 JWT token
    }

    device_data = {}  # 用于存储文件名与对应的 deviceId

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # 只处理图片文件
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # 确保只处理图片文件
            try:
                image = Image.open(file_path)
                decoded_data = decode(image)

                if decoded_data:
                    for qr_code in decoded_data:
                        qr_content = qr_code.data.decode("utf-8")

                        # 构造请求数据并发送 POST 请求
                        payload = {"qrCode": qr_content}
                        response = requests.post(BASE_URL, headers=headers, json=payload)
                        response_data = response.json()

                        # 获取设备ID并存储文件名与 deviceId 的对应关系
                        if response_data.get('code') == 0:
                            device_id = response_data['data']['result']['deviceId']
                            device_data[file_name] = device_id
                else:
                    continue  # 没有二维码跳过

            except Exception as e:
                continue  # 处理异常时跳过当前文件

    # 保存文件名与 deviceId 的对应关系
    save_device_ids(device_data)


# 调用函数扫描二维码并发送请求
scan_and_request_qr_codes()
