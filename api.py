# -*- coding: utf-8 -*-
import requests
import json
import time
import hashlib

market_url = "http://api.coinbene.com/v1/market/"
trade_url = "http://api.coinbene.com/v1/trade/"
header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko", \
               "Content-Type": "application/json;charset=utf-8", "Connection": "keep-alive"}

# timestamp = create_timestamp()

class Coinbene(object):
    #  此处为API请求地址及参数
    def __init__(self, api, secret):
    #  获取最新价
    #  此处为APIID SECRET
        self.apiid  = api
        self.secret = secret

    def http_request(self, url, data):
        if data == None:
            response = requests.get(url, headers=header_dict)
        else:
            response = requests.post(url, data=json.dumps(data), headers=header_dict)
        try:
            # if response.status_code == 200:
            #     return json.loads(response.text)
            # else:
            #     return None
            content = response.json()
            # print(content)
            return content
        except Exception as e:
            print('http failed : %s' % e)
            return None

    def http_get_nosign(self, url):
        return self.http_request(url, data=None)

    def http_post_sign(self, url, dic):
        dic['appid'] = self.apiid
        dic['secret'] = self.secret
        dic['timestamp'] = self.create_timestamp()
        mysign = self.sign(**dic)
        del dic['secret']
        dic['sign'] = mysign
        return self.http_request(url, data=dic)

    #  生成签名sign
    def sign(self, **kwargs):
        """
        将传入的参数生成列表形式，排序后用＆拼接成字符串，用hashbli加密成生sign
        """
        sign_list = []
        for key, value in kwargs.items():
            sign_list.append("{}={}".format(key, value))


        sign_list.sort()
        sign_str = "&".join(sign_list)
        mysecret = sign_str.upper().encode()
        m = hashlib.md5()
        m.update(mysecret)
        return m.hexdigest()

    #  生成时间戳
    def create_timestamp(self):
        timestamp = int(round(time.time() * 1000))
        return timestamp

    def get_ticker(self, symbol):
        """
        symbol必填，为all或交易对代码:btcusdt
        """
        url = market_url + "ticker?symbol=" + str(symbol)
        return self.http_get_nosign(url)


    #  获取挂单
    def get_orderbook(self, symbol, depth=200):
        """
        depth为选填项，默认为200
        """
        url = market_url + "orderbook?symbol=" + symbol + "&depth=" + str(depth)
        return self.http_get_nosign(url)


    #  获取成交记录
    def get_trade(self, symbol, size=300):
        """
        size:获取记录数量，按照时间倒序传输。默认300
        """
        url = market_url + "trades?symbol=" + symbol + "&size=" + str(size)
        return self.http_get_nosign(url)


    #  查询账户余额
    def post_balance(self, dic):
        """
        以字典形式传参
        apiid:可在coinbene申请,
        secret:个人密钥(请勿透露给他人),
        timestamp:时间戳,
        account:默认为exchange，
        """
        url = trade_url + "balance"
        return self.http_post_sign(url, dic)


    #  下单
    def post_order_place(self, dic):
        """
        以字典形式传参
        apiid,symbol,timestamp
        type:可选 buy-limit/sell-limit
        price:购买单价
        quantity:购买数量
        """
        url = trade_url + "order/place"
        return self.http_post_sign(url, dic)


    #  查询委托
    def post_info(self, dic):
        """
        以字典形式传参
        apiid,timestamp,secret,orderid
        """
        url = trade_url + "order/info"
        return self.http_post_sign(url, dic)


    #  查询当前委托
    def post_open_orders(self, dic):
        """
        以字典形式传参
        apiid,timestamp,secret,symbol
        """
        url = trade_url + "order/open-orders"
        return self.http_post_sign(url, dic)


    #  撤单
    def post_cancel(self, dic):
        """
        以字典形式传参
        apiid,timestamp,secret,orderid
        """
        url = trade_url + "order/cancel"
        return self.http_post_sign(url, dic)
