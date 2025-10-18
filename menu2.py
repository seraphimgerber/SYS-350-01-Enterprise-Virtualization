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

    if choice == "1":
        search = input("VM name: ")
        vms = get_vms(search)
        for vm in vms:
            print(f"{vm.name} - {vm.runtime.powerState}")

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

    elif choice == "3":
        search = input("VM name: ")
        vms = get_vms(search)
        snap_name = input("Snapshot name: ")
        for vm in vms:
            vm.CreateSnapshot(snap_name, "", False, False)
            print(f"Snapshot created for {vm.name}")

    elif choice == "4":

    elif choice == "5":

    elif choice == "6":

    elif choice == "7":
       
    elif choice == "8":
        Disconnect(si)
        break

    else:
        print("Invalid option, please enter 1-4.")


# creds 
# create snapshot - https://github.com/reubenur-rahman/vmware-pyvmomi-examples/blob/master/create_and_remove_snapshot.py

