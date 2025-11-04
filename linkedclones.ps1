# variables
$vm = "win11"
$baseimage = "C:\Users\Public\Documents\Hyper-V\Virtual hard disks\WinDev2407Eval.vhdx"
$clonevm = "win11_clone"
$clonepath = "C:\Users\Public\Documents\Hyper-V\Virtual hard disks\"
$vmswitch = "LAN-INTERNAL"
$cpu = 2
$ram = 4GB

# powershell
New-VHD -Path "$clonepath$clonevm.vhdx" -ParentPath $baseimage -Differencing
New-VM -Name $clonevm -Generation 2
Set-VM $clonevm -ProcessorCount $cpu -MemoryStartupBytes $ram
Remove-VMHardDiskDrive -VMName $clonevm -ControllerType SCSI -ControllerNumber 0 
Add-VMHardDiskDrive -VMName $clonevm -Path "$clonepath$clonevm.vhdx"
Set-VMFirmware -VmName $clonevm -EnableSecureBoot Off
Connect-VMNetworkAdapter -VMName $clonevm -SwitchName $vmswitch

# start the vm
Start-VM $clonevm
Write-Host "Linked clone $clonevm has been created and started!"

