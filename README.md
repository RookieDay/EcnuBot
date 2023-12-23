# EcnuBot
<p align="center" width="100%">
<a href="" target="_blank"><img src="https://github.com/RookieDay/EcnuBot/blob/main/examples/EcnuBot.png" alt="EcnuBot" style="width: 50%; min-width: 300px; display: block; margin: auto;"></a>
</p>

#### 华东师范大学专属智能客服，接入华东师范大学研发教育领域对话大模型[EduChat](https://github.com/THUDM/ChatGLM3) ，同时支持[ChatGLM3](https://github.com/THUDM/ChatGLM3)、[qwen-max](https://github.com/QwenLM/Qwen)等多种大模型支持，支持对开放问答、作文批改、启发式教学和情感支持等教育特色功能以及各大模型能力。

## 目录
- [功能介绍](#spiral_notepad-功能介绍)
- [本地部署](#robot-本地部署)
  - [硬件要求](#硬件要求)
  - [下载安装](#下载安装)
  - [部署示例](#部署示例)
- [快速体验](#fire-快速体验)
- [部分功能展示](#fountain_pen-部分功能展示)
- [未来计划](#construction-未来计划)
- [致谢](#link-致谢)
- [声明](#page_with_curl-声明)

----

## :spiral_notepad: 功能介绍

**⚡ 支持**   
* [x] web端
* [x] 自动问答
* [x] 知识库问答
* [x] 关键词触发回复
* [x] 私信语音识别答复
* [x] 自动添加好友
* [x] 自动拉入群聊
* [x] 拉入群聊@EcnuBot交互
* [x] 社群维护
* [x] 数据存储
* [x] 支持 EduChat 大模型
* [x] 支持 qwen-max 大模型
* [x] 支持 千帆 大模型
* [x] 支持 ChatGLM3 大模型
* [x] 更多大模型支持中...

## :robot: 本地部署
### 硬件要求

1. 本项目目前仅支持在windows上运行，由于本人电脑配置较低，所以将EduChat大模型部署至远程服务器，需开通[AutoDL](https://www.autodl.com/)账号，申请RTX 3090(24GB) * 2卡 资源
2. 本项目已支持web端体验，还在不断完善中，私戳[EcnuBot_web](https://github.com/RookieDay/EcnuBot_web)

### 下载安装
1. 安装对应版本[PC端](https://git.openi.org.cn/attachments/3bf60134-9d9d-437a-acf4-bfcc50521997?type=0)
2. 其他安装包可到[百度网盘](链接：https://pan.baidu.com/s/19o3a483vxXizCFlno6oZ1A?pwd=6dxf)自取，其中ffmpeg主要用于处理和操纵音频和视频文件
3. 下载本仓库内容至本地
```bash
git clone https://github.com/RookieDay/EcnuBot.git
cd EcnuBot
```
4. 安装相关依赖包

```bash
pip install -r requirements.txt
```

### 使用示例
1. 按照config.py文件备注，修改相关配置

2. [AutoDL](https://www.autodl.com/)服务端部署EduChat大模型，部署依托于[EduChat](https://github.com/THUDM/ChatGLM3) ，代码魔改已放置demo文件夹，可在服务端替换，如有疑问请私信EcnuBot。
```bash
# 两张显卡加载模型
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

model_path = "/root/autodl-tmp/educhat-sft-002-13b-baichuan"
config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
with init_empty_weights():
    model = AutoModelForCausalLM.from_config(
        config, torch_dtype=torch.float16, trust_remote_code=True
    )
model.tie_weights()
model = load_checkpoint_and_dispatch(
    model, model_path, device_map="auto", dtype=torch.float16
)
```

<details><summary><b>AutoDL配置</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/AutoDL.png)

</details>

3. 运行，启动服务

```bash
python .\main.py
```

## :fire: 快速体验
欢迎扫码入群，解锁EduChat全部能力，如有疑问，欢迎添加小助手微信（situerleng）为您解答。
<details><summary><b>EcnuBot体验群</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/wxGroup.png)

</details>


## :fountain_pen: 部分功能展示

<details><summary><b>能力菜单</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/menu.png)

</details>

<details><summary><b>文生图</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/txt2image.png)

</details>

<details><summary><b>ECNU 情感</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/EcnuEmotion.png)

</details>

<details><summary><b>语音识别</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/yuyin.png)

</details>

<details><summary><b>加群</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/ingrp.png)

</details>

<details><summary><b>其他大模型支持等</b></summary>

![image](https://github.com/RookieDay/EcnuBot/blob/main/examples/otherModel.png)

</details>

## :construction: 未来计划

初代EcnuBot主要集成EduChat教育大模型以及其他各大模型支持，随着面向群体以及用户的需求的扩大，从应用性等角度考虑，未来亦着手建设以下功能：

**⚡ 开发**  
* [ ] Mac版部署支持
* [ ] 学术解析等功能
* [ ] 用户信息分析等功能
* [ ] 文件内容识别处理、总结等功能
* [ ] 自定义角色等功能
* [ ] 插件支持等
* [ ] 数据存储优化等
* [ ] 低成本部署等（模型量化、CPU部署）
* [ ] 更多大模型接入
* [ ] 小程序、web端、手机端支持等多端应用
* [ ] ...... 


## :heart: 致谢

- [EduChat](https://github.com/icalk-nlp/EduChat) 开源支持 
- [千帆大模型](https://cloud.baidu.com/product/wenxinworkshop) 提供的接口服务 
- [通义千文问模型](https://www.aliyun.com/product/bailian) 提供的接口服务
- [whisper](https://github.com/openai/whisper) openai提供语音识别支持
- [awesome-chatgpt](https://github.com/uhub/awesome-chatgpt) 提供的开源技术支持

## :page_with_curl: 声明

本项目仅供研究目的使用，项目开发者对于使用本项目（包括但不限于数据、模型、代码等）所导致的任何危害或损失不承担责任。
