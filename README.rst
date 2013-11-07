=================================
dockbot - Docker-base buildbot CI
=================================

This is an experimental setup of a buildbot CI server, that is using a
Docker-based slave to run tests in isolation. It uses a basic Docker image
``dockbot/buildslave`` and uses a masterless Saltstack server to provision it
prior to running the test.

.. image:: https://d2weczhvl823v0.cloudfront.net/elbaschid/dockbot/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free
