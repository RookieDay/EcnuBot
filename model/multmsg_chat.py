# -*- coding: utf-8 -*-
import asyncio
import random
import time
import xml.dom.minidom
from utils import config, drawer
from .model_chat import Model_list, user_QA

# ecnu chat
bot_hi = f"您好，我是EcnuBot，您的AI小伙伴。目前支持以下能力：\n\n1. 【文生图】交互方式：绘画 英文描述\n如：绘画 snowing winter, super cute baby pixar style white fairy bear, shiny snow-white fluffy, big bright eyes, wearing a woolly cyan hat, delicate and fine, ...\n\n2.【自动问答】交互方式\n(1) Educhat大模型：\n    ECNU 问答 描述\n    ECNU 教学 描述\n    ECNU 情感 描述\n    ECNU 情感 inner 描述\n(2) 通义千问大模型：千问 描述\n(3) ChatGLM3：ChatGLM3 描述\n(4) 千帆大模型：千帆 描述\n(5) 千帆大模型：描述\n\n3.【答复语音】交互方式：私信EcnuBot发送语音\n\n4.【其他】如您未在EcnuBot交流群，可私信EcnuBot发送“加群”，即可加入EcnuBot交流群。\n\n注：群聊内需@EcnuBot才可触发上述功能，且@是真正@，并非复制！"
bot_hi_newFri = f"您好，我是EcnuBot，您的AI小伙伴。您可以私信EcnuBot发送“加群”，加入EcnuBot体验交流群。"
models = Model_list()


def scenes_msg(wechat_instance, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    room_wxid = data["room_wxid"]
    input_prompt = data["msg"].strip()
    nickname = wechat_instance.get_self_info()["nickname"]

    print("input_prompt")
    print(input_prompt)
    # 判断消息不是自己发的&不是群消息->回复对方
    if from_wxid != self_wxid and not room_wxid:
        if input_prompt == "加群":
            try:
                member = []
                room_wxid = config.config["room_wxid"]
                member.append(data["from_wxid"])

                sleep_time = random.randint(0, 4)
                time.sleep(sleep_time)
                wechat_instance.invite_room_member(room_wxid, member_list=member)
                sleep_time = random.randint(0, 4)
                time.sleep(sleep_time)
            except:
                wechat_instance.send_text(to_wxid=from_wxid, content=f"任务存在问题，请联系作者。")

        elif input_prompt.split(" ")[0] == "菜单":
            wechat_instance.send_text(to_wxid=from_wxid, content=bot_hi)

        elif input_prompt.split(" ")[0] == "对话":
            text_prompt = input_prompt.replace("对话", "").strip()
            response = models.knowledge_chat(text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="【知识库对话回复】" + "\n" + response
            )
        elif input_prompt.split(" ")[0] == "结束对话":
            text_prompt = input_prompt.split(" ")[0].strip()
            response = models.knowledge_chat(text_prompt, from_wxid)
            wechat_instance.send_text(to_wxid=from_wxid, content="【知识库对话已结束】")

        elif input_prompt.split(" ")[0] == "绘画":
            text_prompt = data["msg"].split(" ")[1]
            wechat_instance.send_text(to_wxid=from_wxid, content=f"正在作画，请您耐心等待！")
            try:
                file_path = config.config["file_path"]
                print(file_path)
                image_list = asyncio.run(drawer.image_url(text_prompt, file_path))
                for i, image_path in enumerate(image_list):
                    time.sleep(1)
                    wechat_instance.send_image(to_wxid=from_wxid, file_path=image_path)
                    if i == 2:
                        break
                time.sleep(6)
                wechat_instance.send_text(to_wxid=from_wxid, content="图像已生成完毕，希望您喜欢。")
            except:
                wechat_instance.send_text(to_wxid=from_wxid, content="文生图功能暂时关闭。")

        elif input_prompt.split(" ")[0] == "千问":
            text_prompt = input_prompt.replace("千问 ", "")
            response = models.qianwen(text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="【通义千问大模型回复】" + "\n" + response
            )

        elif input_prompt.split(" ")[0] == "ChatGLM3":
            text_prompt = input_prompt.replace("ChatGLM3", "")
            response = models.qianwen_chatgml3(text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="【ChatGLM3-6B大模型回复】" + "\n" + response
            )

        elif input_prompt.split(" ")[0] == "千帆":
            text_prompt = input_prompt.replace("千帆 ", "")
            response = models.qianfan(text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="【百度千帆大模型回复】" + "\n" + response
            )

        elif input_prompt.split(" ")[0] == "ECNU":
            quest = ""
            for question in user_QA:
                if question in input_prompt:
                    quest = question
                    break
            # text_prompt = input_prompt.replace('ECNU ', '')
            text_prompt = input_prompt.replace(quest, "").strip()
            response = models.ecnu_chat(quest, text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="【ECNU大模型回复】" + "\n" + response
            )

        elif input_prompt.split(" ")[0] == "清华":
            text_prompt = input_prompt.replace("清华 ", "")
            wechat_instance.send_text(to_wxid=from_wxid, content="正在回答请您稍等！")
            response = models.thudm_chat(text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="【ChatGLM2大模型回复】" + "\n" + response
            )
        else:
            text_prompt = input_prompt
            response = models.qianfan(text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="【百度千帆大模型回复】" + "\n" + response
            )

    # 群聊
    elif from_wxid != self_wxid and room_wxid:
        member = []
        black_wxid = config.config["black_wxid"]
        member.append(data["from_wxid"])
        room_wxid = data["room_wxid"]
        article_prompt = data["msg"].strip()
        if article_prompt.split(" ")[0] == "对话":
            text_prompt = article_prompt.replace("对话", "").strip()
            response = models.knowledge_chat(text_prompt, from_wxid)
            wechat_instance.send_room_at_msg(
                to_wxid=room_wxid,
                content="{$@} " + "【知识库对话回复】" + "\n" + response,
                at_list=member,
            )
        elif article_prompt.split(" ")[0] == "结束对话":
            text_prompt = article_prompt.split(" ")[0].strip()
            response = models.knowledge_chat(text_prompt, from_wxid)
            wechat_instance.send_room_at_msg(
                to_wxid=room_wxid,
                content="{$@} " + "【知识库对话已结束】" + "\n" + response,
                at_list=member,
            )

        if "@" + nickname in data["msg"]:
            at_nickname = "@" + nickname
            if "\u2005" in data["msg"].replace(at_nickname, ""):
                input_prompt = data["msg"].replace(at_nickname + "\u2005", "").strip()
            elif at_nickname + " " in data["msg"]:
                input_prompt = data["msg"].replace(at_nickname + " ", "").strip()
            else:
                input_prompt = data["msg"].replace(at_nickname, "").strip()

            if data["from_wxid"] not in black_wxid:
                if "菜单" in data["msg"]:
                    wechat_str = bot_hi
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content="{$@} " + "\n" + wechat_str,
                        at_list=member,
                    )

                elif input_prompt.split(" ")[0] == "绘画":
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid, content="{$@} 好哦,请您稍等！", at_list=member
                    )
                    text_prompt = input_prompt.split(" ")[1]
                    try:
                        file_path = config.config["file_path"]
                        print("................................")
                        print(file_path)
                        image_list = asyncio.run(
                            drawer.image_url(text_prompt, file_path)
                        )
                        for i, image_path in enumerate(image_list):
                            time.sleep(1)

                            wechat_instance.send_image(
                                to_wxid=room_wxid, file_path=image_path
                            )
                            if i == 2:
                                break
                        time.sleep(6)
                        wechat_instance.send_room_at_msg(
                            to_wxid=room_wxid,
                            content="{$@}" + "图像已生成完毕，希望您喜欢。",
                            at_list=member,
                        )
                        # 拍一拍
                        # time.sleep(1)
                        # wechat_instance.send_pat(room_wxid=room_wxid,
                        #                             patted_wxid=data['from_wxid'])
                    except:
                        wechat_instance.send_room_at_msg(
                            to_wxid=room_wxid,
                            content="{$@} " + "文生图功能暂时关闭",
                            at_list=member,
                        )
                elif input_prompt.split(" ")[0] == "千问":
                    text_prompt = input_prompt.replace("千问 ", "")
                    response = models.qianwen(text_prompt, from_wxid)
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content="{$@} " + "【通义千问大模型回复】" + "\n" + response,
                        at_list=member,
                    )

                elif input_prompt.split(" ")[0] == "ChatGLM3":
                    text_prompt = input_prompt.replace("ChatGLM3", "")
                    response = models.qianwen_chatgml3(text_prompt, from_wxid)
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content="{$@} " + "【ChatGLM3-6B大模型回复】" + "\n" + response,
                        at_list=member,
                    )

                elif input_prompt.split(" ")[0] == "千帆":
                    text_prompt = input_prompt.replace("千帆 ", "")
                    response = models.qianfan(text_prompt, from_wxid)
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content="{$@} " + "【百度千帆大模型回复】" + "\n" + response,
                        at_list=member,
                    )

                elif input_prompt.split(" ")[0] == "ECNU":
                    quest = ""
                    for question in user_QA:
                        if question in input_prompt:
                            quest = question
                            break
                    # text_prompt = input_prompt.replace('ECNU ', '')
                    text_prompt = input_prompt.replace(quest, "").strip()
                    response = models.ecnu_chat(quest, text_prompt, from_wxid)
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content="{$@} " + "【ECNU大模型回复】" + "\n" + response,
                        at_list=member,
                    )

                elif input_prompt.split(" ")[0] == "清华":
                    text_prompt = input_prompt.replace("清华 ", "")
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid, content="{$@} 正在回答，请您稍等！", at_list=member
                    )
                    response = models.thudm_chat(text_prompt, from_wxid)
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content="{$@} " + "【ChatGLM2大模型回复】" + "\n" + response,
                        at_list=member,
                    )

                else:
                    text_prompt = input_prompt
                    response = models.qianfan(text_prompt, from_wxid)
                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content="{$@} " + "【百度千帆大模型回复】" + "\n" + response,
                        at_list=member,
                    )


def voice_msg(wechat_instance, message, whisper_mp3):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    room_wxid = data["room_wxid"]
    type_wx = message["type"]

    if from_wxid != self_wxid and not room_wxid:
        # 语音的type
        if type_wx == 11048:
            mp3_file = data["mp3_file"]
            wechat_instance.send_text(to_wxid=from_wxid, content=f"正在为您解答，请您耐心等待！")
            mp3_text = whisper_mp3.whisper_mp3(mp3_file)
            print("mp3_text..............", mp3_text)
            text_prompt = mp3_text
            response = models.qianfan(text_prompt, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid,
                content="【百度千帆大模型回复】" + "\n" + "语音转文字:" + mp3_text + "\n" + response,
            )

    # 以下的通过接口的实现方式，
    # url = "http://127.0.0.1:8000/content"
    # params = {"mp3_txt": mp3_text}
    # # 设置请求头
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    # }
    # # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
    # response = requests.get(
    #     url, params=params, headers=headers
    # )
    # wechat_instance.send_text(to_wxid=from_wxid, content=response.json())


def group_msg(wechat_instance, message):
    type_wx = message["type"]
    if type_wx == 11098:
        data = message["data"]
        member_wxid = data["member_list"][0]["wxid"]
        member = []
        member.append(member_wxid)
        room_wxid_ = data["room_wxid"]
        time.sleep(0.5)
        try:
            main_room_wxid = config.config["room_wxid"]
            if room_wxid_ == main_room_wxid:
                sleep_time = random.randint(0, 4)
                time.sleep(sleep_time)
                wechat_instance.send_room_at_msg(
                    to_wxid=room_wxid_,
                    content="{$@},欢迎加入EcnuBot交流群！详细内容可看群公告.\n\n温馨提示：@EcnuBot回复“菜单”可解锁EcnuBot全部能力。",
                    at_list=member,
                )
        except:
            pass


def file_msg(wechat_instance, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    room_wxid = data["room_wxid"]

    print("data")
    print(data)
    # 判断消息不是自己发的->回复对方
    if from_wxid != self_wxid:
        if room_wxid:
            member = []
            member.append(data["from_wxid"])
            wechat_instance.send_room_at_msg(
                to_wxid=room_wxid,
                content="{$@} "
                + "\n"
                + "正在为您生成摘要，请稍等"
                + "\n"
                + "发送【对话 描述】即可与该文档内容开始对话"
                + "\n"
                + "发送【结束对话】即可与该文档内容结束对话",
                at_list=member,
            )
            time.sleep(0.5)
            knowledge_gene = models.knowledge_generate(data, from_wxid)
            wechat_instance.send_room_at_msg(
                to_wxid=room_wxid,
                content="{$@} " + "摘要如下：" + "\n" + knowledge_gene,
                at_list=member,
            )

            pass
        else:
            wechat_instance.send_text(
                to_wxid=from_wxid,
                content="正在为您生成摘要，请稍等"
                + "\n"
                + "发送【对话 描述】即可与该文档内容开始对话"
                + "\n"
                + "发送【结束对话】即可与该文档内容结束对话",
            )
            time.sleep(0.5)
            knowledge_gene = models.knowledge_generate(data, from_wxid)
            wechat_instance.send_text(
                to_wxid=from_wxid, content="摘要如下：" + "\n" + knowledge_gene
            )


def addFriend_msg(wechat_instance, message):
    xml_content = message["data"]["raw_msg"]
    dom = xml.dom.minidom.parseString(xml_content)
    # 从xml取相关参数
    encryptusername = dom.documentElement.getAttribute("encryptusername")
    ticket = dom.documentElement.getAttribute("ticket")
    scene = dom.documentElement.getAttribute("scene")
    # 自动同意好友申请
    wechat_instance.accept_friend_request(encryptusername, ticket, int(scene))

    from_wxid = dom.documentElement.getAttribute("fromusername")
    time.sleep(1)
    wechat_instance.send_text(to_wxid=from_wxid, content=bot_hi_newFri)


def addContact_msg(wechat_instance, message):
    type_wx = message["type"]

    if type_wx == 11098:
        member = []
        data = message["data"]
        member_wxid = data["member_list"][0]["wxid"]
        member.append(member_wxid)
        room_wxid_ = data["room_wxid"]
        time.sleep(0.5)
        main_room_wxid = config.config["room_wxid"]

        if room_wxid_ == main_room_wxid:
            sleep_time = random.randint(0, 4)
            time.sleep(sleep_time)
            wechat_instance.send_room_at_msg(
                to_wxid=room_wxid_,
                content="{$@},欢迎加入EcnuBot交流群！详细内容可看群公告.\n\n温馨提示：@EcnuBot回复“菜单”可解锁EcnuBot全部能力。",
                at_list=member,
            )
