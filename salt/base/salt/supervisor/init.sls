supervisor:
  pkg:
    - installed
  service:
    - running
    - require:
      - pkg: supervisor
    - watch:
      - file: /etc/supervisor/supervisord.conf

/etc/supervisor/supervisord.conf:
  file.managed:
    - source: salt://supervisor/supervisord.conf
    - user: root
    - group: root
    - mode: 0644
