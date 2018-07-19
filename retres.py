#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import requests
from configfile import DescribeDomain
from signature import compose_url

class make_request(object):

    def __init__(self, option):
        self._option = option
        self._elk = []

    def _makereq(self):
        self.url = compose_url(DescribeDomain(self._option))
        self.res = requests.get(self.url)
        self.res = self.res.json()
        return self.res

    def _data(self,UrlList, data,strtime):
        for i in data:
            elk_dict = {}
            elk_dict['measurement'] = 'TopUrlVisit'
            elk_dict['time']=strtime
            elk_dict['tags'] = {'Code': UrlList,'UrlDetail':i['UrlDetail']}
            elk_dict['fields'] = {'Visit(%)': float(i['VisitProportion']),
                                  'VisitData':float(i['VisitData']),
                                  'Flow(%)': float(i['FlowProportion']),
                                  'Flow':float(i['Flow'])
                                  }
            self._elk.append(elk_dict)

    @property
    def DomainBps(self):
        res=self._makereq()
        res_list=res[ 'BpsDataPerInterval']['DataModule']
        for i in res_list:
            if i['Value'] !=0:
                elk_dic={}
                elk_dic['measurement']=self._option
                elk_dic['tags']={self._option:self._option}
                elk_dic['time']=i['TimeStamp']
                elk_dic['fields']={'value':i['Value']}
                self._elk.append(elk_dic)
        return self._elk

    @property
    def DomainFlow(self):
        res=self._makereq()
        res_list=res[ 'FlowDataPerInterval'][ 'DataModule']
        for i in res_list:
            if i['Value'] !=0:
                elk_dic = {}
                elk_dic['measurement'] = self._option
                elk_dic['tags'] = {self._option: self._option}
                elk_dic['time']=i['TimeStamp']
                elk_dic['fields']={'value':i['Value']}
                self._elk.append(elk_dic)
        return self._elk

    @property
    def DomainSrcBps(self):
        res=self._makereq()
        res_list=res['SrcBpsDataPerInterval']['DataModule']
        for i in res_list:
            if i['Value'] !=0:
                elk_dic = {}
                elk_dic['measurement'] = self._option
                elk_dic['tags'] = {self._option: self._option}
                elk_dic['time']=i['TimeStamp']
                elk_dic['fields']={'value':float(i['Value'])}
                self._elk.append(elk_dic)
        return self._elk

    @property
    def DomainSrcFlow(self):
        res=self._makereq()
        res_list=res['SrcFlowDataPerInterval'][ 'DataModule']
        for i in res_list:
            if i['Value'] !=0:
                elk_dic = {}
                elk_dic['measurement'] = self._option
                elk_dic['tags'] = {self._option: self._option}
                elk_dic['time']=i['TimeStamp']
                elk_dic['fields']={'value':i['Value']}
                self._elk.append(elk_dic)
        return self._elk

    @property
    def DomainHitRate(self):
        res=self._makereq()
        res_list=res['HitRateInterval']['DataModule']
        for i in res_list:
            if i['Value'] !=0:
                elk_dic = {}
                elk_dic['measurement'] = self._option
                elk_dic['tags'] = {self._option: self._option}
                elk_dic['time']=i['TimeStamp']
                elk_dic['fields']={'value':i['Value']}
                self._elk.append(elk_dic)
        return self._elk

    @property
    def HttpCode(self):
        res=self._makereq()
        res_list=res['HttpCodeData']['UsageData']
        for i in res_list:
            for Value in i['Value']['CodeProportionData']:
                elk_dic={}
                elk_dic['measurement']=self._option
                elk_dic['time'] = i['TimeStamp']
                elk_dic['tags']={'Code':Value['Code']}
                elk_dic['fields']={'Count':Value['Count'],'Proportion': Value['Proportion']}
                self._elk.append(elk_dic)
        return self._elk

    @property
    def TopUrlVisit(self):
        res = self._makereq()
        strtime = res['StartTime']
        res_list1 = res['Url200List']['UrlList']
        res_list2 = res['Url300List']['UrlList']
        res_list3 = res['Url400List']['UrlList']
        res_list4 = res['Url500List']['UrlList']
        self._data(UrlList='2XX',data=res_list1,strtime=strtime)
        self._data(UrlList='3XX', data=res_list2,strtime=strtime)
        self._data(UrlList='4XX', data=res_list3,strtime=strtime)
        self._data(UrlList='5XX', data=res_list4,strtime=strtime)
        return self._elk

if __name__ == '__main__':
    # res=make_request('TopUrlVisit').TopUrlVisit
    pass


