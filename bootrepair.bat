@echo off
color 0a
title BOOT REPAIR

echo Running SFC scan...
sfc /scannow

echo Running DISM Health Restore...
DISM /Online /Cleanup-Image /RestoreHealth

echo Restart recommended after completion.
pause
