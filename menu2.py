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
menu['1']="Power On/Off VMs"
menu['2']="Snapshot VMs"
menu['3']="Full Clone VM"
menu['4']="Linked Clone VM"
menu['5']="Delete VM"
menu['6']="Create VM from Template"
menu['7']="Exit"
while True:
    print("\n")
    for key in sorted(menu.keys()):
        print(f"{key}. {menu[key]}")

    choice = input("Choice: ")

    if choice == "1":

    elif choice == "2":

    elif choice == "3":

    elif choice == "4":

    elif choice == "5":

    elif choice == "6":
       
    elif choice == "7":
        Disconnect(si)
        break

    else:
        print("Invalid option, please enter 1-4.")