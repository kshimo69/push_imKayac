#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import urllib2, urllib
import xml.etree.ElementTree
import re

class IMKayac(object):
    """ push im.kayac
    """

    def __init__(self, id, password=None, sig=None):
        self.id = id
        self.password = password
        self.sig = sig

    def notify(self, msg):
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
            path = 'http://im.kayac.com/api/post/%s' % self.id
            params = {
                'message':msg,
                }
            if self.password:
                params['password'] = self.password
            if self.sig:
                params['sig'] = hashlib.sha1(msg + self.sig).hexdigest()

            urllib2.build_opener().open(path, urllib.urlencode(params))

class GetWeather(object):
    """ get current weather from livedoor api
    """

    def __init__(self, location):
        self.params = urllib.urlencode({'city':location, 'day':'today'})

    def get(self):
        dom = xml.etree.ElementTree.fromstring(urllib.urlopen(
                'http://weather.livedoor.com/forecast/webservice/rest/v1?%s'
                % self.params
                ).read())
        if re.match(r'.*雨.*', dom.findtext('.//telop').encode('utf-8')):
            return dom.findtext('.//title') + ' ' + dom.findtext('.//telop')
        else:
            return None

if __name__ == '__main__':
    weather = GetWeather(70) # 70 means Yokohama, Kanagawa
    weatherStr = weather.get()
    if weatherStr:
        im = IMKayac('ID', 'PASSWORD', 'SIG')
        message = u"傘いるかも: " + weatherStr
        im.notify(message)
