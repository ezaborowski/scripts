# Add Netapp Volumes to a Protection Job Using Python

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This script adds Netapp Volumes to a protection job.

Note: this script is written for Cohesity 6.5.1 and later

## Download the script

You can download the scripts using the following commands:

```bash
# download commands
curl -O https://raw.githubusercontent.com/bseltz-cohesity/scripts/master/python/protectNetapp/protectNetapp.py
curl -O https://raw.githubusercontent.com/bseltz-cohesity/scripts/master/python/pyhesity.py
chmod +x protectNetapp.py
# end download commands
```

## Components

* protectNetapp.py: the main powershell script
* pyhesity.py: the Cohesity REST API helper module

Place both files in a folder together and run the main script like so:

```bash
./protectNetapp.py -v mycluster \
                   -u myuser \
                   -d mydomain.net \
                   -j 'My Backup Job' \
                   -s myNetapp
```

## Parameters

* -v, --vip: DNS or IP of the Cohesity cluster to connect to
* -u, --username: username to authenticate to Cohesity cluster
* -d, --domain: (optional) domain of username, defaults to local
* -k, --useApiKey: (optional) use API key for authentication
* -pwd, --password: (optional) password of API key
* -s, --sourcename: name of registered Netapp to protect
* -z, --svmname: (optional) protect specific SVM (repeat for multiple SVMs)
* -n, --volumename: (optional) protect specific volumes (repeat for multiple volumes)
* -l, --volumelist: (optional) list of volume names in a text file
* -j, --jobname: name of the job to add the server to
* -i, --include: (optional) file path to include (use multiple times for multiple paths)
* -n, --includefile: (optional) a text file full of include paths
* -x, --exclude: (optional) file path to exclude (use multiple times for multiple paths)
* -f, --excludefile: (optional) a text file full of exclude file paths
* -sd, --storagedomain: (optional) name of storage domain to create job in (default is DefaultStorageDomain)
* -p, --policyname: (optional) name of protection policy to use for new job (only required for new job)
* -tz, --timezone: (optional) time zone for new job (default is US/Eastern)
* -st, --starttime: (optional) start time for new job (default is 21:00)
* -is, --incrementalsla: (optional) incremental SLA minutes (default is 60)
* -fs, --fullsla: (optional) full SLA minutes (default is 120)
* -ei, --enableindexing: (optional) default is no indexing
* -c, --cloudarchivedirect: (optional) use direct cloud archiving
* -ip, --incrementalsnapshotprefix: (optional) prefix of Netapp snapshot name
* -fp, --fullsnapshotprefix: (optional) prefix of Netapp snapshot name
* -enc, --encryptionenabled: (optional) enable in-flight encryption of data between the Netapp and Cohesity