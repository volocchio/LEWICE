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

$remoteScript = @"
set -e
mkdir -p '$RemoteRepoPath'
if [ ! -d '$RemoteRepoPath/.git' ]; then
    git clone git@github.com:volocchio/LEWICE.git '$RemoteRepoPath'
fi
cd '$RemoteRepoPath'
git fetch origin
git reset --hard origin/master
docker network ls | grep caddy-net >/dev/null || docker network create caddy-net
docker compose build --no-cache
docker compose up -d
if grep -q 'lewice.voloaltro.tech' /etc/caddy/Caddyfile; then
    perl -0777 -i -pe 's#lewice\\.voloaltro\\.tech\\s*\\{[^}]*\\}#lewice.voloaltro.tech {\\n\\treverse_proxy 127.0.0.1:8518\\n}#s' /etc/caddy/Caddyfile
else
    printf '\nlewice.voloaltro.tech {\n\treverse_proxy 127.0.0.1:8518\n}\n' >> /etc/caddy/Caddyfile
fi
caddy fmt --overwrite /etc/caddy/Caddyfile
systemctl reload caddy
if [ -x /usr/local/bin/sync-and-update-portal.sh ]; then
    /usr/local/bin/sync-and-update-portal.sh
else
    echo 'Skipping portal sync (script not found)'
fi
"@

$remoteScriptLf = $remoteScript -replace "`r", ""
$remoteScriptLf | wsl ssh -i $SshKey "$VpsUser@$VpsHost" "bash -s"

Write-Host 'Deploy completed.' -ForegroundColor Green
