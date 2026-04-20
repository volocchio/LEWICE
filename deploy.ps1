[CmdletBinding()]
param(
    [Alias('m')]
    [string]$Message = "deploy $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'

$VpsHost = '185.164.110.65'
$VpsUser = 'root'
$SshKey = '/home/honeybadger/.ssh/id_ed25519'
$RemoteRepoPath = '/root/.openclaw/workspace-tag_coding/LEWICE'
$RepoName = Split-Path (Get-Location) -Leaf

Write-Host "Deploying $RepoName" -ForegroundColor Cyan

git add -A

$hasStaged = (& git diff --cached --name-only) -join "`n"
if ($hasStaged.Trim()) {
    git commit -m $Message
} else {
    Write-Host 'No staged changes to commit.' -ForegroundColor Yellow
}

if (-not $NoPush) {
    git push
}

$remoteCmd = "set -e; mkdir -p '$RemoteRepoPath'; if [ ! -d '$RemoteRepoPath/.git' ]; then git clone git@github.com:volocchio/LEWICE.git '$RemoteRepoPath'; fi; cd '$RemoteRepoPath'; git fetch origin; git reset --hard origin/master; /usr/local/bin/sync-and-update-portal.sh"

wsl ssh -i $SshKey "$VpsUser@$VpsHost" $remoteCmd

Write-Host 'Deploy completed.' -ForegroundColor Green
