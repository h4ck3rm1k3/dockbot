en_US.UTF-8:
  locale.system

core-pkgs:
  pkg.installed:
    - names:
      - vim
      - git
      - mercurial
      - apt-transport-https
    - require:
      - locale: en_US.UTF-8

salt-minion:
  pkg.latest
