# This file is part of Buildbot. Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members
import os
import sys

from twisted.internet import reactor, protocol
from twisted.python.runtime import platformType

from buildbot.scripts.start import Follower

TWISTED_LOG = os.path.expanduser('~/.dockbot/twisted.log')
BUILDBOT_TAC = os.path.join(os.path.dirname(__file__),
                            '../master/buildbot.tac')
MASTER_CFG = os.path.join(os.path.dirname(__file__),
                            '../master/master.cfg')


def launchNoDaemon(config):
    os.chdir(config['basedir'])
    sys.path.insert(0, os.path.abspath(config['basedir']))

    argv = [
        "twistd",
        "--no_save",
        '--nodaemon',
        "--logfile={0}".format(TWISTED_LOG),
        "--python={0}".format(BUILDBOT_TAC),
    ]
    sys.argv = argv

    # this is copied from bin/twistd. twisted-2.0.0 through 2.4.0 use
    # _twistw.run . Twisted-2.5.0 and later use twistd.run, even for
    # windows.
    from twisted.scripts import twistd
    twistd.run()


def launch(config):
    os.chdir(config['basedir'])
    sys.path.insert(0, os.path.abspath(config['basedir']))

    # see if we can launch the application without actually having to
    # spawn twistd, since spawning processes correctly is a real hassle
    # on windows.
    argv = [
        sys.executable,
        "-c",
        # this is copied from bin/twistd. twisted-2.0.0 through 2.4.0 use
        # _twistw.run . Twisted-2.5.0 and later use twistd.run, even for
        # windows.
        "from twisted.scripts import twistd; twistd.run()",
        "--no_save",
        "--logfile={0}".format(TWISTED_LOG),
        "--python={0}".format(BUILDBOT_TAC),
    ]

    # ProcessProtocol just ignores all output
    reactor.spawnProcess(
        protocol.ProcessProtocol(),
        sys.executable,
        argv,
        env=os.environ
    )


def start(config):
    if config['nodaemon']:
        launchNoDaemon(config)
        return 0

    launch(config)

    # We don't have tail on windows
    if platformType == "win32" or config['quiet']:
        return 0

    # this is the parent
    rc = Follower().follow(config['basedir'])
    return rc
