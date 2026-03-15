# Unbrowse setup for Cursor - run from project root
# 1. Install Unbrowse globally
# 2. Add Unbrowse skill for Cursor (non-interactive)
# You must run "npx unbrowse setup" once and accept ToS (y) when prompted.

$ErrorActionPreference = "Stop"
Write-Host "Installing Unbrowse globally..."
npm install -g unbrowse@latest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Adding Unbrowse skill for Cursor..."
npx -y skills add unbrowse-ai/unbrowse --yes --agent cursor
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Done. Next: run 'npx unbrowse setup' once and type y to accept the Terms of Service."
Write-Host "Then run 'unbrowse health' to verify. See scripts/setup_unbrowse_cursor.md for details."
