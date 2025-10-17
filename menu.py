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

# hi menu!!
menu = {}
menu['1']="vCenter Info"
menu['2']="Session Details"
menu['3']="VM Details"
menu['4']="Exit"
while True:
    print("\n")
    for key in sorted(menu.keys()):
        print(f"{key}. {menu[key]}")

    choice = input("Choice: ")

    if choice == "1":
        print(f"Username: {config['username']}")
        print(f"vCenter Hostname: {config['vcenter_hostname']}")

    elif choice == "2":
        session = si.content.sessionManager.currentSession
        print(f"DOMAIN/Username: {session.userName}")
        print(f"vCenter Server: {config['vcenter_hostname']}")
        print(f"Source IP: {session.ipAddress}")

    elif choice == "3":
        search = input("VM name (or hit Enter for all:) ")
        container = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)

        for vm in container.view:
            if search == "" or search.lower() in vm.name.lower():
                print(f"\nVM Name: {vm._name}")
                print(f"Power State: {vm.runtime.powerState}")
                print(f"CPUs: {vm.config.hardware.numCPU}")
                print(f"Memory: {vm.config.hardware.memoryMB / 1024} GB")
                print(f"IP Address: {vm.guest.ipAddress if vm.guest.ipAddress else 'N/A'}")

    elif choice == "4":
        Disconnect(si)
        break

    else:
        print("Invalid option, please enter 1-4.")