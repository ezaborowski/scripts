# Upgrade Cohesity Agents using Python

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This script will initiate upgrade for registered agents.

## Components

* upgradeAgents.py: the main python script
* pyhesity.py: the Cohesity REST API helper module

You can download the scripts using the following commands:

```bash
# download commands
curl -O https://raw.githubusercontent.com/bseltz-cohesity/scripts/master/python/upgradeAgents/upgradeAgents.py
curl -O https://raw.githubusercontent.com/bseltz-cohesity/scripts/master/python/pyhesity.py
chmod +x upgradeAgents.py
# end download commands
```

Running the script against one cluster (with direct authentication):

```bash
./upgradeAgents.py -v mycluster -u myuser -d local  # -d myAdDomain.net (for active directory)
```

If you want to initiate upgrades, include the -x (--execute) switch:

```bash
./upgradeAgents.py -v mycluster -u myuser -d local -x
```

Running the script against all Helios clusters (note: you will need to create an API key in helios and use that as the password when prompted):

```bash
./upgradeAgents.py -u myuser@mydomain.net
```

Running the script against selected Helios clusters (note: you will need to create an API key in helios and use that as the password when prompted):

```bash
./upgradeAgents.py -u myuser@mydomain.net -c cluster1 -c cluster2
```

## Authentication Parameters

* -v, --vip: (optional) DNS or IP of the Cohesity cluster to connect to (default is helios.cohesity.com)
* -u, --username: (optional) username to authenticate to Cohesity cluster (default is helios)
* -d, --domain: (optional) domain of username (defaults to local)
* -i, --useApiKey: (optional) use API key for authentication
* -pwd, --password: (optional) password or API key
* -np, --noprompt: (optional) do not prompt for password
* -mcm, --mcm: (optional) connect through MCM
* -c, --clustername: (optional) helios/mcm cluster to connect to (will loop through all clusters if connected to helios)
* -m, --mfacode: (optional) MFA code for authentication
* -e, --emailmfacode: (optional) send MFA code via email

## Other Parameters

* -x, --execute: (optional) initiate ugrades (will just show status if omitted)
* -o, --ostype: (optional) filter on OS type, e.g. windows, linuz, aix
* -s, --showcurrent: (optional) show up to date agents (will only show upgradable agents if omitted)
* -n, --agentname: (optional) only include agents with this name (repeat for multiple)
* -l, --agentlist: (optional) text file of agents to include (one per line)
* -k, --skipwarnings: (optional) exclude agents that have registration/refresh errors

## The Python Helper Module - pyhesity.py

The helper module provides functions to simplify operations such as authentication, api calls, storing encrypted passwords, and converting date formats. The module requires the requests python module.

### Installing the Prerequisites

```bash
sudo yum install python-requests
```

or

```bash
sudo easy_install requests
```
