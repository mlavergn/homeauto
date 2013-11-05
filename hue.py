#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

def LogConsole(arg):
  print("%s\n" % arg)

#===============================================================================

from phue import Bridge
import json
import ast

class Base:

  #-----------------------------------------------------------------------------

  def lightPower(self, bridge, bulb, on):
    state = True
    if on == False:
      state = False
    elif on == True:
      state = True
    elif on == 'False':
      state = False
    elif on == 'True':
      state = True
    elif on == "Off":
      state = False
    elif on == "On":
      state = True

    bridge.set_light(bulb.light_id, 'on', state)

  #-----------------------------------------------------------------------------

  def lightHue(self, bridge, bulb, bri, sat, ct):
    bridge.set_light(bulb.light_id, 'bri', 254)
    bridge.set_light(bulb.light_id, 'sat', 128+64)
    bridge.set_light(bulb.light_id, 'ct', 400) #154-500

  #-----------------------------------------------------------------------------

  def lightColorWarmWhite(self, bridge, bulb):
    self.lightHue(bridge, bulb, 254, 128+64, 400)

  #-----------------------------------------------------------------------------

  def allLights(self, state):
    for bulb in self.bulbs:
      base.lightPower(self.bridge, bulb, state)
      base.lightColorWarmWhite(self.bridge, bulb)

  #-----------------------------------------------------------------------------

  def __init__(self, arg):
    try:
      bridgeIP = Bridge().get_ip_address()
      self.bridge = Bridge(ip=bridgeIP, username=config['hue']['username'])
      self.bulbs = self.bridge.get_light_objects()
    except:
      print sys.exc_info()[0]

#===============================================================================

if __name__ == "__main__":
  configFile = "%s/config.json" % os.path.dirname(sys.argv[0])
  fd = open(os.path.expanduser(configFile), 'r')
  config = json.load(fd)

  argc = len(sys.argv)
  if (argc == 1):
    tgtstate = True
  else:
    tgtstate = sys.argv[1].strip().title()

  base = Base(0)
  base.allLights(tgtstate)

#===============================================================================
