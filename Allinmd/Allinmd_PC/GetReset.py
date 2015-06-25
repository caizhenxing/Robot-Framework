#!/usr/bin/env python
#-*- coding:utf8 -*-

__version__ = '0.1'

from robot.api import logger
import urllib2, json, re, os
from xml.etree import ElementTree

class GetReset():
    def __init__(self):
        self.dom = ElementTree.parse(os.getcwd()+"\\data\\reset_passwd_info.xml")
        if int(self.dom.find("mode").text) == 1:
            self.get_phone()
        else:
            self.get_url()
            
    def get_url(self):
        html = self.dom.find("emailurl").text\
            + "?order=asc&page=1"\
            + "&queryJson={'email'%3A'"\
            + self.dom.find("email").text\
            + "'}" + "&rows=1&sort=id"
    
        req = urllib2.Request(html)
        content = urllib2.urlopen(req).read()
        data = json.loads(content)
        reg = re.compile("(http://)(www.|m.)(.*).cn/[a-n]{4,5}/customer/reset/password/input/\\?itemId=[0-9]{4}&resetSite=[0-9]&validCode=[0-9a-z]{32}")
        str = reg.findall(data['rows'][0]['sendContent'])
        url = (str[0][0]+str[0][1]+str[0][2]).split('"')[0]
        print url
    
    def get_phone(self):
        html = self.dom.find("phoneurl").text\
            + "?order=asc&page=1"\
            + "&queryJson={'cellPhone'%3A'"\
            + self.dom.find("phone").text\
            + "'}" + "&rows=1&sort=id"
            
        req = urllib2.Request(html)
        content = urllib2.urlopen(req).read()
        data = json.loads(content)
        code = data['rows'][0]['smsContent'][8:14]
        print code
        
if __name__ == "__main__":
    get = GetReset()
