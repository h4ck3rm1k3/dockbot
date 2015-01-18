import logging

logger = logging.getLogger(__name__)


try:
    from docker import client
    HAS_DOCKER_CLIENT = True
except ImportError:
    HAS_DOCKER_CLIENT = False

__virtualname__ = "docker"

def __virtual__():
    if not HAS_DOCKER_CLIENT:
        logger.error("Docker client 'docker-py' not available")
        return False
    else:
        return __virtualname__


def _get_docker_client():
    kwargs = {}
    base_url = __salt__['pillar.get']('docker:base_url')
    version = __salt__['pillar.get']('docker:api_version')
    if base_url:
        kwargs['base_url'] = base_url
    if version:
        kwargs['version'] = version
    return client.Client(**kwargs)


def version():
    return _get_docker_client().version()


def images():
    return _get_docker_client().images()


def pull(name, tag=None):
    kwargs = {}
    if tag:
        kwargs['tag'] = tag
    return _get_docker_client().pull(name, **kwargs)
