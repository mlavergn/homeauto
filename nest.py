#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# https://github.com/wiredprairie/unofficial_nodejs_nest/blob/master/index.js
#

import sys
import os

from requests import session

def LogConsole(arg):
  print("%s" % arg)

#===============================================================================

import json

class Base:

  def login(self, username, password):

    print '======================================================================'
    
    #
    # login
    #
    payload = {
      'username': username,
      'password': password,
    }
    request = self.www.post('https://home.nest.com/user/login', data=payload)

    print request.status_code    
    data = request.json()
    print data 
    
    url = data['urls']['transport_url']
    print url
    
    atoken = data['access_token']
    print atoken
    
    userid = data['user']
    print userid
    
    serviceUrl = "%s/v2/mobile/%s" % (url, userid)
    print serviceUrl

    print '======================================================================'
    
    #
    # service info
    #
    headers = {
      'Authorization': 'Basic %s' % atoken,
      'X-nl-protocol-version': 1,
      'X-nl-user-id': userid,
      'User-Agent': 'Nest/3.0.1.15 (iOS) os=6.0 platform=iPad3,1',
    }    
    request = self.www.post('https://home.nest.com/user/service_urls', headers=headers)
    print request.status_code    
    data = request.json()
    print data 

    print '======================================================================'

    #
    # weather info
    #

    weatherUrl = 'http://www.wunderground.com/auto/nestlabs/geo/current/i?query=95030'
    request = self.www.get(weatherUrl, headers=headers)
    
    print request.status_code    
    data = request.json()
    print data 
    
    print '======================================================================'

    #
    # device info
    #
    request = self.www.get(serviceUrl, headers=headers)

    print request.status_code    
    data = request.json()
    print data 

    shared = data['shared']
    print shared

    devices = data['device']
    print devices

    print '======================================================================'
    
    for deviceID in devices:
      print shared[deviceID]['current_temperature']
      print shared[deviceID]['target_temperature']
      print devices[deviceID]['current_humidity']
      print devices[deviceID]['serial_number']
      print devices[deviceID]['battery_level'] # 3.6 == 0% / 3.9 == 100%

    print '======================================================================'

    #
    # device control
    #
    deviceSerial = devices[deviceID]['serial_number']
    deviceUrl = "%s/v2/put/shared.%s" % (url, deviceSerial)
    print deviceUrl

    payload = {
      'target_change_pending': 'true',
      'target_temperature': 16.11111,
    }
    
    headers = {
      'Authorization': 'Basic %s' % atoken,
      'X-nl-protocol-version': 1,
      'X-nl-user-id': userid,
      'X-nl-merge-payload': 'true',
      'User-Agent': 'Nest/3.0.1.15 (iOS) os=6.0 platform=iPad3,1',
    }    

    # request = self.www.post(deviceUrl, headers=headers)
    # print request.status_code    
    # data = request.json()
    # print data 

    print '======================================================================'

    #
    # logout
    # @TODO ... what's the URL here?
    #

    # print url
    # request = self.www.get(url, headers)
    # print request.status_code

  #-----------------------------------------------------------------------------

  def __init__(self, arg):
    try:
      self.www = session()
    except:
      print sys.exc_info()[0]

#===============================================================================

if __name__ == "__main__":
  configFile = "%s/config.json" % os.path.dirname(sys.argv[0])
  fd = open(os.path.expanduser(configFile), 'r')
  config = json.load(fd)

  base = Base(0)
  base.login(config['nest']['username'], config['nest']['password'])

#===============================================================================