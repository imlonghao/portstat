#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

__author__ = 'imlonghao'
__version__ = '0.0.3'


def version():
    return __version__.split(',')


def getConfig(path):
    settings = configparser.ConfigParser()
    settings.read(path)
    portGroups = []
    for each in settings.sections():
        portGroups.append(
            [each, settings.get(each, 'Port'), settings.get(each, 'Webhook')])
    return portGroups


def sync(portGroups):
    with open('/etc/portstat.rules', 'w') as portstat_rules:
        portstat_rules.write('#!/bin/bash\n')
        portstat_rules.write('/sbin/iptables -F PORTSTAT\n')
        for each in portGroups:
            if '-' in each[1]:
                begin = int(each[1].split('-')[0])
                end = int(each[1].split('-')[1]) + 1
                for i in range(begin, end):
                    portstat_rules.write(
                        '/sbin/iptables -A PORTSTAT -p tcp --dport %s\n' % str(i))
                    portstat_rules.write(
                        '/sbin/iptables -A PORTSTAT -p tcp --sport %s\n' % str(i))
            elif ',' in each[1]:
                portLists = each[1].split(',')
                while '' in portLists:
                    portLists.remove('')
                for i in portLists:
                    portstat_rules.write(
                        '/sbin/iptables -A PORTSTAT -p tcp --dport %s\n' % i)
                    portstat_rules.write(
                        '/sbin/iptables -A PORTSTAT -p tcp --sport %s\n' % i)
            else:
                portstat_rules.write(
                    '/sbin/iptables -A PORTSTAT -p tcp --dport %s\n' % each[1])
                portstat_rules.write(
                    '/sbin/iptables -A PORTSTAT -p tcp --sport %s\n' % each[1])
    os.system('/bin/bash /etc/portstat.rules')


def upload(portGroups):
    # stats = {9999: 11111}, {10000: 11112}
    stats = {}
    for each in os.popen('/sbin/iptables -vxn -L PORTSTAT').readlines()[2:]:
        port = int(each.strip().split()[9][4:])
        value = int(each.strip().split()[1])
        if port in stats:
            stats[port] += value
        else:
            stats[port] = value
    # datas = [{'1.php': {9999: 11111}}, {'2.php': {10000: 122222, 10001: 1212414}}]
    datas = []
    for each in portGroups:
        line = {}
        if '-' in each[1]:
            begin = int(each[1].split('-')[0])
            end = int(each[1].split('-')[1]) + 1
            for i in range(begin, end):
                line[i] = stats[i]
        elif ',' in each[1]:
            portLists = each[1].split(',')
            while '' in portLists:
                portLists.remove('')
            for i in portLists:
                line[int(i)] = stats[int(i)]
        else:
            line[int(each[1])] = stats[int(each[1])]
        datas.append({each[2]: line})
    for each in datas:
        req = urllib2.Request(each.keys()[0], urlencode(each.values()[0]))
        urllib2.urlopen(req)
    os.system('/sbin/iptables -Z PORTSTAT')


def main():
    parser = argparse.ArgumentParser(
        description='A simple port traffic monitor')
    parser.add_argument('-c', '--config', type=str,
                        default='/etc/portstat.conf', help='Path of the config file.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-v', '--version', help='Show portstat version.', action='store_true')
    group.add_argument(
        '-s', '--sync', help='Sync the portstat settings and iptables.', action='store_true')
    group.add_argument(
        '-u', '--upload', help='Upload the port stat with webhook.', action='store_true')
    args = parser.parse_args()
    portGroups = getConfig(args.config)
    if args.version:
        print('portstat in version %s' % version())
    if args.sync:
        sync(portGroups)
    if args.upload:
        upload(portGroups)


if __name__ == '__main__':
    main()
