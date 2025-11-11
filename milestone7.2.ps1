#1 - vm summary
function Get-VMSummary {

    $vms = Get-VM

    Write-Host "Getting VMs..."

    foreach ($vm in $vms) {
        $ip = (Get-VMNetworkadapter -VMName $vm.name).IPAddresses

        Write-Host "`nVM Name: $($vm.Name)"
        Write-Host "Power State: $($vm.State)"
        Write-Host "IP Address: $ip"
    }
}

#2 - vm detailed info
function Get-VMDetailed {
    param($vmname)

    Write-Host "Getting $($vmname)s info..."

    $vm = Get-VM -Name $vmname
    $cpu = Get-VMProcessor -VMName $vmname
    $disk = Get-VMHardDiskDrive -VMName $vmname
    $net = Get-VMNetworkAdapter -VMName $vmname

    Write-Host "`nVM Name: $($vm.Name)"
    Write-Host "Power State: $($vm.State)"
    Write-Host "CPU Count: $($cpu.Count)"
    Write-Host "Memory (in GB): $($vm.MemoryAssigned / 1GB)"
    Write-Host "Disk: $($disk.Path)"
    Write-Host "Network Switch: $($net.SwitchName)"
}


clear

$Prompt = "`n"
$Prompt += "1 - VM Summary`n"
$Prompt += "2 - VM Detailed Info`n"
$Prompt += "3 - Take VM Snapshot`n"
$Prompt += "4 - Restore Snapshot`n"
$Prompt += "5 - Delete VM Snapshot`n"
$Prompt += "6 - Power On/Off VM`n"
$Prompt += "7 - Create Full Clone VM`n"
$Prompt += "8 - Delete VM`n"
$Prompt += "9 - Exit"


$operation = $true

while($operation){

    Write-Host $Prompt | Out-String
    $choice = Read-Host "Select your option"
#9 - exit
    if($choice -eq 9){
        Write-Host "Seeya!" | Out-String
        exit
        $operation = $false
    }
#1 - vm summary
    elseif($choice -eq 1){
        Get-VMSummary
    }
#2 - detailed individual vm info
    elseif($choice -eq 2){
        $vmname = Read-Host "Enter name of VM youd like the details of"
        Get-VMDetailed -vmname $vmname
    }
#3 - take snapshot of vm
    elseif($choice -eq 3){
        $vmname = Read-Host "Enter name of VM youd like to snapshot"

        $vm = Get-VM -Name $vmname -ErrorAction SilentlyContinue

        if($vm -eq $null){
            Write-Host "VM '$vmname' not found. Please try again."
        }
        else{

            $snapshotname = Read-Host "Enter name of snapshot"

            Checkpoint-VM -Name $vmname -SnapshotName $snapshotname
        }
    }
#4 - restore snapshot
    elseif($choice -eq 4){
        $vmname = Read-Host "Enter name of VM youd like to restore the snapshot of"

        $vm = Get-VM -Name $vmname -ErrorAction SilentlyContinue

        if($vm -eq $null){
            Write-Host "VM '$vmname' not found. Please try again."
        }
        else{

            $snapshotname = Read-Host "Enter name of snapshot to restore to"

            Restore-VMSnapshot -VMName $vmname -Name $snapshotname
        }
    }
#5 - delete snapshot
    elseif($choice -eq 5){
        $vmname = Read-Host "Enter name of VM youd like to delete the snapshot of"

        $vm = Get-VM -Name $vmname -ErrorAction SilentlyContinue

        if($vm -eq $null){
            Write-Host "VM '$vmname' not found. Please try again."
        }
        else{

            $snapshotname = Read-Host "Enter name of snapshot to delete"

            Remove-VMSnapshot -VMName $vmname -Name $snapshotname
        }
    }
# 6 - power vm on/off
    elseif($choice -eq 6){
        $vmname = Read-Host "Enter name of VM to be powered on/off"
        
        $vm = Get-VM -Name $vmname -ErrorAction SilentlyContinue

        if($vm -eq $null){
            Write-Host "VM '$vmname' not found. Please try again."
        }
        else{

            $powerstate = Read-Host "`nPower on = 1`nPower off = 2"
                if ($powerstate -eq 1){
                    Start-VM -Name $vmname
                    }
                elseif($powerstate -eq 2){
                    Stop-VM -Name $vmname
                    }
                else{
                    Read-Host "Incorrect value entered. Please try again."
                    }
             }
    }
#7 - create full clone
    elseif($choice -eq 7){
        $vmname = Read-Host "Enter name of VM youd like to clone"

        $clonename = Read-Host "Enter name of clone"

        $vm = Get-VM -Name $vmname -ErrorAction SilentlyContinue

        if($vm -eq $null){
            Write-Host "VM '$vmname' not found. Please try again."
        }
        else{
            $sourcedisk = Get-VMHardDiskDrive -VMName $vmname

            $basepath = "C:\Users\Public\Documents\Hyper-V\Virtual Hard Disks\"
            $newdiskpath = "$basepath$clonename.vhdx"

            Copy-Item -Path $sourcedisk.Path -Destination $newdiskpath
            Write-Host "Creating VM..."
            New-VM -Name $clonename -MemoryStartupBytes $vm.MemoryStartup -Generation $vm.Generation -NoVHD

            Add-VMHardDiskDrive -VMName $clonename -Path $newdiskpath 
            $cpuCount = (Get-VMProcessor -VMName $sourcevm).Count
            Set-VMProcessor -VMName $clonename -Count $cpuCount
            $sourceNet = Get-VMNetworkAdapter -VMName $vmname
            Connect-VMNetworkAdapter -VMName $clonename -SwitchName $sourceNet.SwitchName
    

        }
    }
#8 - delete vm
    elseif($choice -eq 8){
        $vmname = Read-Host "Enter name of VM youd like to delete"

        $vm = Get-VM -Name $vmname -ErrorAction SilentlyContinue

        if($vm -eq $null){
            Write-Host "VM '$vmname' not found. Please try again."
        }
        else{
            Remove-VM -Name $vmname
        }
    }

}
