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

class Iris:

  #-----------------------------------------------------------------------------

  #
  # login
  #
  def login(self, username, password):
    payload = {
      'username': username,
      'password': password,
      'rememberMyUsername': 0,
    }
    request = self.www.post('https://www.irissmarthome.com/myhome/index/login/format/json/', data=payload)

    # camelcase the username for some reason    
    self.username = username[0].upper() + username[1:]
    
    # print request.status_code
    if request.status_code == 200:
      LogConsole("Login complete")
      return 0
    else:
      LogConsole("Failed to login")
      return 1

  #-----------------------------------------------------------------------------

  #
  # state
  #
  def state(self):
    payload = {
      'Controls': '#/controls/widget/format/json',
      'Magic': '#/rules/magic/reload/true/category/CONTROLS/format/json'
    }
    request = self.www.post('https://www.irissmarthome.com/myhome/index/ajax', data=payload)

    # print request.status_code
    if request.status_code == 200:
      LogConsole("Queried devices")
    else:
      LogConsole("Failed to query devices")
      return None

    # print request.headers
    # print request.text
    data = request.json()
    # print data 
    plugs = data['Controls']['data']['summary']['smartplugs']
    # print plugs

    for plug in plugs:
      LogConsole("%s [%s] %s" % (plug['name'], plug['id'], plug['onOffState']))
      
    return plugs

  #-----------------------------------------------------------------------------

  #
  # control
  #
  def control(self, plug, state):
    payload = {
      'onOffState': state,
    }

    url = 'https://www.irissmarthome.com/v5/users/%s/widgets/SmartPlugs/%s/onOffState' % (self.username, plug['id'])
    print "Setting %s to %s via [%s]" % (plug['name'], state, url)
    request = self.www.put(url, data=payload)
    
    print request.status_code
    if request.status_code == 204:
      LogConsole("204 == SUCCESS")
      return 0
    elif request.status_code == 405:
      LogConsole("Set %s to %s" % (plug['name'], state))
      return 0
    else:
      LogConsole("Failed to control device")
      return 1

  #-----------------------------------------------------------------------------

  #
  # logout
  #
  def logout(self):
    request = self.www.post('https://www.irissmarthome.com/myhome/logout')
    
    # print request.status_code
    if request.status_code == 200:
      LogConsole("Logout complete")
      return 0
    else:
      LogConsole("Logout failed")
      return 1

  #-----------------------------------------------------------------------------
  
  #
  # scene
  #
  def scene(self, plugs, filter, state):
    LogConsole("filter:[%s] state:[%s]" % (filter, state))
    for plug in plugs:
      print plug['name']
      if plug['name'].lower().find(filter) == 0:
        print plug['name']
        rc = iris.control(plug, state)
    
  #-----------------------------------------------------------------------------

  def __init__(self, arg):
    try:
      self.www = session()
    except:
      print sys.exc_info()[0]

#===============================================================================

if __name__ == "__main__":
  version = 2.0
  LogConsole("Iris Control v.%f" % version)

  configFile = "%s/config.json" % os.path.dirname(sys.argv[0])
  fd = open(os.path.expanduser(configFile), 'r')
  config = json.load(fd)

  argc = len(sys.argv)
  if (argc == 1):
    filter = 'Lights'
    tgtstate = 'on'
  else:
    filter = sys.argv[1].lower().strip()
    tgtstate = sys.argv[2].lower().strip()

  iris = Iris(0)
  rc = iris.login(config['iris']['username'], config['iris']['password'])
  if rc:
    exit(1)
  plugs = iris.state()
  if plugs is None:
    exit(1)

  # rc = iris.control(plugs[1], tgtstate)
  rc = iris.scene(plugs, filter, tgtstate)
  if rc:
    exit(1)
  iris.logout()

#===============================================================================