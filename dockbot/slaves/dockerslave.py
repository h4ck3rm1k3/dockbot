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
# Portions Copyright Buildbot Team Members
import logging

from twisted.internet import defer, threads

from buildbot.buildslave import AbstractLatentBuildSlave
from buildbot import config, interfaces

logger = logging.getLogger('dockerslave')

try:
    from docker import client
    _hush_pyflakes = [client]
except ImportError:
    client = None


class DockerLatentBuildSlave(AbstractLatentBuildSlave):
    instance = None
    default_image = u'dockbot/buildslave'

    def __init__(self, name, password, docker_host, command, image=None,
                 max_builds=None, notify_on_missing=None,
                 missing_timeout=(60 * 20), build_wait_timeout=(60 * 10),
                 properties={}, locks=None, master_host=None,
                 master_port=9989, volumes=None):

        if not client:
            config.error("The python module 'docker-py' is needed "
                         "to use a DockerLatentBuildSlave")

        AbstractLatentBuildSlave.__init__(self, name, password, max_builds,
                                          notify_on_missing or [],
                                          missing_timeout, build_wait_timeout,
                                          properties, locks)

        self.docker_host = docker_host
        self.image = image or self.default_image
        self.command = command

        if not master_host:
            raise ValueError("You didn't specify the master's hostname")

        self.master_host = master_host
        self.master_port = master_port
        self.volumes = volumes or []

    def start_instance(self, build):
        if self.instance is not None:
            raise ValueError('instance active')
        return threads.deferToThread(self._start_instance)

    def _start_instance(self):
        docker_client = client.Client(base_url=self.docker_host)
        image = self.default_image

        volumes = {}
        binds = {}
        for volume_string in self.volumes:
            try:
                volume = volume_string.split(":")[1]
            except IndexError:
                logger.error("Invalid volume definition for docker "
                             "{0}. Skipping...".format(volume_string))
                continue
            volumes[volume] = {}

            volume, bind = volume_string.split(':', 1)
            binds[volume] = bind

        instance = docker_client.create_container(
            image,
            self.command,
            environment=[
                'CI=true',
                'BUILDBOT_USER={0}'.format(self.slavename),
                'BUILDBOT_PASSWORD={0}'.format(self.password),
                'BUILDBOT_HOST={0}'.format(self.master_host),
                'BUILDBOT_PORT={0}'.format(self.master_port),
            ],
            volumes=volumes,
        )
        if instance.get('Id', None):
            self.instance = instance
            docker_client.start(instance['Id'], binds=binds)
            return [instance['Id'], self.image]
        else:
            raise interfaces.LatentBuildSlaveFailedToSubstantiate(
                'Failed to start container'
            )

    def stop_instance(self, fast=False):
        if self.instance is None:
            # be gentle. Something may just be trying to alert us that an
            # instance never attached, and it's because, somehow, we never
            # started.
            return defer.succeed(None)
        instance = self.instance
        self.instance = None
        self._stop_instance(instance, fast)

    def _stop_instance(self, instance, fast):
        docker_client = client.Client(self.docker_host)
        docker_client.commit(
            container=instance['Id'],
            repository='dockbot/{0}'.format(self.slavename),
        )
        docker_client.stop(instance['Id'])
        docker_client.wait(instance['Id'])

    def buildFinished(self, sb):
        self.insubstantiate()
