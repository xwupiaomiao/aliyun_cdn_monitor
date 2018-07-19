#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import ConfigParser,os

class DescribeDomain(object):
    '''
    解析配置文件
    '''
    def __init__(self,Describe,Select=None):
        self._CONFIGFILE=os.path.join(os.path.dirname(os.path.abspath(__file__)), "aliyun.ini")
        self._config=ConfigParser.ConfigParser()
        self._config.read(self._CONFIGFILE)
        self._access_id = self._config.get('Credentials', 'accesskeyid')
        self._access_key = self._config.get('Credentials', 'accesskeysecret')
        self._Action = self._config.get(Describe, 'Action')
        self._DomainName = self._config.get(Describe, 'DomainName')
        self._Select=Select
        self._user_param={}

    @property
    def access_key_id(self):
        return self._access_id

    @property
    def access_key_secret(self):
        return self._access_key

    @property
    def user_params(self):
        if self._Action and self._DomainName:
            self._user_param['Action'] = self._Action
            self._user_param['DomainName'] = self._DomainName
            if not self._Select:
                return self._user_param
            else:
                Select_list=self._config.items(self._Select)
                for i in Select_list:
                    self._user_param[i[0]] = i[1]
                return self._user_param