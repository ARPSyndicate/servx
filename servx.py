#!/usr/bin/python3

import optparse
import sys
import os

BLUE='\033[94m'
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CLEAR='\x1b[0m'

print(BLUE + "ServX[1.0] by ARPSyndicate" + CLEAR)
print(YELLOW + "Bash Command as a Service" + CLEAR)

if len(sys.argv)<2:
	print(RED + "[!] ./servx --help" + CLEAR)
	sys.exit()

else:
    parser = optparse.OptionParser()
    parser.add_option('-t', '--temp', action="store", default="template.servx", dest="template", help="service template")
    parser.add_option('-n', '--name', action="store", default="servx", dest="name", help="service name")
    parser.add_option('-c', '--cmd', action="store", dest="command", help="command to execute")
    parser.add_option('-e', '--enable-service', action="store_true", dest="enable", help="start service after creation", default=False)

inputs,args  = parser.parse_args()
if not inputs.command:
	parser.error(RED + "[!] command not given" + CLEAR)


temp = str(inputs.template)
name = str(inputs.name)
cmd = str(inputs.command)
enable = inputs.enable
ipath = "/etc/systemd/system/"+name+".service"

if(os.path.exists(ipath)):
    print(YELLOW + "[!] removing existing service with same name" + CLEAR)
    os.remove(ipath)

print(GREEN + "[+] service created" + CLEAR)
with open("template.servx", "r") as f:
    data = f.read()
    f.close()
with open(ipath, "w") as f:
    f.write(data.format(description=name, command=cmd))
    f.close()

if(enable):
    print(GREEN + "[+] service enabled" + CLEAR)
    os.system("systemctl enable {0}.service && systemctl start {0}.service".format(name))
