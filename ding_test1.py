#coding=utf-8
import urllib2
import json
import requests

corp_id = ""
corp_secret = ""
agent_id = ""


# 获取企业的access_token, 2小时过期
def get_access_token():
    url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' % (corp_id, corp_secret)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response_str = response.read()
    response_dict = json.loads(response_str)
    error_code_key = "errcode"
    access_token_key = "access_token"
    if response_dict.has_key(error_code_key) and response_dict[error_code_key] == 0 and response_dict.has_key(access_token_key):
        return response_dict[access_token_key]
    else:
        return ''

# 发送工作通知，给某个人或多个人发送信息
def send_text_to_users(users, text):
    access_token = get_access_token()
    msg_type, msg = _gen_text_msg(text)
    return _send_msg_to_users(access_token, users, msg_type, msg)

def _gen_text_msg(text):
    msg_type = 'text'
    msg = {"content": text}
    return msg_type, msg


def _send_msg_to_users(access_token, users, msg_type, msg):
    to_users = '|'.join(users)
    print to_users, 1111111
    body_dict = {
        "touser": to_users,
        "agentid": agent_id,
        "msgtype": "oa",
        "oa": {
                "message_url": "http://mobilejs.jxtbkt.com/",
                "head": {
                    "bgcolor": "FFBBBBBB",
                    "text": "小明的反馈"
        },
        "body": {
            "title": "2017-8-13 小明的反馈",
             "form": [
             {
                            "key": "反馈人:",
                            "value": "张三"
                        },
                        {
                            "key": "问题:",
                            "value": "自己是sb"
                        },
                        {
                            "key": "手机号:",
                            "value": "123456789"
                        },
                        {
                            "key": "出现问题的姓名班级:",
                            "value": "1奶奶级10班"
                        },
                        {
                            "key": "客户端:",
                            "value": "ios"
                        },
                        {
                            "key": "版本:",
                            "value": "ios.2.2.14"
                        }
                    ],
                    "content": "打开应用一直在加载中",
                    "author": "小明 "
                }
            }
    }
    body_dict[msg_type] = msg
    body = json.dumps(body_dict)
    access_token = access_token
    url = "https://oapi.dingtalk.com/message/send?access_token=%s" % access_token
    r = requests.post(url, body)
    if r.json().get("errcode", 0) == 40014:
        url = "https://oapi.dingtalk.com/message/send?access_token=%s" % get_access_token()
        requests.post(url, body)
    print r.json()
send_text_to_users(["manager1137"], "2018-5-22 刘帅asdasdadasdas的反馈")



