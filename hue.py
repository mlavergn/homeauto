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

import urllib

class Base:

  #-----------------------------------------------------------------------------

  def bridgeIP(self):
    sock = urllib.urlopen("https://www.meethue.com/api/nupnp")
    content = sock.read()
    sock.close()
    data = json.loads(content)
    return data[0]['internalipaddress']

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

  def hueRgbToXy(r, g, b):
      """ 
      Calculates the XY values (in the Hue's colourspace) from given RGB values.
      https://github.com/PhilipsHue/PhilipsHueSDKiOS/blob/master/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md
      Returns two floats; the X and Y values of the colour.
      """
      r = pow((r + 0.055) / (1.0 + 0.055), 2.4) if r > 0.04045 else r / 12.92
      g = pow((g + 0.055) / (1.0 + 0.055), 2.4) if g > 0.04045 else g / 12.92
      b = pow((b + 0.055) / (1.0 + 0.055), 2.4) if b > 0.04045 else b / 12.92
      X = r * 0.649926 + g * 0.103455 + b * 0.197109
      Y = r * 0.234327 + g * 0.743075 + b * 0.022598
      Z = r * 0.000000 + g * 0.053077 + b * 1.035763
      x = X / (X + Y + Z)
      y = Y / (X + Y + Z)
      # print "rgb returns x: %s and y: %s" % (x, y)
      return x, y

  #-----------------------------------------------------------------------------

  def lightHueRgb(self, red, green, blue):
    x, y = self.hueRgbToXy(red/255, green/255, blue/255)
    cmd = {'xy': (x, y)}
    bridge.set_light(bulb.light_id, cmd)

  #-----------------------------------------------------------------------------

  def lightHue(self, bridge, bulb, bri, sat, ct):
    cmd = {'bri': 254, 'sat': 128+64, 'ct': 400}
    bridge.set_light(bulb.light_id, cmd)

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
      # bridgeIP = Bridge().get_ip_address()
      bridgeIP = self.bridgeIP()
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
