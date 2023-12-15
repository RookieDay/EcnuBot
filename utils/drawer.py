# 以下部分代码摘录自：https://github.com/CrazyBoyM/nonebot-plugin-drawer/blob/main/nonebot_plugin_drawer/drawer.py
import os
import json
from pydantic.v1 import BaseSettings
import base64
import string
import random
import requests
from utils import config


qianfan_url = config.config["qianfan_url"]
qianfan_img = config.config["qianfan_img"]
qianfan_ak = config.config["qianfan_ak"]
qianfan_sk = config.config["qianfan_sk"]


class Config(BaseSettings):
    # 千帆 stable Stable-Diffusion-XL
    qianfan_url: str = qianfan_url  # token url
    qianfan_img: str = qianfan_img  # img url
    qianfan_ak: str = qianfan_ak  # ak
    qianfan_sk: str = qianfan_sk  # sk
    qianfan_cd_time: int = 60  # cd时间，单位秒
    qianfan_image_count: int = 1  # 图片数量

    class Config:
        extra = "ignore"


qianfan_config = Config()


# 获取access_token
async def get_token():
    url = qianfan_url
    params = {
        "grant_type": "client_credentials",
        "client_id": qianfan_config.qianfan_ak,
        "client_secret": qianfan_config.qianfan_sk,
    }
    try:
        resp = requests.post(url, params=params)
        access_token = resp.json()["access_token"]
    except:
        access_token = f"access_token failed"
    return access_token


# 获取绘画的结果
async def get_img(access_token, text_prompt):
    url = qianfan_img + access_token
    base_prompt = "masterpiece, best quality,"
    neg_prompt = "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation. tattoo, watermark,"
    # size：生成图片长宽，默认值 1024x1024，取值范围如下：["768x768", "768x1024", "1024x768", "576x1024", "1024x576", "1024x1024"]
    # n：生成图片数量，说明：默认值为1，取值范围为1-4，单次生成的图片较多及请求较频繁可能导致请求超时
    payload = json.dumps(
        {
            "prompt": base_prompt + text_prompt,
            "negative_prompt": neg_prompt,
            "size": "1024x1024",
            "n": 1,
            "steps": 30,
            "sampler_index": "DPM++ 2M Karras",
        }
    )
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        resp = requests.request("POST", url, headers=headers, data=payload).json()
        if "data" in resp and len(resp["data"]) > 0:
            resp_data = resp["data"]
    except:
        resp_data = f'绘画任务失败,返回msg: {resp["error_msg"]}'
    return resp_data


def download(image_name, img_b64, file_path):
    # 是否有这个路径
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    image_path = os.path.join(file_path, image_name)
    print('image_path')
    print(image_path)
    image_data = base64.b64decode(img_b64)
    with open(image_path, "wb") as f:
        f.write(image_data)
    return image_path


async def image_url(text_prompt, file_path):
    access_token = await get_token()
    img_data = await get_img(access_token, text_prompt)
    number = 0
    image_path_list = []
    for img in img_data:
        number += 1
        image_name = (
            "".join(random.sample(string.ascii_letters + string.digits, 12))
            + str(number)
            + ".png"
        )
        image_path = download(image_name, img["b64_image"], file_path)
        image_path_list.append(image_path)
    return image_path_list
