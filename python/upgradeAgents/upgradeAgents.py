#!/usr/bin/env python
"""Upgrade Cohesity Agents Using Python"""

### usage: ./upgradeAgents.py -v 192.168.1.198 -u admin [-d local]

### import pyhesity wrapper module
from pyhesity import *
from datetime import datetime
import codecs

### command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vip', type=str, default='helios.cohesity.com')
parser.add_argument('-u', '--username', type=str, default='helios')
parser.add_argument('-d', '--domain', type=str, default='local')
parser.add_argument('-t', '--tenant', type=str, default=None)
parser.add_argument('-c', '--clustername', type=str, action='append')
parser.add_argument('-mcm', '--mcm', action='store_true')
parser.add_argument('-i', '--useApiKey', action='store_true')
parser.add_argument('-pwd', '--password', type=str, default=None)
parser.add_argument('-np', '--noprompt', action='store_true')
parser.add_argument('-m', '--mfacode', type=str, default=None)
parser.add_argument('-e', '--emailmfacode', action='store_true')
parser.add_argument('-o', '--ostype', type=str, default=None)
parser.add_argument('-x', '--execute', action='store_true')
parser.add_argument('-s', '--showcurrent', action='store_true')
parser.add_argument('-n', '--agentname', action='append', type=str)
parser.add_argument('-l', '--agentlist', type=str)
parser.add_argument('-k', '--skipwarnings', action='store_true')

args = parser.parse_args()

vip = args.vip
username = args.username
domain = args.domain
tenant = args.tenant
clusternames = args.clustername
mcm = args.mcm
useApiKey = args.useApiKey
password = args.password
noprompt = args.noprompt
mfacode = args.mfacode
emailmfacode = args.emailmfacode
ostype = args.ostype
showcurrent = args.showcurrent
execute = args.execute
agentnames = args.agentname
agentlist = args.agentlist
skipwarnings = args.skipwarnings


# gather server list
def gatherList(param=None, filename=None, name='items', required=True):
    items = []
    if param is not None:
        for item in param:
            items.append(item)
    if filename is not None:
        f = open(filename, 'r')
        items += [s.strip() for s in f.readlines() if s.strip() != '']
        f.close()
    if required is True and len(items) == 0:
        print('no %s specified' % name)
        exit()
    return items


agentnames = gatherList(agentnames, agentlist, name='agents', required=False)

# authenticate
apiauth(vip=vip, username=username, domain=domain, password=password, useApiKey=useApiKey, helios=mcm, prompt=(not noprompt), emailMfaCode=emailmfacode, mfaCode=mfacode, tenantId=tenant)

# exit if not authenticated
if apiconnected() is False:
    print('authentication failed')
    exit(1)

now = datetime.now()
dateString = now.strftime("%Y-%m-%d-%H-%M-%S")

if mcm or vip.lower() == 'helios.cohesity.com':
    outfile = 'agentUpgrades-helios-%s.csv' % dateString
    if clusternames is None or len(clusternames) == 0:
        clusternames = [c['name'] for c in heliosClusters()]
else:
    cluster = api('get', 'cluster')
    clusternames = [cluster['name']]
    cluster = api('get', 'cluster')
    outfile = 'agentUpgrades-%s-%s.csv' % (cluster['name'], dateString)

f = codecs.open(outfile, 'w')
f.write('Cluster Name,Cluster Version,Agent Name,Agent Version,OS Type,OS Name,Status,Error Message\n')

reportNextSteps = False

for clustername in clusternames:
    print('Connecting to %s...\n' % clustername)
    if mcm or vip.lower() == 'helios.cohesity.com':
        heliosCluster(clustername)

    cluster = api('get', 'cluster')

    ### get Physical Servers
    nodes = api('get', 'protectionSources/registrationInfo?environments=kPhysical&allUnderHierarchy=true')

    if nodes is not None and 'rootNodes' in nodes and nodes['rootNodes'] is not None:
        for node in nodes['rootNodes']:
            tenant = ''
            agentIds = []  # list of agents to upgrade
            name = node['rootNode']['physicalProtectionSource']['name']
            version = 'unknown'
            hostType = 'unknown'
            osName = 'unknown'
            status = 'unknown'
            errorMessage = ''
            errors = ''
            if 'entityPermissionInfo' in node['rootNode']:
                if tenant in node['rootNode']['entityPermissionInfo']:
                    if 'name' in node['rootNode']['entityPermissionInfo']['tenant']:
                        tenant = node['rootNode']['entityPermissionInfo']['tenant']['name']
            try:
                if 'authenticationErrorMessage' in node['registrationInfo'] and node['registrationInfo']['authenticationErrorMessage'] is not None:
                    errorMessage = node['registrationInfo']['authenticationErrorMessage'].split(',')[0].split('\n')[0]
                if 'refreshErrorMessage' in node['registrationInfo'] and node['registrationInfo']['refreshErrorMessage'] is not None and node['registrationInfo']['refreshErrorMessage'] != '':
                    errorMessage = node['registrationInfo']['refreshErrorMessage'].split(',')[0].split('\n')[0]
            except Exception:
                pass
            if len(agentnames) == 0 or name.lower() in [a.lower() for a in agentnames]:
                if 'agents' in node['rootNode']['physicalProtectionSource'] and node['rootNode']['physicalProtectionSource']['agents'] is not None and len(node['rootNode']['physicalProtectionSource']['agents']) > 0:
                    try:
                        version = node['rootNode']['physicalProtectionSource']['agents'][0]['version']
                        hostType = node['rootNode']['physicalProtectionSource']['hostType'][1:]
                        osName = node['rootNode']['physicalProtectionSource']['osName']
                    except Exception:
                        pass
                    for agent in node['rootNode']['physicalProtectionSource']['agents']:
                        if 'upgradability' in agent and agent['upgradability'] is not None:
                            if agent['upgradability'] == 'kUpgradable':
                                status = 'upgradable'
                                agentIds.append(agent['id'])
                            else:
                                status = 'current'
                if ostype is None or ostype.lower() == hostType.lower():
                    if len(agentIds) > 0:
                        if errorMessage != '':
                            errors = '(warning: registration/refresh errors)'
                        if skipwarnings is not True or errors == '':
                            if execute is True:
                                status = 'upgrading'
                                print('    %s (%s): upgrading ...  %s' % (name, hostType, errors))
                                thisUpgrade = {'agentIds': agentIds}
                                if tenant != '':
                                    impersonate(tenant)
                                result = api('post', 'physicalAgents/upgrade', thisUpgrade)
                                if tenant != '':
                                    switchback()
                            else:
                                print('    %s (%s): %s ***  %s' % (name, hostType, status, errors))
                                reportNextSteps = True
                    else:
                        if showcurrent is True or name.lower() in [a.lower() for a in agentnames]:
                            print('    %s (%s): %s  %s' % (name, hostType, status, errors))
                f.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (cluster['name'], cluster['clusterSoftwareVersion'], name, version, hostType, osName, status, errorMessage))

if reportNextSteps is True:
    print('\nTo perform the upgrades, rerun the script with the -x (--execute) switch')

f.close()
print('\nOutput saved to %s\n' % outfile)
