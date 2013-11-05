#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import traceback

def LogConsole(arg):
  print("%s\n" % arg)

#===============================================================================
# easy_install requests

from requests import session

import smtplib
from email.mime.text import MIMEText
import time
import datetime
import pytz
import json

#
# Enable at under OS X
# sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.atrun.plist
#

class Base:

  #-----------------------------------------------------------------------------
  #
  # weather info
  #
  def forecast(self, zipcode):
    weatherUrl = 'http://www.wunderground.com/auto/nestlabs/geo/current/i?query=%i' % zipcode
    request = self.www.get(weatherUrl, headers={})
    # print request.status_code    
    data = request.json()
    #print data 
    return data

  #-----------------------------------------------------------------------------

  def localtime(self, epoch):
    # could use tzlocal.get_localzone() insteaf of self.timezone
    tz = pytz.timezone(self.timezone)
    dst = time.localtime().tm_isdst
    offset = tz.utcoffset(datetime.datetime.utcnow(), is_dst = dst).total_seconds()
    localtime = time.gmtime(epoch + offset)
    # print localtime
    return localtime

  #-----------------------------------------------------------------------------

  def attime(self, timeval):
    if (timeval.tm_hour) > 12:
      attimestring = "%i:%02ipm" % (timeval.tm_hour - 12, timeval.tm_min)
    else:
      attimestring = "%i:%02iam" % (timeval.tm_hour, timeval.tm_min)
    return attimestring

  #-----------------------------------------------------------------------------

  def sunset(self, data):
    sunset = data[str(zipcode)]['current']['sunset']
    sunsetlocal = base.localtime(sunset)
    sunsetstring = base.attime(sunsetlocal)
    return sunsetstring

  #-----------------------------------------------------------------------------

  def temps(self, data):
    temps = data[str(zipcode)]['forecast']['hourly']
    return temps

  #-----------------------------------------------------------------------------

  def heatup(self, data, limit):
    temps = base.temps(data)
    onOff = {}
    for temp in temps:
      if temp['temp_f'] >= limit and onOff.has_key('on') == False:
        timelocal = base.localtime(temp['time'])
        onOff['on'] = base.attime(timelocal)
      elif temp['temp_f'] <= limit and onOff.has_key('on'):
        timelocal = base.localtime(temp['time'])
        onOff['off'] = base.attime(timelocal)
        break

    return onOff

  #-----------------------------------------------------------------------------

  def scheduleIris(self, filter, state, attime, atday):
    irisFile = os.path.abspath("%s/iris.py" % os.path.dirname(sys.argv[0]))
    cmd = 'echo "python %s %s %s" | at %s %s' % (irisFile, filter, state, attime, atday)
    # print cmd
    os.system(cmd)
    return cmd

  #-----------------------------------------------------------------------------

  def scheduleHue(self, filter, state, attime, atday):
    irisFile = os.path.abspath("%s/iris.py" % os.path.dirname(sys.argv[0]))
    cmd = 'echo "python %s %s" | at %s %s' % (irisFile, state, attime, atday)
    # print cmd
    os.system(cmd)
    return cmd

  #-----------------------------------------------------------------------------

  def sendmail(self, config, message):
    msg = MIMEText(message)
    msg['Subject'] = "Home Automation Schedule"
    msg['From'] = config['smtp']['email']
    msg['To'] = config['smtp']['email']

    server = smtplib.SMTP()
    server.connect(config['smtp']['server'], config['smtp']['port'])
    server.starttls()
    server.login(config['smtp']['username'], config['smtp']['password'])
    server.sendmail(config['smtp']['email'], [config['smtp']['email']], msg.as_string())
    server.quit()

  #-----------------------------------------------------------------------------

  def __init__(self, arg):
    try:
      self.www = session()
      self.timezone = arg
    except:
      print sys.exc_info()[0]

#===============================================================================

if __name__ == "__main__":
  version = 2.0
  LogConsole("Home Automation Control v.%f" % version)

  configFile = os.path.abspath("%s/config.json" % os.path.dirname(sys.argv[0]))
  fd = open(configFile, 'r')
  config = json.load(fd)

  message = ""

  base = Base('US/Pacific')
  zipcode = config['nest']['zipcode']
  try:
    data = base.forecast(zipcode)
    lightstring = base.sunset(data)
    message += base.scheduleIris('Lights', 'on', lightstring, 'today') + "\n"
    message += base.scheduleIris('Lights', 'off', '1:00am', 'tomorrow') + "\n"
    message += base.scheduleHue('Lights', 'on', lightstring, 'today') + "\n"
    message += base.scheduleHue('Lights', 'off', '1:00am', 'tomorrow') + "\n"

    poolstring = base.heatup(data, 66)
    if poolstring.has_key('on'):
      message += base.scheduleIris('Pool', 'on', poolstring['on'], 'today') + "\n"
      message += base.scheduleIris('Pool', 'off', poolstring['off'], 'today') + "\n"
    else:
      message += base.scheduleIris('Pool', 'on', '1:00pm', 'today') + "\n"
      message += base.scheduleIris('Pool', 'off', '2:00pm', 'today') + "\n"
  except:
    LogConsole("Fallback behavior")
    message += base.scheduleIris('Lights', 'on', '6:00pm', 'today') + "\n"
    message += base.scheduleIris('Lights', 'off', '1:00am', 'tomorrow') + "\n"
    message += base.scheduleHue('Lights', 'on', '6:00pm', 'today') + "\n"
    message += base.scheduleHue('Lights', 'off', '1:00am', 'tomorrow') + "\n"
    message += base.scheduleIris('Pool', 'on', '1:00pm', 'today') + "\n"
    message += base.scheduleIris('Pool', 'off', '4:00pm', 'today') + "\n"
    traceback.print_exc()

  base.sendmail(config, message)

#===============================================================================
