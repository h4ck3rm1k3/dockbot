from buildbot.buildslave import BuildSlave
from dockerslave import DockerLatentBuildSlave


def get_slaves(config):
    docker_host = 'unix://var/run/docker.sock'  # http://127.0.0.1:4243
    slaves = [
        BuildSlave("static-slave", "rockstatic"),
        DockerLatentBuildSlave(
            name='docker-slave',
            password='likeawhale',
            docker_host=docker_host,
            #image='elbaschid/buildslave',
            command="buildslave --verbose start --nodaemon /root/slave",
            #master_host='termite.tangentsnowball.com.au',
            master_host='172.17.42.1',
            #volumes=['/home/dockbot/.ssh:/root/.ssh:ro'],
            build_wait_timeout=0,
        )
    ]
    for project in config.projects:
        project_name = project.get('name')
        if not project_name:
            continue
        slaves.append(
            DockerLatentBuildSlave(
                name='docker-{0}'.format(project_name),
                password='likeawhale',
                docker_host=docker_host,
                #image='elbaschid/{0}'.format(project_name),
                command="buildslave --verbose start --nodaemon /root/slave",
                master_host='172.17.42.1',
                #volumes=[
                #    '/home/woody/.ssh:/root/.ssh:ro',
                #    '/home/woody/wheelhouse:/root/wheelhouse:rw',
                #],
                build_wait_timeout=0,
            )
        )
    return slaves
