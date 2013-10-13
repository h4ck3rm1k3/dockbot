from buildbot.schedulers.trysched import Try_Userpass
from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler

from .builders import get_builder_names


def get_schedulers(config):
    builder_names = get_builder_names(config)
    schedulers = []

    for builder_name in builder_names:
        if builder_name.startswith("TRY"):
            schedulers += [
                Try_Userpass(
                    name='{}'.format(builder_name),
                    builderNames=[builder_name],
                    port=8031,
                    userpass=config.auth.items(),
                ),
            ]
        else:
            schedulers += [
                AnyBranchScheduler(
                    name="all",
                    treeStableTimer=None,
                    builderNames=[builder_name]
                ),
                ForceScheduler(
                    name="force",
                    builderNames=[builder_name]
                )
            ]
    return schedulers
