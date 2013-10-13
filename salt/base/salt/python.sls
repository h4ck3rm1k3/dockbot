python-apt:
  pkg.installed

python-software-properties:
  pkg.installed

python-setuptools:
  pkg.installed

pip-install:
  cmd.run:
    - name: easy_install pip
    - require:
      - pkg: python-setuptools

virtualenv:
  pip.installed:
    - require:
      - cmd: pip-install
