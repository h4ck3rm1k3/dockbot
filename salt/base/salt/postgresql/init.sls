include:
  - python

postgresql-ppa:
  pkgrepo.managed:
    - humanname: Postgres PPA
    - name: deb http://apt.postgresql.org/pub/repos/apt/ {{ grains['oscodename'] }}-pgdg main
    - key_url: http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc

psycopg2:
  pip.installed:
    - require:
      - pkg: postgresql
      - cmd: pip-install

{% with postgres_version = salt['pillar.get']('pkgs:postgres:version', '9.3') %}
postgresql:
  pkg.installed:
    - names:
      - postgresql-{{ postgres_version }}
      - postgresql-server-dev-{{ postgres_version }}
    - require:
      - pkgrepo: postgresql-ppa
  service.running:
    - require:
      - pkg: postgresql
    - watch:
      - file: /etc/postgresql/{{ postgres_version }}/main/pg_hba.conf

/etc/postgresql/{{ postgres_version }}/main/pg_hba.conf:
  file.managed:
    - source: salt://postgresql/pg_hba.conf
    - template: jinja
    - require:
      - pkg: postgresql

/etc/postgresql/{{ postgres_version }}/main/postgresql.conf:
  file.managed:
    - source: salt://postgresql/postgresql.conf
    - template: jinja
    - context:
      postgres_version: {{ postgres_version }}
    - require:
      - pkg: postgresql
{% endwith %}
