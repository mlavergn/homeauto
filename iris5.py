#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import traceback

def LogConsole(arg):
  print("%s" % arg)

#===============================================================================
# easy_install requests

from requests import session
import json
import urllib
import uuid

class Iris:

  #-----------------------------------------------------------------------------

  #
  # login
  #
  def login(self, username, password):
    payload = {
      'username': username,
      'password': password,
      'caller': 'iPhone',
      'detail': 'tariff hub widgets',
      'version': '1.8.1',
    }

    payloadString = ""
    for key in payload:
      payloadString += "%s=%s&" % (key, urllib.quote(payload[key]))
    payloadString = payloadString[:len(payloadString)-1]
    print payloadString


    response = self.www.post('https://api.irissmarthome.com/v5/login', data=payloadString, headers=self.headers, proxies=self.proxies)

    print response

    # print response.status_code
    if response.status_code == 200:
      LogConsole("Login success")
      return 0
    else:
      LogConsole("Login fail")
      return 1

  #-----------------------------------------------------------------------------

  def irrigationState(self, username):
    self.headers['If-None-Match'] = str(uuid.uuid4()).replace('-','')

    response = None
    while True:
      response = self.www.get('https://api.irissmarthome.com/v5/users/%s/widgets/irrigation' % username, headers=self.headers, proxies=self.proxies)
      if response.status_code != 304:
        break

    print response
    data = response.json()

    # print data
    # print data['irrigation']['devices']

    for device in data['irrigation']['devices']:
      print device['id']
      print device['name']

    zone = data['irrigation']['active']
    print zone['id']
    print zone['name']
    print zone['state']

    # print response.status_code
    if response.status_code == 200:
      LogConsole("Irrigation success")
      return 0
    else:
      LogConsole("Irrigation fail")
      return 1

  #-----------------------------------------------------------------------------

  def dashboard(self, username):
    self.headers['If-None-Match'] = str(uuid.uuid4()).replace('-','')

    response = None
    while True:
      response = self.www.get('https://api.irissmarthome.com/v5/users/%s/widgets/dashboard?logSize=3' % username, headers=self.headers, proxies=self.proxies)
      if response.status_code != 304:
        break

    print response
    data = response.json()

    # print data

    devices = data['IRRIGATION']['irrigation']
    print devices

    for device in devices:
      print "%s:%s" % device['id'], device['state']

    if state == 'WATERING':
      return True
    elif state == 'IDLE':
      return False
    else:
      return False

    # print response.status_code
    if response.status_code == 200:
      LogConsole("Irrigation success")
      return 0
    else:
      LogConsole("Irrigation fail")
      return 1

  #-----------------------------------------------------------------------------

  def irrigationStart(self, username, macaddr, duration):
    self.headers.pop('If-None-Match', None)

    payload = {
      'duration': 1,
      'zoneId': 'AD-2E-00-00-0B-B6-AD-01'
    }

    response = self.www.put('https://api.irissmarthome.com/v5/users/%s/widgets/irrigation/%s/state' % (username, macaddr), headers=self.headers, data=payload, proxies=self.proxies)
    print response

    # print response.status_code
    if response.status_code == 204:
      LogConsole("Irrigation success")
      return 0
    else:
      LogConsole("Irrigation fail")
      return 1

  #-----------------------------------------------------------------------------

  def irrigationStop(self, username, macaddr):
    self.headers.pop('If-None-Match', None)

    response = self.www.put('https://api.irissmarthome.com/v5/users/%s/widgets/irrigation/%s/stop' % (username, macaddr), headers=self.headers, proxies=self.proxies)
    print response

    # print response.status_code
    if response.status_code == 204:
      LogConsole("Irrigation success")
      return 0
    else:
      LogConsole("Irrigation fail")
      return 1

  #-----------------------------------------------------------------------------

  def logout(self):
    None

  #-----------------------------------------------------------------------------

  def __init__(self, arg):
    try:
      self.www = session()
      self.proxies = {
        "http": "http://192.168.1.201:8888",
        "https": "http://192.168.1.201:8888",
      }
      self.headers = {
        "User-Agent": "Iris 1.8.1 rv:1173 (iPhone; iPhone OS 7.1; en_US)",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip",
        "Connection": "close",
        "Proxy-Connection": "close",
      }
    except:
      print sys.exc_info()[0]

#===============================================================================

if __name__ == "__main__":
  version = 1.0
  LogConsole("Iris Control v.%f" % version)

  configFile = "%s/config.json" % os.path.dirname(sys.argv[0])
  fd = open(os.path.expanduser(configFile), 'r')
  config = json.load(fd)

  argc = len(sys.argv)
  if (argc == 1):
    filter = 'Water'
    tgtstate = 'off'
  else:
    filter = sys.argv[1].lower().strip()
    tgtstate = sys.argv[2].lower().strip()

  iris = Iris(0)
  rc = iris.login(config['iris']['username'], config['iris']['password'])
  if rc:
    exit(1)

  macaddr = '00-00-00-00-00-00-00-00'
  if tgtstate == 'on':
    iris.irrigationState(config['iris']['username'])
    iris.irrigationStart(config['iris']['username'], macaddr, 1)
    iris.irrigationState(config['iris']['username'])
  else:
    iris.irrigationState(config['iris']['username'])
    iris.irrigationStop(config['iris']['username'], macaddr)
    iris.irrigationState(config['iris']['username'])
    
  if rc:
    exit(1)
  iris.logout()

#===============================================================================