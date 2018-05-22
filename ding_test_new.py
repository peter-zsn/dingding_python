#coding=utf-8
"""
调取钉钉应用的第三方接口，向某个钉钉人员反馈信息
此接口的限流限流规则包括：1、给同一用户发相同内容消息一天仅允许一次；2、给同一用户发消息一天不超过100次
"""

import requests
import json

corp_id = ""                                            # 企业id
corp_secret = ""            # 企业key
agent_id = ""                                                                      # 钉钉应用的id


class DingTalk:
    def __init__(self):
        self.corp_id = corp_id                                              # 企业id
        self.corp_secret = corp_secret                                      # 企业key
        self.agent_id = agent_id                                            # 钉钉应用的id
        self.get_token_url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' % (self.corp_id, self.corp_secret)        # 获取access_token的地址
        self.send_data_url = "https://oapi.dingtalk.com/message/send?access_token=%s"              # 发送信息的地址

    def get_access_token(self):
        """
        获取access_token,  两小时过期， 因此每次调用都重新获取access_token
        :return:
        """
        r = requests.get(url=self.get_token_url)
        data = r.json()
        if r.status_code == 200 and data.get("access_token", "") != "":
            return data.get("access_token")
        else:
            return ""

    def send_text_msg(self, to_users, text):
        """
        "touser": to_users,             # 接收人的userIds  列表["1", "2"]
        "msgtype": "text",              # 消息格式
        "text": "老宋"                #  消息内容
        发送消息text形式的给接收者
        :return:
        """
        to_users = "|".join(to_users)
        data = {
            "touser": to_users,
            "agentid": self.agent_id,
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        err = self._send_msg(data)
        if err:
            return False, err
        return True, ""

    def send_oa_msg(self, to_users, oa):
        """
        发送消息oa形式的给接收者
        "touser": to_users,             # 接收人的userIds  列表["1", "2"]
        "msgtype": "oa",                # 消息格式
        "oa": {                         # 内容主体
            "message_url": "http://mobilejs.jxtbkt.com/",           # 手机端能打开的链接地址
            "head": {
                "bgcolor": "FFBBBBBB",                              # 颜色
                "text": "小明的反馈"                                 # 标题
                },
            "body": {                                                   # 主题
                "title": "2017-8-13 小明的反馈",
                 "form": [
                    {
                        "key": "反馈人:",
                        "value": "张三"
                    },...
                ],
                "content": "打开应用一直在加载中",                        # 主体内容
                "author": "小明 "                                       # 作者
            }
        }
        :return:
        """
        to_users = "|".join(to_users)
        data = {
            "touser": to_users,
            "agentid": self.agent_id,
            "msgtype": "oa",
            "oa": oa
        }
        err = self._send_msg(data)
        if err:
            return False, err
        return True, ""

    def send_link_msg(self, to_users, link):
        """
        发送链接信息
        :param to_users:
        :param link:
            {
                "messageUrl": "http://user.jxtbkt.cn/",              # 消息点击链接地址
                "title": "5-22日-小胖孩的反馈",                        # 消息标题
                "text": "点击应用一直处在加载中"                        # 	消息描述
            }
        :return:
        """
        to_users = "|".join(to_users)
        data = {
            "touser": to_users,
            "agentid": self.agent_id,
            "msgtype": "link",
            "link":  link
        }
        err = self._send_msg(data)
        if err:
            return False, err
        return True, ""

    def _send_msg(self, data):
        """
        发送信息
        :param data:
        :return: error or ""
        """
        r = requests.post(self.send_data_url % self.get_access_token(), json.dumps(data))
        result = r.json()
        if r.status_code != 200 or result.get("errcode", 12) == 12:
            return u'发送钉钉消息错误, 消息未发出%s' % result.get("errmsg")
        return ""

    def upload_media(self, file_path, file_name):
        """
        上传图片文件, 图片大小不能超过1M
        :return:
        """
        url = "https://oapi.dingtalk.com/media/upload?access_token=%s&type=%s" % (self.get_access_token(), "image")
        file = {"media": open(file_path, 'rb')}
        data = {
            "media": file_name
        }
        r = requests.post(url, data=data, files=file)
        result = r.json()
        if r.status_code != 200 or result.get("errcode", 12) == 12:
            return ""
        else:
            return result.get("media_id", "")

    def get_media(self, media_id):
        # media_id = "@lADPBY0V41ftY7LNBDjNB4A"
        url = "https://oapi.dingtalk.com/media/downloadFile?access_token=%s&media_id=%s" % (self.get_access_token(), media_id)
        print url
        requests.get(url)


DingTest = DingTalk()
# print DingTest.upload_media("1.jpg", "1.jpg"), 11111111111

# flag, err = DingTest.send_text_msg(["manager1137"], "老宋")
# print flag, err
#
oa = {                         # 内容主体
        "message_url": "http://mobilejs.jxtbkt.com/",           # 手机端能打开的链接地址
            "head": {
                "bgcolor": "FFBBBBBB",                              # 颜色
                "message_url": "http://mobilejs.jxtbkt.com/",           # 手机端能打开的链接地址
                },
            "body": {                                                   # 主题
                "title": "2017-8-13 小明的反馈",
                 "form": [
                    {
                        "key": "反馈人:",
                        "value": "张三"
                    },
                     {
                         "key": "账号信息",
                         "value": "15班小刘，手机号：13600000000"
                     }
                ],
                "content": "打开应用一直在加载中",                        # 主体内容
                "author": "小明 ",                                       # 作者
                "image": "@lADPBY0V41ftY7LNBDjNB4A"
            }
        }
flag, err = DingTest.send_oa_msg(["manager1137"], oa)
print flag, err
#
# link = {
#           "messageUrl": "http://user.jxtbkt.cn/",
#           "title": "5-22日-小胖孩1的反馈",
#           "text": "点击应用1一直处在加载中,啊实打实大苏打似的亲卫队请问大概把"
#                   "数据库考法硕联考的饭卡里说的块钱我翻出来看你卢卡斯能货到付款进",
#           "picUrl": "@lADOADmaWMzazQKA"
# }
# flag, err = DingTest.send_link_msg(["manager1137"], link)
# print flag, err