# start-dev.ps1
# Sobe o front em modo dev
$ErrorActionPreference = "Stop"
cd $PSScriptRoot
npm install
npm run dev
