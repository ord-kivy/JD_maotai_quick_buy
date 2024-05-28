import configparser
import json
import warnings
import requests
import re
from urllib import parse
import time
from tools import utils
from tools.jd_sign import getSign

warnings.filterwarnings("ignore")


def getUrlParams(url):
    res = dict(parse.parse_qsl(url))
    return res


def get_cookie_string(cookie):
    cookie_string = ""
    for cookie_key in cookie.keys():
        cookie_string += "%s=%s;" % (cookie_key, cookie[cookie_key])
    return cookie_string


def get_jd_time():
    response = requests.get(
        url="https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5"
    )
    print(response.json())


def get_sk(data):
    data_val = [val for val in data["data"].values()]
    n, o, p, q, r, s = (
        data_val[0],
        data_val[1],
        data_val[2],
        data_val[3],
        data_val[4],
        data_val[5],
    )
    sk_val = ""
    if n == "cca":
        sk_val = p[14:19].lower() + o[5:15].upper()
    if n == "ab":  # check ok
        sk_val = r[10:18] + s[2:13].lower()
    if n == "ch":
        sk_val = q.upper() + r[6:10].upper()
    if n == "cbc":  # check ok
        sk_val = q[3:13].upper() + p[10:19].lower()
    if n == "by":
        sk_val = o[5:8] + re.sub("a", "c", p, flags=re.IGNORECASE)
    if n == "xa":
        sk_val = o[1:16] + s[4:10]
    if n == "cza":
        sk_val = q[6:19].lower() + s[5:11]
    if n == "cb":
        sk_val = s[5:14] + p[2:13].upper()

    return sk_val


class JDSecKillAPI:
    def __init__(self, sku, ck):
        self.skuId = sku
        self.s = requests.session()
        self.sku = sku
        self.ck = ck
        self.aid = "6f7e68aa-5b38-4a20-a971-41478d4f0772"
        self.eid = "eidAab4281218esdGQTaDRX9QrWRjWe8/TIYdxkE24gLaXbrVS2DA6FDHTA6DvyFJkD8" \
                   "/3Fzn1ad3Zp8oA6oRyt6ElO8rOyq2RilE7ngakzDGKnEy3Va "
        self.uuid = "23191589d81d4ef4"
        self.uts = "0f31TVRjBSsqndu4/jgUPz6uymy50MQJNdGPA8M8DwcXPjMzKz5N8X6EVhIJQl35adLPXD96o2gJzoCjUIQ" \
                   "+7VoW1pj2qDt3HCjvSWHxdAYMJkWSnOmfhVgpBY+bOAFaXupQw7n" \
                   "+Z2K62cSNSbXgX4VkZUGqOD5MqVbly0IV4YG2kAQqRSFYDH7WeMCXIpEtFKVFPiRvFwDXt8RMEU69WQ== "
        self.wifiBssid = "80885293e4c5736445e7f418ee6ca1f2"
        # self.ua = "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36"
        # self.ua = 'Mozilla/5.0 (Linux; Android 12; 22021211RC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046011 Mobile Safari/537.36'
        # self.ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1"
        self.ua = "okhttp/3.12.16;jdmall;android;version/12.1.0;build/98893;"

    # 预约操作
    def appoint_sku(self):
        # 协议头
        headers = {
            'Cookie': self.ck,
            'J-E-C': '%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1695984101202'
                     '%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22pin%22%3A%22GwvxG29kZzUyCK%3D%3D%22%7D%2C'
                     '%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall'
                     '%22%7D',
            'X-Rp-Client': 'android_3.0.0',
            'jdgs': '{"b1":"6f620b67-a8af-423b-ae64-8a0efc68a355","b2":"3.2.3.1_0","b3":"2.1",'
                    '"b4":"kvlMRxBK1LcMdkWOfMXPg48oH0dZkGBaI9Bv+zK8FifKYc3XHdsdC1xmn+a+rZ894h6wJz'
                    '/RrIEUdzAzImwJM9rfx7JR2DDMrXeT'
                    '+fvYeWyJ4rZpoiCp5pgGX9kzPIiP8FeIyAka2xYHazPuEMuQ2FKpOnxcnoBwg1KXh1OOxex+wuu'
                    '+9TZJqW3DQF74gReIWzqN2V/DckGoeLlA/u0r016rxgaaOyg4hO0Iv0'
                    '+n5hEAvHXyIL4G6gzwkJz2XFhaeuTcUsQAiQ8tYeG2QZPbGgsGUhjGSm6Fn'
                    '/h4RSFpgR509Tqc6SRODQdeQG4ULpvR25NYK0y+GBDGNMmK1mEr0r/Hrzu/o6YaxSVt21apZJELBN1z'
                    '+ECSCxPyNmejpSRHGUkfeOvIRyYfUYEwdg==","b5":"4f3b78c8fd4031a6ff4062b5bc2f5ed79e719cca",'
                    '"b7":"1695984151563","b6":"9c9f112267f3cc63c809148badd0fdc712b22fa6"}',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.16;jdmall;android;version/12.1.0;build/98893;',
            'X-Referer-Package': 'com.jingdong.app.mall',
            'Charset': 'UTF-8',
            'X-Referer-Page': 'com.jd.lib.productdetail.ProductDetailActivity',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'api.m.jd.com'
        }

        # 取13位时间戳
        ts = int(time.time() * 1000)
        # UUID
        uuid = self.uuid
        ep = utils.get_ep(ts, uuid)
        #
        query_params = {
            "functionId": "appoint",
            "clientVersion": "12.1.0",
            "build": "98893",
            "client": "android",
            "partner": "huaweiharmony",
            "oaid": self.aid,
            "sdkVersion": "29",
            "lang": "zh_CN",
            "harmonyOs": 1,
            "networkType": "wifi",
            "uts": self.uts,
            "uemps": "0-0-0",
            "ext": '{"prstate":"0","pvcStu":"1"}',
            "avifSupport": 1,
            "eid": self.eid,
            "ef": 1,
            'ep': json.dumps(ep, ensure_ascii=False, separators=(',', ':')),
        }
        # 请求地址
        reserve_url = "https://api.m.jd.com/client.action"

        body = {
            "autoAddCart": "0",
            "bsid": "",
            "check": "0",
            "ctext": "",
            "isShowCode": "0",
            "mad": "0",
            "skuId": self.skuId,
            "type": "4",
        }

        plainTextDic = {
            "st": ts,  # 毫秒级时间戳
            "sv": "120",
            "functionId": query_params["functionId"],
            "uuid": uuid,
            "client": query_params["client"],
            "clientVersion": query_params["clientVersion"],
            "body": json.dumps(body, ensure_ascii=False, separators=(",", ":")),
        }
        # 计算sign值
        st, sign, sv = getSign(plainTextDic)
        print("sign", sign)
        query_params.update(st=st)
        query_params.update(sign=sign)
        query_params.update(sv=sv)
        data = {"body": json.dumps(body, ensure_ascii=False, separators=(",", ":"))}

        response = self.s.post(
            url=reserve_url,
            params=query_params,
            data=data,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=3,
        )
        print(query_params)
        return response.json()


    # 获取token操作******************************************************************************************************
    def get_token_key(self):
        # 协议头
        headers = {
            'Cookie': self.ck,
            'J-E-C': '%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1695984101202'
                     '%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22pin%22%3A%22GwvxG29kZzUyCK%3D%3D%22%7D%2C'
                     '%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall'
                     '%22%7D',
            'X-Rp-Client': 'android_3.0.0',
            'jdgs': '{"b1":"6f620b67-a8af-423b-ae64-8a0efc68a355","b2":"3.2.3.1_0","b3":"2.1",'
                    '"b4":"kvlMRxBK1LcMdkWOfMXPg48oH0dZkGBaI9Bv+zK8FifKYc3XHdsdC1xmn+a+rZ894h6wJz'
                    '/RrIEUdzAzImwJM9rfx7JR2DDMrXeT'
                    '+fvYeWyJ4rZpoiCp5pgGX9kzPIiP8FeIyAka2xYHazPuEMuQ2FKpOnxcnoBwg1KXh1OOxex+wuu'
                    '+9TZJqW3DQF74gReIWzqN2V/DckGoeLlA/u0r016rxgaaOyg4hO0Iv0'
                    '+n5hEAvHXyIL4G6gzwkJz2XFhaeuTcUsQAiQ8tYeG2QZPbGgsGUhjGSm6Fn'
                    '/h4RSFpgR509Tqc6SRODQdeQG4ULpvR25NYK0y+GBDGNMmK1mEr0r/Hrzu/o6YaxSVt21apZJELBN1z'
                    '+ECSCxPyNmejpSRHGUkfeOvIRyYfUYEwdg==","b5":"4f3b78c8fd4031a6ff4062b5bc2f5ed79e719cca",'
                    '"b7":"1695984151563","b6":"9c9f112267f3cc63c809148badd0fdc712b22fa6"}',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.16;jdmall;android;version/12.1.0;build/98893;',
            'X-Referer-Package': 'com.jingdong.app.mall',
            'Charset': 'UTF-8',
            'X-Referer-Page': 'com.jd.lib.productdetail.ProductDetailActivity',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'api.m.jd.com'
        }
        ts = int(time.time() * 1000)
        uuid = self.uuid
        ep = utils.get_ep(ts, uuid)
        query_params = {
            "functionId": "genToken",
            "clientVersion": "12.1.0",
            "build": "98893",
            "client": "android",
            "partner": "huaweiharmony",
            "oaid": self.aid,
            "sdkVersion": "29",
            "lang": "zh_CN",
            "harmonyOs=1": 1,
            "networkType": "wifi",
            "uts": self.uts,
            "uemps": "0-0-0",
            "ext": '{"prstate":"0","pvcStu":"1"}',
            "avifSupport": 1,
            "eid": self.eid,
            "ef": 1,
            'ep': json.dumps(ep, ensure_ascii=False, separators=(',', ':')),
        }

        body = {
            "action": "to",
            "to": "https://divide.jd.com/user_routing?skuId=" + self.sku,
        }

        plainTextDic = {
            "st": ts,  # 毫秒级时间戳
            "sv": "120",
            "functionId": query_params["functionId"],
            "uuid": uuid,
            "client": query_params["client"],
            "clientVersion": query_params["clientVersion"],
            "body": json.dumps(body, ensure_ascii=False, separators=(",", ":")),
        }
        st, sign, sv = getSign(plainTextDic)

        query_params.update(st=st)
        query_params.update(sign=sign)
        query_params.update(sv=sv)

        data = {"body": json.dumps(body, ensure_ascii=False, separators=(",", ":"))}

        response = self.s.post(
            url="https://api.m.jd.com/client.action",
            params=query_params,
            data=data,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=3,
        )
        token_key = response.json()['tokenKey']
        print("token_key",token_key)
        print('Token Key: ----------> %s' % response.json())
        print(response.status_code)
        json_obj = response.json()
        print("Get genToken--------------->%s" % str(json_obj))
        return json_obj

    def get_appjmp(self, token_params):
        headers = {"user-agent": self.ua}
        appjmp_url = token_params["url"]
        params = {
            "to": "https://divide.jd.com/user_routing?skuId=%s" % self.skuId,
            "tokenKey": token_params["tokenKey"],
        }

        response = self.s.get(
            url=appjmp_url,
            params=params,
            allow_redirects=False,
            verify=False,
            headers=headers,
        )
        print("Get Appjmp跳转链接-------------->%s" % response.headers["Location"])
        return response.headers["Location"]

    def get_divide(self, divide_url):
        headers = {"user-agent": self.ua}
        response = self.s.get(
            url=divide_url, allow_redirects=False, verify=False, headers=headers
        )
        print("Get Divide跳转链接-------------->%s" % response.headers["Location"])
        return response.headers["Location"]

    def get_captcha(self, captcha_url):
        headers = {"user-agent": self.ua}
        response = self.s.get(
            url=captcha_url, allow_redirects=False, verify=False, headers=headers
        )
        print("Get Captcha跳转链接-------------->%s" % response.headers["Location"])
        return response.headers["Location"]

    def visit_seckill(self, seckill_url):
        headers = {"user-agent": self.ua}
        response = self.s.get(
            url=seckill_url, allow_redirects=False, verify=False, headers=headers
        )
        return response

    # 抢单函数,num定义数量*********************************************************************************************
    # **************************************************************************************************************
    # 创建配置解析器对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('config.ini')

    # 获取配置项的值

    def init_action(self, num=config.get('number', 'num')):
        print("num:", num)
        try:
            headers = {"user-agent": self.ua, "Connection": "keep-alive"}
            init_action_url = (
                "https://marathon.jd.com/seckillnew/orderService/init.action"
            )
            data = {
                "sku": self.skuId,
                "num": num,
                "id": 0,
                "provinceId": 0,
                "cityId": 0,
                "countyId": 0,
                "townId": 0,
            }
            response = self.s.post(
                url=init_action_url,
                data=data,
                allow_redirects=False,
                verify=False,
                headers=headers,
            )
            print("init action返回数据：%s" % response.text)
            # JDSecKillSubmit.log("init action返回数据：%s" % response.text)
            return response.json()
        except Exception as e:
            print(str(e))
            return None

    def get_tak(self):
        try:
            headers = {"user-agent": self.ua, "Connection": "keep-alive"}
            tak_url = "https://tak.jd.com/t/871A9?_t=%d" % (
                int(round(time.time() * 1000))
            )
            response = self.s.get(
                url=tak_url, allow_redirects=False, verify=False, headers=headers
            )
            sk_val = get_sk(data=response.json())
            return sk_val
        except Exception as e:
            print(str(e))
            return ""

    def submit_order(self, order_data, sk):
        try:
            headers = {"user-agent": self.ua, "Connection": "keep-alive"}
            submit_order_url = (
                    "https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=%s"
                    % self.skuId
            )
            address_info = order_data["address"]
            invoice_info = order_data["invoiceInfo"]
            data = {
                "num": order_data["seckillSkuVO"]["num"],
                "addressId": address_info["id"],
                "yuShou": True,
                "isModifyAddress": False,
                "name": address_info["name"],
                "provinceId": address_info["provinceId"],
                "provinceName": address_info["provinceName"],
                "cityId": address_info["cityId"],
                "cityName": address_info["cityName"],
                "countyId": address_info["countyId"],
                "countyName": address_info["countyName"],
                "townId": address_info["townId"],
                "townName": address_info["townName"],
                "addressDetail": address_info["addressDetail"],
                "mobile": address_info["mobile"],
                "mobileKey": address_info["mobileKey"],
                "email": "",
                "invoiceTitle": invoice_info["invoiceTitle"],
                "invoiceContent": invoice_info["invoiceContentType"],
                "invoicePhone": invoice_info["invoicePhone"],
                "invoicePhoneKey": invoice_info["invoicePhoneKey"],
                "invoice": True,
                "codTimeType": "3",
                "paymentType": "4",
                "overseas": "0",
                "token": order_data["token"],
                # "sk": sk,
            }

            response = self.s.post(
                url=submit_order_url,
                data=data,
                allow_redirects=False,
                verify=False,
                headers=headers,
            )
            return response.json()
        except Exception as e:
            print("提交错误 error--->" + str(e))
            return None

    def send_message(self, content):
        pass
        # try:
        #     # 推送token
        #     PUSH_TOKEN = "AT_4XxUFvSjSLWTlFhX1nFmIepe1RNoGq8b"

        #     UIDS = [
        #         "UID_D77yyDO0pT7K0f1q2UijDTGnGthF",
        #     ]
        #     msg = WxPusher.send_message(content, uids=UIDS, token=PUSH_TOKEN)
        # except Exception as e:
        #     print("send_message error--->" + str(e))


if __name__ == "__main__":
    # 创建配置解析器对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('config.ini')
    # 获取配置项的值
    sku = config.get('skuId', 'sku')
    ck = config.get('cookies', 'ckLong')
    # ck = 'wskey=AARklXecAECOliANxM81qWLIXZ5ibhKwZB5uL7nBHtiSCwb5ORlpGqOa0_93VKW4rC2CxaEO2dDxAubnvJFdzogZ15QhIEiR;whwswswws=JD012145b9RiaZd1Kf3G169598410584505igLZWes-q_D_rkzmAUSfsktnhrwqUYfb5i2tsZwACxctDLLK5dCZ14nd0BapXj64oJQEpsKsuIcfe1wjK7xoaQ0yo642p~AAkEWiOCKEAAAAAAAAAAAAAAAACMZFYnYHU70fwAAAApCaWdDb25nNTIw;unionwsws={"devicefinger":"eidAab4281218esdGQTaDRX9QrWRjWe8\\/TIYdxkE24gLaXbrVS2DA6FDHTA6DvyFJkD8\\/3Fzn1ad3Zp8oA6oRyt6ElO8rOyq2RilE7ngakzDGKnEy3Va","jmafinger":"JD012145b9RiaZd1Kf3G169598410584505igLZWes-q_D_rkzmAUSfsktnhrwqUYfb5i2tsZwACxctDLLK5dCZ14nd0BapXj64oJQEpsKsuIcfe1wjK7xoaQ0yo642p~AAkEWiOCKEAAAAAAAAAAAAAAAACMZFYnYHU70fwAAAApCaWdDb25nNTIw"};pin_hash=1484288750;',
    jdapi = JDSecKillAPI(sku, ck)
    print("预约结果--->", jdapi.appoint_sku())
    # print("gentoken结果--->", jdapi.get_token_key())