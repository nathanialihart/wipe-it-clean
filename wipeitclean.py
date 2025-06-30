import subprocess

def r(cmd):
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd], capture_output=True)

bloat = [
    "Microsoft.*","Microsoft.Xbox*","Microsoft.GetHelp","Microsoft.Getstarted","Microsoft.Messaging","Microsoft.Microsoft*",
    "Microsoft.MixedReality*","Microsoft.Office*","Microsoft.OneConnect","Microsoft.People","Microsoft.Print3D","Microsoft.SkypeApp",
    "Microsoft.Wallet","Microsoft.Whiteboard","Microsoft.Windows*","Microsoft.Zune*","Microsoft.Bing*","Microsoft.YourPhone",
    "Clipchamp.Clipchamp","Microsoft.Todos","Microsoft.PowerAutomateDesktop","Microsoft.WindowsTerminal","Microsoft.WindowsNotepad",
    "Microsoft.WindowsMail","Microsoft.MSPaint","Microsoft.Advertising.Xaml","Microsoft.ScreenSketch","Microsoft.StorePurchaseApp",
    "Microsoft.VP9VideoExtensions","Microsoft.WebMediaExtensions","Microsoft.WebpImageExtensions","Microsoft.DesktopAppInstaller",
    "Microsoft.MSPaint","Microsoft.GetHelp","Microsoft.People","Microsoft.WindowsFeedbackHub","Microsoft.WindowsSoundRecorder",
    "Microsoft.XboxGameOverlay","Microsoft.XboxGamingOverlay","Microsoft.XboxIdentityProvider","Microsoft.XboxSpeechToTextOverlay"
]

for app in bloat:
    r(f"Get-AppxPackage -Name {app} -AllUsers | Remove-AppxPackage -ErrorAction SilentlyContinue")
    r(f"Get-AppxProvisionedPackage -Online | Where-Object {{$_.DisplayName -like '{app}'}} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue")

cleanup_cmds = [
    "Dism /Online /Cleanup-Image /StartComponentCleanup /ResetBase /Quiet /NoRestart",
    "Dism /Online /Cleanup-Image /SPSuperseded /Quiet /NoRestart",
    "Dism /Online /Cleanup-Image /AnalyzeComponentStore",
    "Remove-Item -Path 'C:\\Windows\\SoftwareDistribution\\Download\\*' -Recurse -Force -ErrorAction SilentlyContinue",
    "Remove-Item -Path 'C:\\Windows\\Temp\\*' -Recurse -Force -ErrorAction SilentlyContinue",
    "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue"
]

for cmd in cleanup_cmds:
    r(cmd)

tasks = [
    "Microsoft\\Windows\\Customer Experience Improvement Program\\*",
    "Microsoft\\Windows\\Application Experience\\*",
    "Microsoft\\Windows\\Autochk\\*",
    "Microsoft\\Windows\\Windows Error Reporting\\*",
    "Microsoft\\Windows\\Feedback\\*",
    "Microsoft\\Windows\\UpdateOrchestrator\\*",
    "Microsoft\\Windows\\LocationNotification\\*",
    "Microsoft\\Windows\\Maps\\*",
    "Microsoft\\Windows\\Defrag\\ScheduledDefrag",
    "Microsoft\\Windows\\DiskCleanup\\*",
    "Microsoft\\Windows\\Shell\\FamilySafetyMonitor*"
]

for task in tasks:
    r(f'Schtasks /Change /TN "{task}" /Disable')

services = [
    "DiagTrack","dmwappushsvc","Wecsvc","WerSvc","Wuauserv","DoSvc","BthAvctpSvc","MapsBroker","WSearch","SysMain",
    "SecurityHealthService","WMPNetworkSvc","UsoSvc","DeliveryOptimization","Wcmsvc","UnistoreSvc","UnistoreSvcGroup"
]

for svc in services:
    r(f"Stop-Service {svc} -Force -ErrorAction SilentlyContinue")
    r(f"Set-Service {svc} -StartupType Disabled")

r('Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Signature Updates" -Name "DisableSignatureUpdates" -Value 1 -Type DWord -Force')

reg_cmds = [
    'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Type DWord -Value 0 -Force',
    'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent" -Name "DisableWindowsConsumerFeatures" -Type DWord -Value 1 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" -Name "Enabled" -Type DWord -Value 0 -Force',
    'Set-ItemProperty -Path "HKCU:\\Control Panel\\Location" -Name "Enabled" -Type DWord -Value 0 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" -Name "CortanaConsent" -Type DWord -Value 0 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" -Name "DisableNotificationCenter" -Value 1 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" -Name "DisableActionCenter" -Value 1 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SystemPaneSuggestionsEnabled" -Value 0 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SubscribedContent-338388Enabled" -Value 0 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SubscribedContent-338389Enabled" -Value 0 -Force',
    'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SubscribedContent-353694Enabled" -Value 0 -Force'
]

for cmd in reg_cmds:
    r(cmd)
