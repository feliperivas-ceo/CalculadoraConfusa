param(
    [string]$FrontendHost = $env:FRONTEND_HOST,
    [string]$FrontendUser = $env:FRONTEND_USER,
    [string]$BackendUrl = $env:BACKEND_URL,
    [string]$RemoteDir = $(if ($env:REMOTE_DIR) { $env:REMOTE_DIR } else { "~/calculadora-frontend" })
)

$ErrorActionPreference = "Stop"

if (-not $FrontendHost) { throw "Define FRONTEND_HOST, por ejemplo 192.168.131.37" }
if (-not $FrontendUser) { throw "Define FRONTEND_USER, por ejemplo swarch" }
if (-not $BackendUrl) { throw "Define BACKEND_URL, por ejemplo http://192.168.131.192:5000" }

$Remote = "{0}@{1}" -f $FrontendUser, $FrontendHost

ssh $Remote "mkdir -p $RemoteDir/frontend"
scp docker-compose.frontend.yml "${Remote}:$RemoteDir/"
scp frontend/Dockerfile frontend/index.html frontend/nginx.conf frontend/entrypoint.sh "${Remote}:$RemoteDir/frontend/"
ssh $Remote "cd $RemoteDir && BACKEND_URL='$BackendUrl' docker compose -f docker-compose.frontend.yml up -d --build"

Write-Host "Frontend deployed on ${FrontendHost}:8080"