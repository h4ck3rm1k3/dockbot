#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys

from twisted.python import usage, reflect

from buildbot.scripts import runner


runner.StartOptions.subcommandFunction = 'dockbot.scripts.start.start'
runner.UpgradeMasterOptions.subcommandFunction = \
        'dockbot.scripts.upgrade_master.upgradeMaster'


def main():
    config = runner.Options()

    basedir = os.path.expanduser('~/.dockbot')
    if not os.path.exists(basedir):
        os.mkdir(basedir)

    try:
        config.parseOptions(sys.argv[1:])
    except usage.error, e:
        print "%s: %s" % (sys.argv[0], e)
        print
        c = getattr(config, 'subOptions', config)
        print str(c)
        sys.exit(1)

    subconfig = config.subOptions
    subcommandFunction = reflect.namedObject(subconfig.subcommandFunction)
    sys.exit(subcommandFunction(subconfig))


if __name__ == "__main__":
    main()
