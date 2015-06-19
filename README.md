# portstat 

![](https://badge.fury.io/py/portstat.svg) ![](https://travis-ci.org/imlonghao/portstat.svg) ![](https://landscape.io/github/imlonghao/portstat/master/landscape.svg?style=flat)

A simple port traffic monitor

## Install

### Install pip

For Debian / Ubunut user

```
apt-get update
apt-get install python-pip
```

### Install portstat

```
pip install portstat
```

### System setting

Add the following line to `/etc/rc.local` to run portstat on the startup.

Notice that add it before `exit 0` .

```
/sbin/iptables -N PORTSTAT
/sbin/iptables -A INPUT -j PORTSTAT
/sbin/iptables -A OUTPUT -j PORTSTAT
/bin/bash /etc/portstat.rules
```

To upload the traffic information every minute, we should add the following line in `crontab -e`

```
* * * * * /usr/local/bin/portstat -u
```

Run it every 5 minutes like the following

```
*/5 * * * * /usr/local/bin/portstat -u
```

To activate the new iptables rules, please run the `/sbin/iptables` command manually or issue a `reboot` command.

After that, you have installed portstat successfully.

## Upgrade

Every new version I will upload it to pypi so that you can upgrade to the latest version with the following code.

```
pip install -U portstat
```

For some unexpectable reason, I can NOT promise that you can upgrade to the latest version without change your settings.

So, please come back to see what's new at every upgrade.

## Usage

```
usage: portstat [-h] [-c CONFIG] [-v | -s | -u]

A simple port traffic monitor

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path of the config file.
  -v, --version         Show portstat version.
  -s, --sync            Sync the portstat settings and iptables.
  -u, --upload          Upload the port stat with webhook.
```

## Tutorial

First of all, you should install portstat as I mentioned above.

Create a conf in where you like, by default the path is `/etc/portstat.conf`, just remenber use `-c path` to declare the config file if you don't use the default path.
The conf file should looks like that:

```
[imlonghao]
Port=80
Webhook=https://imlonghao.com/?imlonghao

[shadowsocks]
Port=10000-10010
Webhook=https://imlonghao.com/?shadowsocks
```

`[name]` used to distinguish every port you want to monitor.
 
`Port=111` used to declare the port you want to monitor, it should be a int like `111` , or a range like `10000-10010`

`Webhook=https://imlonghao.com/` used to received the traffic information, portstat will post the information to the webhook like that

![](https://cloud.githubusercontent.com/assets/4951333/8232820/24432094-1605-11e5-9534-5fc9362d1626.png)

Then, save the config file.

Run `portstat -s` to create new iptables rules to monitor the port you just add.

Run `portstat -u` to upload to port traffic information to webhook manually.

## Contribution

- [Issue](https://github.com/imlonghao/portstat/issues)
- [Pull Request](https://github.com/imlonghao/portstat/pulls)

## License

Licensed under the Apache License, Version 2.0