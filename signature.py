#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

from hashlib import sha1
import base64,hmac,time,uuid,urllib

cdn_server_address = 'https://cdn.aliyuncs.com'

def percent_encode(str):
    res = urllib.quote(str.decode('UTF-8').encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])
    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def compose_url(Describe):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2014-11-11', \
            'AccessKeyId'   : Describe.access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
   }
    for key in Describe.user_params.keys():
        if  Describe.user_params[key]:
            parameters[key] = Describe.user_params[key]
    signature = compute_signature(parameters, Describe.access_key_secret)
    parameters['Signature'] = signature
    url = cdn_server_address + "/?" + urllib.urlencode(parameters)
    return url
