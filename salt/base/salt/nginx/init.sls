include:
  - base: nginx

/etc/nginx/sites-available/buildbot-master.conf:
  file.managed:
    - source: salt://nginx/buildbot-master.conf
    - require:
      - pkg: nginx

/etc/nginx/sites-enabled/buildbot-master.conf:
  file.symlink:
    - target: /etc/nginx/sites-available/buildbot-master.conf
    - require:
      - file: /etc/nginx/sites-available/buildbot-master.conf
    - require_in:
      - service: nginx

/var/www/termite.htpasswd:
  file.managed:
    - source: salt://nginx/termite.htpasswd.jinja
    - user: www-data
    - group: www-data
    - template: jinja
    - require_in:
      - service: nginx
