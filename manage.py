#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import time
from influxdb import InfluxDBClient
from retres import make_request

def post(data):
    client = InfluxDBClient('10.47.39.8', 8086, database='aliyun')
    client.write_points(data, time_precision='m')
    client.close()

if __name__ == '__main__':
        post(make_request('DomainBps').DomainBps)
        post(make_request('DomainFlow').DomainFlow)
        post(make_request('DomainSrcBps').DomainSrcBps)
        post(make_request('DomainSrcFlow').DomainSrcFlow)
        post(make_request('DomainHitRate').DomainHitRate)
        post(make_request('HttpCode').HttpCode)
        post(make_request('TopUrlVisit').TopUrlVisit)
