include:
  - core
  - python

docker-py:
  pip.installed:
    - require:
      - cmd: pip-install

docker:
  group.present

docker-ppa:
  pkgrepo.managed:
    - humanname: Docker PPA
    - name: deb https://get.docker.io/ubuntu docker main
    - key_url: http://get.docker.io/gpg
    - require:
      - pkg: core-pkgs

lxc-docker:
  pkg.installed:
    - require:
      - pkgrepo: docker-ppa

pull-docker-images:
  cmd.run:
    - name: docker pull dockbot/buildslave
    - require:
      - pkg: lxc-docker
      - pip: docker-py
