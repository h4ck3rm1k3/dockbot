#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from buildbot.scripts import runner


def main():
    print os.path.abspath(os.path.dirname(__file__))


if __name__ == "__main__":
    main()
