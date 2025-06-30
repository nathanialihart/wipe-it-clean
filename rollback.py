import subprocess

def r(cmd):
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd], capture_output=True)

reg_cmds = [
    'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection" -Name "AllowTelemetry" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" -Name "Enabled" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKCU:\\Control Panel\\Location" -Name "Enabled" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" -Name "CortanaConsent" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent" -Name "DisableWindowsConsumerFeatures" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" -Name "DisableAntiSpyware" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" -Name "DisableRealtimeMonitoring" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" -Name "DisableNotificationCenter" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" -Name "DisableActionCenter" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\lfsvc\\Service\\Configuration" -Name "Status" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "EnableSmartScreen" -ErrorAction SilentlyContinue',
    'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "DisableCMD" -ErrorAction SilentlyContinue'
]

for cmd in reg_cmds:
    r(cmd)

r('Get-Service | Where-Object {$_.Status -eq "Stopped"} | Start-Service -ErrorAction SilentlyContinue')
r('Get-Service | Set-Service -StartupType Automatic -ErrorAction SilentlyContinue')
r('Get-ScheduledTask | foreach { Enable-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath -ErrorAction SilentlyContinue }')
r('Set-MpPreference -DisableRealtimeMonitoring $false')
r('Set-Service wuauserv -StartupType Automatic')
r('Start-Service wuauserv')
r('Set-Service WSearch -StartupType Automatic')
r('Start-Service WSearch')
r('Set-Service SysMain -StartupType Automatic')
r('Start-Service SysMain')
r('Set-Service SecurityHealthService -StartupType Automatic')
r('Start-Service SecurityHealthService')

diag_services = ["DiagTrack","dmwappushsvc","Wecsvc","WerSvc"]
for svc in diag_services:
    r(f'Set-Service {svc} -StartupType Automatic')
    r(f'Start-Service {svc}')

core_services = [
    "BITS","EventLog","Themes","LanmanWorkstation","LanmanServer","Dhcp","Dnscache",
    "AudioSrv","Audiosrv","PlugPlay","Power","RpcSs","Winmgmt","W32Time","ShellHWDetection",
    "EventSystem","CryptSvc","DcomLaunch","TrkWks","Spooler","Netman","WlanSvc","WbioSrvc"
]

for svc in core_services:
    r(f'Set-Service {svc} -StartupType Automatic')
    r(f'Start-Service {svc}')

r('sfc /scannow')
r('DISM /Online /Cleanup-Image /RestoreHealth')

store_apps = [
    "Microsoft.WindowsStore","Microsoft.DesktopAppInstaller","Microsoft.WindowsCalculator",
    "Microsoft.WindowsCamera","Microsoft.Windows.Photos","Microsoft.WindowsNotepad",
    "Microsoft.WindowsSoundRecorder","Microsoft.WindowsTerminal"
]

for app in store_apps:
    r(f'Get-AppxPackage -AllUsers -Name {app} | Foreach {{"Reinstalling: " + $_.Name; Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml" -ErrorAction SilentlyContinue }}')
