# -*- python -*-
# ex: set syntax=python:
import os
import sys

from twisted.application import service
from twisted.python.logfile import LogFile
from twisted.python.log import ILogObserver, FileLogObserver

#from buildbot.master import BuildMaster
from dockbot.master import DockbotMaster

basedir = os.path.expanduser('~/.dockbot/')

rotateLength = '10000000'
maxRotatedFiles = '10'

# note: this line is matched against to check that this is a buildmaster
# directory; do not edit it.
application = service.Application('buildmaster')

logfile = LogFile.fromFullPath(
    os.path.join(basedir, "twistd.log"),
    rotateLength=rotateLength,
    maxRotatedFiles=maxRotatedFiles
)

application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

m = DockbotMaster(
    basedir=basedir,
    configFileName=os.path.join(
        os.path.dirname(__file__),
        'master.cfg'
    )
)
m.setServiceParent(application)
m.log_rotation.rotateLength = rotateLength
m.log_rotation.maxRotatedFiles = maxRotatedFiles
