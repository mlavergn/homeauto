#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

def LogConsole(arg):
  print("%s\n" % arg)

#===============================================================================

import subprocess

class Base:

  #-----------------------------------------------------------------------------

  def isAdmin(self):
    if 'SUDO_USER' in os.environ and os.geteuid() == 0:
      return True
    else:
      return False

  #-----------------------------------------------------------------------------

  def osxRunOSA(self, cmd):
    p = subprocess.Popen("""osascript -e 'do shell script "%s" with administrator privileges'""" % cmd, stdout= subprocess.PIPE, stdin= subprocess.PIPE, stderr= subprocess.STDOUT, shell=True)
    return p.communicate()[0]

  #-----------------------------------------------------------------------------

  def osxRun(self, cmd):
    p = subprocess.Popen(cmd, stdout= subprocess.PIPE, stdin= subprocess.PIPE, stderr= subprocess.STDOUT, shell=True)
    return p.communicate()[0]

  #-----------------------------------------------------------------------------

  def __init__(self, arg):
    if not self.isAdmin():
      print "This script must be run under sudo"
      return

    showCmd = 'plutil -p /System/Library/LaunchDaemons/com.apple.atrun.plist'
    setCmd = 'plutil -replace Disabled -bool false /System/Library/LaunchDaemons/com.apple.atrun.plist'

    try:
      data = self.osxRun(showCmd)
      if data.find('"Disabled" => 1') > 0:
        data = self.osxRun(setCmd)
        print data
        if data.find('"Disabled" => 0') > 0:
          print "atd enabled"
        else:
          print "atd disabled"
      else:
        print "atd is enabled"
    except:
      print sys.exc_info()[0]

#===============================================================================

if __name__ == "__main__":
  base = Base(0)

#===============================================================================
