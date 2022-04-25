#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   web.py    
@Description TODO
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/3/2 17:06:05   weizongtang      1.0         None
'''

# import lib
import logging

from flask import Flask, request

from util.ip2Region import Ip2Region

from util.IpAddress import IpAddress

app = Flask(__name__)
region = Ip2Region()
address = IpAddress()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/getAddressInfo', methods=['GET'])
def getAddressInfo():
    result = {}
    result['code'] = 200
    try:
        ip = request.args['ip']
        res = region.binarySearch(ip)
        logging.error('返回结果:%s' % res)
        result['address'] = res['region'].decode()
    except:
        result['code'] = 500
        logging.error('请求失败')
    return result


@app.route('/getIsChinaIP', methods=['GET'])
def getIsChinaIP():
    result = {}
    result['code'] = 200
    try:
        ip = request.args['ip']
        result['isChinaIP'] = address.isChinaIP(ip)
    except:
        result['code'] = 500
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
