#!/usr/bin/python
#
# Grab some memory stats for Docker Containers on a host
# This is only tested on Ubuntu with Docker 1.7 and unlikely to 
# work on other distros without changing the memStat path
#
# @fintanr, June 3rd 2015
#

import os
import csv
from docker import Client

cli = Client(base_url='unix://var/run/docker.sock')
memStat = "/sys/fs/cgroup/memory/docker/%s/memory.stat"
cStats = {}

for container in cli.containers():

    mstat = memStat % container["Id"]

    reader = csv.reader(open(mstat, mode='r'), delimiter=' ')
    ourContainerStats = dict(reader)

    ourRssMbs = '%.2fMb' % ( float(ourContainerStats['rss']) / 1048576 )
    ourCacheMbs = '%.2fMb' % ( float(ourContainerStats['cache']) / 1048576 )

    cStats[container['Id']] = {}
    cStats[container['Id']]['RSS_MB'] = ourRssMbs
    cStats[container['Id']]['Cache_MB'] = ourCacheMbs
    cStats[container['Id']]['Image'] = container['Image']


print("RSS\tCache\tImage Name\n");

for key,value in cStats.items():
    print ( "%s\t%s\t%s " ) % ( cStats[key]['RSS_MB'], cStats[key]['Cache_MB'], cStats[key]['Image'] )
