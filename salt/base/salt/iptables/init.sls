include:
  - base: iptables

extend:
  /etc/iptables.rules:
    file.managed:
      - user: root
      - group: root
      - mode: 640
      - source: salt://iptables/iptables.rules?env=termite
      - template: jinja
      - watch:
        - pkg: iptables
