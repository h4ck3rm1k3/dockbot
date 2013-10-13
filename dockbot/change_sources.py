from buildbot.changes.gitpoller import GitPoller


def get_change_sources(config):
    sources = []
    for project in config.projects:
        sources.append(
            GitPoller(
                project['repository'],
                project=project['name'],
                workdir='{}-workdir'.format(project['name']),
                branches=project.get('branches', ['master']),
                pollinterval=(5 * 60)
            )
        )
    return sources
