import json
import ssl
import getpass
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

# reading config file
with open('vcenter-config.json') as f:
    config = json.load(f)

# connect to vcenter
password = getpass.getpass(f"Password for {config['username']}: ")
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_NONE
si = SmartConnect(host=config['vcenter_hostname'], user=config['username'], pwd=password, sslContext=context)

# get vms list
def get_vms(search=""):
    container = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
    vms = []
    for vm in container.view:
        if search == "" or search.lower() in vm.name.lower():
            vms.append(vm)
    return vms

# hi menu!!
menu = {}
menu['1'] = "List VMs"
menu['2'] = "Power On/Off"
menu['3'] = "Snapshot"
menu['4'] = "Full Clone"
menu['5'] = "Linked Clone"
menu['6'] = "Delete VM"
menu['7'] = "Create from Template"
menu['8'] = "Exit"
while True:
    print("\n")
    for key in sorted(menu.keys()):
        print(f"{key}. {menu[key]}")

    choice = input("Choice: ")
    # list vms
    if choice == "1":
        search = input("VM name: ")
        vms = get_vms(search)
        for vm in vms:
            print(f"{vm.name} - {vm.runtime.powerState}")
    # power on/off
    elif choice == "2":
        search = input("VM name: ")
        vms = get_vms(search)
        action = input("1=On, 2=Off: ")
        for vm in vms:
            if action == "1":
                vm.PowerOn()
            else:
                vm.PowerOff()
            print(f"{vm.name} done")
    # snapshot
    elif choice == "3":
        search = input("VM name: ")
        vms = get_vms(search)
        snap_name = input("Snapshot name: ")
        for vm in vms:
            vm.CreateSnapshot(snap_name, "", False, False)
            print(f"Snapshot created for {vm.name}")
    # full clone
    elif choice == "4":
        vm_name = input("VM to clone: ")
        clone_name = input("Clone name: ")
        vms = get_vms(vm_name)
        if vms:
            vm = vms[0]
            clonespec = vim.vm.CloneSpec()
            clonespec.location = vim.vm.RelocateSpec()
            clonespec.powerOn = False
            clonespec.template = False
            vm.Clone(folder=vm.parent, name=clone_name, spec=clonespec)
            print("Creating full clone...")
    # linked clone
    elif choice == "5":
        vm_name = input("VM to clone: ")
        clone_name = input("Clone name: ")
        vms = get_vms(vm_name)
        if vms:
            vm = vms[0]
            if not vm.snapshot:
                vm.CreateSnapshot("temp", "", False, False)
                time.sleep(2)
            
            clonespec = vim.vm.CloneSpec()
            clonespec.location = vim.vm.RelocateSpec()
            clonespec.location.diskMoveType = 'createNewChildDiskBacking'
            clonespec.powerOn = False
            clonespec.template = False
            clonespec.snapshot = vm.snapshot.currentSnapshot
            vm.Clone(folder=vm.parent, name=clone_name, spec=clonespec)
            print("Creating linked clone...")
        
    # delete VMs
    elif choice == "6":
        
    # create from template
    elif choice == "7":
        
    # exit
    elif choice == "8":
        Disconnect(si)
        break

    else:
        print("Invalid option, please enter 1-4.")


# creds 
# create snapshot - https://github.com/reubenur-rahman/vmware-pyvmomi-examples/blob/master/create_and_remove_snapshot.py
# full and linked clone - https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/clone_vm.py

