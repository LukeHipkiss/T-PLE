#!/usr/bin/python2.7

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Update Sheet</title>'
print '</head>'
print '<body>'

from subprocess import Popen
from os.path import expanduser as eu
from os import environ

import datetime
import sys


now = datetime.datetime.now()
basePath = eu("~/workspace/personal_scripts/")
myEnv = environ.copy()
myEnv["PATH"] = "/sv/venv/perscripts/bin/:" + myEnv["PATH"]


def main():
    with open(basePath + 'imaway/cgi-bin/lastUpdate', 'r') as lUpdate:
        if lUpdate.readline() == "{}, {}, {}".format(now.day, now.month, now.year):
            print '<h2>Please try updating tomorrow.</h2>'
            sys.exit()

    update = Popen(["/sv/venv/perscripts/bin/python2.7", basePath + "/scripts/updateELOFromLog.py"])
    update.wait()

    with open(basePath + 'imaway/cgi-bin/lastUpdate', 'w') as lUpdate:
        lUpdate.write("{}, {}, {}".format(now.day, now.month, now.year))

    print '<h2>Update Complete.</h2>'


if __name__ == '__main__':
    main()
    print '</body>'
    print '</html>'
