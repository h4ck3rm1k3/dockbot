from collections import defaultdict

from buildbot.config import BuilderConfig
from buildbot.steps.source.git import Git
from buildbot.steps.master import SetProperty
from buildbot.steps.shell import ShellCommand
from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Interpolate


_builders = {}
_project_builders = defaultdict(list)


def _store_builder(project_name, builder_config):
    _builders[builder_config.name] = builder_config
    _project_builders[project_name].append(builder_config)


def get_before_install_steps(project):
    return [
        ShellCommand(
            command=["virtualenv", "venv"],
            haltOnFailure=True
        ),
        SetProperty(
            property="venv_dir",
            value=Interpolate("%(prop:workdir)s/build/venv")
        ),
        ShellCommand(
            command=["pip", "install", "-U", "pip", "setuptools", "wheel"],
            env={
                'PATH': [Interpolate('%(prop:venv_dir)s/bin'), '${PATH}'],
                'VIRTUAL_ENV': Interpolate('%(prop:venv_dir)s'),
            },
            haltOnFailure=True,
        )
    ]


def get_provision_steps(project):
    return [
        ShellCommand(
            workdir='build/www',
            command=["make", "salt-ci"],
            haltOnFailure=True,
        )
    ]


def get_script_steps(project):
    return [
        ShellCommand(
            workdir='build/www',
            command=["make", "ci"],
            env={
                'PATH': ['${PWD}/venv/bin', '${PATH}'],
                'VIRTUAL_ENV': '${PWD}/venv',
            }
        )
    ]


def _load_builders(projects):
    global _builders

    for project in projects:
        print 'PROJECT', project
        steps = [
            Git(
                repourl=project.get('repository'),
                mode='incremental'
            )
        ]

        factory = BuildFactory()
        steps += get_before_install_steps(project)
        steps += get_provision_steps(project)
        steps += get_script_steps(project)

        factory.addSteps(steps)

        name = "{}".format(project['name'])
        print "PROJECT NAME", name
        _store_builder(
            project_name=name,
            builder_config=BuilderConfig(
                name=name,
                slavenames=['docker-{0}'.format(name)],
                factory=factory
            )
        )
        _store_builder(
            project_name=name,
            builder_config=BuilderConfig(
                name="TRY-{0}".format(name),
                slavenames=['docker-{0}'.format(name)],
                factory=factory
            )
        )


def get_builders(config):
    if not _builders:
        _load_builders(config.projects)
    print [b.name for b in _builders.values()]
    return _builders.values()


def get_builder_names(config):
    if not _builders:
        _load_builders(config.projects)
    return _builders.keys()
