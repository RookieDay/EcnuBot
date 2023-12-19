# -*- coding: utf-8 -*-
import json
import time
import openai
import requests
import asyncio                  
from utils import config, user_data

import dashscope

dashscope.api_key = config.config["dashscope_key"]

# ecnu chat
user_QA = [
    "ECNU 情感 搜索 inner",
    "ECNU 情感 搜索",
    "ECNU 问答 搜索",
    "ECNU 教学 搜索",
    "ECNU 情感 inner",
    "ECNU 搜索",
    "ECNU 情感",
    "ECNU 教学",
    "ECNU 问答",
    "ECNU",
]


class Model_list:
    def __init__(
        self,
        ecnu_data={},
        thudm_data={},
        qianfan_data={},
        tongyi_data={},
        tongyi_chatglm3_data={},
    ):
        self.ecnu_data = ecnu_data
        self.thudm_data = thudm_data
        self.qianfan_data = qianfan_data
        self.tongyi_data = tongyi_data
        self.tongyi_chatglm3_data = tongyi_chatglm3_data

    def qianwen(self, text_prompt, from_wxid):
        # 通义大模型qwen-max
        model_name = 'qwen-max'
        try:
            if from_wxid in self.tongyi_data:
                self.tongyi_data[from_wxid]["messages"].append(
                    {"role": "user", "content": text_prompt}
                )
            else:
                self.tongyi_data[from_wxid] = {
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": text_prompt},
                    ]
                }

            response = dashscope.Generation.call(
                model="qwen-max",
                messages=self.tongyi_data[from_wxid]["messages"],
                seed=1234,
                top_p=0.8,
                result_format="message",
                enable_search=False,
                max_tokens=1500,
                temperature=1.0,
                repetition_penalty=1.0,
            )
            print(response)
            response = response["output"]["choices"][0]["message"]["content"]
            self.tongyi_data[from_wxid]["messages"].append(
                {"role": "assistant", "content": response}
            )
            asyncio.run(user_data.storge_data(from_wxid, text_prompt, response, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), model_name))
            time.sleep(1)
        except:
            print(response)
            response = "任务存在问题"
        return response

    def qianwen_chatgml3(self, text_prompt, from_wxid):
        # 通义大模型服务 ChatGLM3
        # qq.com
        model_name = "chatglm3-6b"
        try:
            if from_wxid in self.tongyi_data:
                self.tongyi_chatglm3_data[from_wxid]["messages"].append(
                    {"role": "user", "content": text_prompt}
                )
            else:
                self.tongyi_chatglm3_data[from_wxid] = {
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": text_prompt},
                    ]
                }

            response = dashscope.Generation.call(
                model="chatglm3-6b",
                messages=self.tongyi_chatglm3_data[from_wxid]["messages"],
            )
            # chatglm3 返回的值 前面有空行，特此替换掉
            response = response["output"]["text"][2:]
            self.tongyi_chatglm3_data[from_wxid]["messages"].append(
                {"role": "assistant", "content": response}
            )
            asyncio.run(user_data.storge_data(from_wxid, text_prompt, response, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), model_name))
            time.sleep(1)
        except:
            response = "任务存在问题"
        return response

    def qianfan(self, text_prompt, from_wxid):
        # 百度千帆大模型
        model_name = "qianfan_chinese_llama_2_13b"
        try:
            token_url = config.config["qianfan_url"]
            API_KEY = config.config["qianfan_ak"]
            SECRET_KEY = config.config["qianfan_sk"]
            params = {
                "grant_type": "client_credentials",
                "client_id": API_KEY,
                "client_secret": SECRET_KEY,
            }
            access_token = str(
                requests.post(token_url, params=params).json().get("access_token")
            )
            url = config.config["qianfan_api"] + access_token
            print(url)
            if from_wxid in self.qianfan_data:
                self.qianfan_data[from_wxid]["messages"].append(
                    {"role": "user", "content": text_prompt}
                )
            else:
                self.qianfan_data[from_wxid] = {
                    "messages": [{"role": "user", "content": text_prompt}]
                }

            payload = json.dumps(self.qianfan_data[from_wxid])
            headers = {"Content-Type": "application/json"}
            response = requests.request("POST", url, headers=headers, data=payload)
            response = response.json()["result"]
            self.qianfan_data[from_wxid]["messages"].append(
                {"role": "assistant", "content": response}
            )
            asyncio.run(user_data.storge_data(from_wxid, text_prompt, response, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), model_name))
            time.sleep(1)
        except:
            response = "任务存在问题"
            print(response)
        return response

    def qianfan_image(self, text_prompt, from_wxid):
        # 百度千帆大模型
        model_name = "Stable-diffusion-XL"
        try:
            token_url = config.config["qianfan_url"]
            API_KEY = config.config["qianfan_ak"]
            SECRET_KEY = config.config["qianfan_sk"]
            params = {
                "grant_type": "client_credentials",
                "client_id": API_KEY,
                "client_secret": SECRET_KEY,
            }
            access_token = str(
                requests.post(token_url, params=params).json().get("access_token")
            )
            url = config.config["qianfan_api"] + access_token
            print(url)
            if from_wxid in self.qianfan_data:
                self.qianfan_data[from_wxid]["messages"].append(
                    {"role": "user", "content": text_prompt}
                )
            else:
                self.qianfan_data[from_wxid] = {
                    "messages": [{"role": "user", "content": text_prompt}]
                }

            payload = json.dumps(self.qianfan_data[from_wxid])
            headers = {"Content-Type": "application/json"}
            response = requests.request("POST", url, headers=headers, data=payload)
            response = response.json()["result"]
            self.qianfan_data[from_wxid]["messages"].append(
                {"role": "assistant", "content": response}
            )
            asyncio.run(user_data.storge_data(from_wxid, text_prompt, response, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), model_name))
            time.sleep(1)
        except:
            print(response)
            response = "任务存在问题"
        return response

    def ecnu_chat(self, quest, text_prompt, from_wxid):
        # 该模型部署到了服务器,可远程调用,备选
        # ECNU educhat大模型
        model_name = "EduChat"
        try:
            url = "http://127.0.0.1:8001/chat"
            if from_wxid in self.ecnu_data:
                self.ecnu_data[from_wxid]["messages"].append(
                    {"role": "prompter", "content": text_prompt}
                )
            else:
                self.ecnu_data[from_wxid] = {
                    "messages": [{"role": "prompter", "content": text_prompt}]
                }
            self.ecnu_data[from_wxid]["user_QA"] = quest

            payload = json.dumps(self.ecnu_data[from_wxid])

            headers = {"Content-Type": "application/json"}
            # 发送请求
            response = requests.post(url, data=payload, headers=headers)
            response = response.json()["response"]
            self.ecnu_data[from_wxid]["messages"].append(
                {"role": "assistant", "content": response}
            )
            asyncio.run(user_data.storge_data(from_wxid, text_prompt, response, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), model_name))
            time.sleep(1)
        except:
            response = "任务存在问题"
            print(response)
        return response

    def thudm_chat(self, text_prompt, from_wxid):
        # 该模型部署到了服务器,可远程调用,备选
        # 模型 THUDM/ChatGLM2-6b
        model_name = "ChatGLM2"
        try:
            openai.api_base = "http://127.0.0.1:8002/v1"
            openai.api_key = "none"
            if from_wxid in self.thudm_data:
                self.thudm_data[from_wxid]["messages"].append(
                    {"role": "user", "content": text_prompt}
                )
            else:
                self.thudm_data[from_wxid] = {
                    "messages": [{"role": "user", "content": text_prompt}]
                }

            completion = openai.ChatCompletion.create(
                model="chatglm2-6b", messages=self.thudm_data[from_wxid]["messages"]
            )
            response = completion["choices"][0].message["content"]
            self.thudm_data[from_wxid]["messages"].append(
                {"role": "assistant", "content": response}
            )
            asyncio.run(user_data.storge_data(from_wxid, text_prompt, response, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), model_name))
            time.sleep(1)

        except:
            response = "任务存在问题"
            print(response)
        return response
