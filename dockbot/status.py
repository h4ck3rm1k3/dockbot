import os
import jinja2

from buildbot.status import html
from buildbot.status.web import authz, auth
from buildbot.status.mail import MailNotifier


DOCKBOT_DIR = os.path.abspath(os.path.dirname(__file__))
print "DOCKBOT_DIR", DOCKBOT_DIR

myloaders = [
    jinja2.FileSystemLoader(os.path.join(DOCKBOT_DIR, 'master/templates')),
]


def get_auth(config):
    if 'htpasswd_file' in config.auth:
        return auth.HTPasswdAprAuth(config.auth['htpasswd_file'])
    else:
        users = config.auth.items()
        return auth.BasicAuth(users)


def get_statuses(config):
    authz_cfg = authz.Authz(
        auth=get_auth(config),
        gracefulShutdown=False,
        forceBuild='auth',
        forceAllBuilds=False,
        pingBuilder='auth',
        stopBuild=False,
        stopAllBuilds=False,
        cancelPendingBuild=False,
    )
    return [
        html.WebStatus(
            http_port=config.webstatus_port,
            authz=authz_cfg,
            change_hook_dialects={'github': True},
            jinja_loaders = myloaders,
            public_html=os.path.join(DOCKBOT_DIR, 'master/public_html')
        ),
        MailNotifier(
            fromaddr=config.from_address,
            extraRecipients=config.extra_recipients,
            mode=config.notifier_mode,
        )
    ]
