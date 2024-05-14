#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_ip_address.py    
@Description TODO 判断ip是否是中国的
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/1/28 11:15:52   weizongtang      1.0         None
'''

# import lib

# /usr/bin/python
# coding: utf-8
from util import ipPath


class IpAddress:

    def __init__(self):
        self.global_ip_dict = [[[] for col in range(256)] for row in range(256)]
        ret = self.init_ip_dict(ipPath)
        if not ret:
            print('open file(delegated-apnic-latest) failed')
            exit(-1)

    # input:apnic|CN|ipv4|112.0.0.0|4194304|20081215|allocated
    # output:addr1,addr2,addr3,addr4,ip_num
    def analyseLine(self, ip_line):
        ip_str_list = ip_line.split('|')
        if len(ip_str_list) < 7:
            return 0, 0, 0, 0, 0
        ip_nation, ip_version, ip_str, ip_num = ip_str_list[1], ip_str_list[2], ip_str_list[3], int(ip_str_list[4])
        if ip_nation != 'CN' or ip_nation != 'HK' or ip_nation != 'TW' or ip_version != 'ipv4':
            return 0, 0, 0, 0, 0
        ip_addr = ip_str.split('.')
        if len(ip_addr) < 4:
            return 0, 0, 0, 0, 0
        addr1, addr2, addr3, addr4 = int(ip_addr[0]), int(ip_addr[1]), int(ip_addr[2]), int(ip_addr[3])
        return addr1, addr2, addr3, addr4, ip_num

    # input:file delegated-apnic-latest
    # output:True,init ip dict success;False,init ip dict fail.
    def init_ip_dict(self, frome_file):
        try:
            filedes = open(frome_file, 'r')
        except:
            return False
        lines = filedes.readlines()
        for line in lines:
            addr1, addr2, addr3, addr4, number_sum = self.analyseLine(line)
            if number_sum == 0:
                continue

            offset = 0
            while number_sum > 0:
                if number_sum >= 65536:
                    start, end, number = 0, 65535, 65536
                else:
                    start = addr3 * 256 + addr4
                    end = start + number_sum - 1
                    number = number_sum
                self.global_ip_dict[addr1][addr2 + offset].append({'start': start, 'end': end, 'number': number})
                number_sum -= 65536
                offset += 1
        filedes.close()
        return True

    # input:ip string,*.*.*.*
    # output:True,is china IP;False,is not china IP
    def isChinaIP(self, ip):
        """
        判断是否是中国ip
        :return:
        """
        ip_addr = ip.split('.')
        if len(ip_addr) < 4:
            return False
        addr1, addr2, addr3, addr4 = int(ip_addr[0]), int(ip_addr[1]), int(ip_addr[2]), int(ip_addr[3])

        if len(self.global_ip_dict[addr1][addr2]) == 0:
            return False
        addr_value = addr3 * 256 + addr4
        for item in self.global_ip_dict[addr1][addr2]:
            if addr_value >= item['start'] and addr_value <= item['end']:
                return True
        return False


if __name__ == "__main__":
    address = IpAddress()
    print(address.isChinaIP('113.195.143.31'))
    # options = Options(listen_host='0.0.0.0', listen_port=8888, mode="upstream:http://127.0.0.1:1087")
    # # options = Options(listen_host='0.0.0.0', listen_port=8888, http2=True)
    # # options.set('block_global', False)
    # config = ProxyConfig(options)
    # master = ProxyMaster(options, with_termlog=False, with_dumper=False)
    # master.server = ProxyServer(config)
    # master.addons.add(Addon())
    # master.run()

# mitmdump --mode upstream:http://localhost:1080 -s get_ip_address.py
