import traceback

from buildbot.util import in_reactor
from twisted.internet import defer
from buildbot import monkeypatches
from buildbot import config as config_module
from buildbot.scripts.upgrade_master import upgradeDatabase


def loadConfig(config, configFileName):
    if not config['quiet']:
        print "checking %s" % configFileName

    try:
        master_cfg = config_module.MasterConfig.loadConfig(*configFileName.rsplit('/', 1))
    except config_module.ConfigErrors, e:
        print "Errors loading configuration:"
        for msg in e.errors:
            print " " + msg
        return
    except:
        print "Errors loading configuration:"
        traceback.print_exc(file=sys.stdout)
        return

    return master_cfg


@in_reactor
@defer.inlineCallbacks
def upgradeMaster(config, _noMonkey=False):
    if not _noMonkey: # pragma: no cover
        monkeypatches.patch_all()

    #if not checkBasedir(config):
    #    defer.returnValue(1)
    #    return

    os.chdir(config['basedir'])
    master_cfg = loadConfig(config, MASTER_CFG)
    print master_cfg
    if not master_cfg:
        defer.returnValue(1)
        return

    #upgradeFiles(config)
    yield upgradeDatabase(config, master_cfg)

    if not config['quiet']:
        print "upgrade complete"

    defer.returnValue(0)

