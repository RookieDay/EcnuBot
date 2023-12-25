# -*- coding: utf-8 -*-
import sys
import time
from utils import whisper_mp3
import ntchat
from model import multmsg_chat

wechat = ntchat.WeChat()
wechat.open(smart=True)
wechat.wait_login()
rooms = wechat.get_rooms()
nickname = wechat.get_self_info()["nickname"]

indirect_num = 0
for indirect_list in rooms:
    indirect_num += indirect_list["total_member"]
myself_wxid = wechat.get_self_info()["wxid"]
direct_num = len(wechat.get_contacts())
print("直接用户：%d人" % direct_num, "间接用户：%d人" % indirect_num, "群聊数量：%d" % len(rooms))


# 注册消息回调 新好友请求通知
@wechat.msg_register(ntchat.MT_RECV_FRIEND_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    multmsg_chat.addFriend_msg(wechat_instance, message)


# 注册消息回调 联系人新增通知
@wechat.msg_register(ntchat.MT_CONTACT_ADD_NOITFY_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    multmsg_chat.addContact_msg(wechat_instance, message)


# 注册消息回调 群成员新增通知
# @wechat.msg_register(ntchat.MT_ROOM_ADD_MEMBER_NOTIFY_MSG)
# def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
#     multmsg_chat.addContact_msg(wechat_instance, message)


# 注册消息回调 文本消息通知
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    multmsg_chat.scenes_msg(wechat_instance, message)


# 注册消息回调 文件消息通知
@wechat.msg_register(ntchat.MT_RECV_FILE_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    multmsg_chat.file_msg(wechat_instance, message)


# 注册消息回调 链接消息通知
@wechat.msg_register(ntchat.MT_RECV_LINK_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    multmsg_chat.link_msg(wechat_instance, message)


# 注册消息回调 语音消息通知
@wechat.msg_register(ntchat.MT_RECV_VOICE_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    multmsg_chat.voice_msg(wechat_instance, message, whisper_mp3)


# 注册监听所有消息回调 用于接收所有的通知消息
@wechat.msg_register(ntchat.MT_ALL)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    multmsg_chat.group_msg(wechat_instance, message)


# 让程序不结束
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
