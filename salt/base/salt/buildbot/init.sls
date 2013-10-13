include:
  - postgresql
  - python
  - docker
  - supervisor

buildbot-deps:
  pkg.installed:
    - names:
      - gcc
      - build-essential
      - python-dev
      # required for SHA1 hashes used in authentication
      - libaprutil1

/home/{{ pillar['build_user'] }}/master:
  file.symlink:
    - target: /vagrant/master

buildbot upgrade-master /home/{{ pillar['build_user'] }}/master:
  cmd.run:
    - env:
      - BUILDBOT_DB_USER: {{ salt['pillar.get']('buildbot:postgres:user') }}
      - BUILDBOT_DB_NAME: {{ salt['pillar.get']('buildbot:postgres:database') }}
      - BUILDBOT_DB_PASSWORD: {{ salt['pillar.get']('buildbot:postgres:password') }}
    - require:
      - file: /home/{{ pillar['build_user'] }}/master

buildbot:
  pip.installed:
    - user: {{ pillar['build_user'] }}
    - require:
      - pkg: buildbot-deps
      - cmd: pip-install
      - user: {{ pillar['build_user'] }}

{{ pillar['build_user'] }}:
  user.present:
    - fullname: Build Whale
    - shell: /bin/bash
    - home: /home/{{ pillar['build_user'] }}
    - groups:
      - adm
      - sudo
      - docker
      - admin
    - require:
      - group: docker
  postgres_user.present:
    - password: {{ salt['pillar.get']('buildbot:postgres:password') }}
    - require:
      - user: {{ pillar['build_user'] }}
      - service: postgresql

dockbot:
  cmd.run:
    - name: pip install -e /vagrant
    - require:
      - cmd: pip-install

/home/{{ pillar['build_user'] }}/.ssh:
  file.directory:
    - user: {{ pillar['build_user'] }}
    - group: {{ pillar['build_user'] }}
    - require:
      - user: {{ pillar['build_user'] }}

/var/www/dockbot.htpasswd:
  file:
    - managed
    - append:
      - text:
        {% for user,pwdhash in pillar.get('dockbot_users', {}).iteritems() %}
        - {{ user}}:{{ pwdhash }}
        {% endfor %}

#####################
# PostgreSQL database
#####################
{{ salt['pillar.get']('buildbot:postgres:database') }}:
  postgres_database.present:
    - owner: {{ pillar['build_user'] }}
    - encoding: UTF8
    - template: template1
    - require:
      - postgres_user: {{ pillar['build_user'] }}

#####################
# Supervisor config
#####################
/etc/supervisor/conf.d/buildbot-master.conf:
  file.managed:
    - source: salt://buildbot/buildbot-master.conf.jinja
    - template: jinja
    - context:
      master_dir: /home/{{ pillar['build_user'] }}/master
      buildbot_user: {{ pillar['build_user'] }}
    - require:
      - pkg: supervisor

buildbot-master:
  supervisord.running:
    - update: True
    - require:
      - pkg: supervisor
      - service: supervisor
      - file: /etc/supervisor/conf.d/buildbot-master.conf
      - file: /var/www/dockbot.htpasswd
    - watch:
      - file: /etc/supervisor/conf.d/buildbot-master.conf
