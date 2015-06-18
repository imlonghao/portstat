#!/usr/bin/env python

from portstat import portstat
from os import path

here = path.abspath(path.dirname(__file__))
confPath = path.join(here, 'portstat.conf')

version = portstat.version()
portGroups = portstat.getConfig(confPath)
portstat.sync(portGroups)
portstat.upload(portGroups)

portstat.main()