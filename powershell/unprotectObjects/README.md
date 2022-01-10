# Unprotect an Object using PowerShell

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This powershell script removes objects from protection jobs.

Note: if the object is the last remaining object in a protection job, the job will be deleted.

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'unprotectObjects'
$repoURL = 'https://raw.githubusercontent.com/bseltz-cohesity/scripts/master/powershell'
(Invoke-WebRequest -Uri "$repoUrl/$scriptName/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/cohesity-api/cohesity-api.ps1").content | Out-File cohesity-api.ps1; (Get-Content cohesity-api.ps1) | Set-Content cohesity-api.ps1
# End Download Commands
```

## Components

* unprotectObjects.ps1: the main powershell script
* cohesity-api.ps1: the Cohesity REST API helper module

Place both files in a folder together and run the main script like so:

```powershell
./unprotectObjects.ps1 -vip mycluster `
                       -username myusername `
                       -domain mydomain.net `
                       -objectName myserver.mydomain.net `
                       -jobName myjob
```

Note: server names must exactly match what is shown in protection sources.

## Parameters

* -vip: Cohesity cluster to connect to
* -username: Cohesity username (e.g. admin)
* -domain: (optional) Active Directory domain (defaults to 'local')
* -useApiKey: (optional) use API Key for authentication
* -password: (optional) will use stored password by default
* -objectName: (optional) comma separated list of object names to remove from jobs
* -objectList: (optional) text file containing object names to remove from jobs
* -jobName: (optional) comma separated list of job names to remove objects from
* -jobList: (optional) text file containing job names to remove objects from