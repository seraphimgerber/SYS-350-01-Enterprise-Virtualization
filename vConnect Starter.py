# vconnect hehe
# https://github.com/seraphimgerber/SYS-350-01-Enterprise-Virtualization/

import getpass
passw = getpass.getpass()
from pyVim.connect import SmartConnect
import ssl
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode=ssl.CERT_NONE
si=SmartConnect(host="vcenter.seraphim.local", user="seraphim-adm@seraphim.local", pwd=passw, sslContext=s)
aboutInfo=si.content.about
print(aboutInfo)
print(aboutInfo.fullName)