#!/usr/local/bin/python3.5

import config

#import os
import time
import sys
import colorama
from colorama import Fore, Back, Style
#import modules.cocon_interface as ccn_iface
import threading
import logging
#import json
#import argparse
import ssh_cocon.ssh_cocon as ccn
import argparse
# JSON parsing
'''
testConfigFile = open('dom-remove.json')
config.testConfigJson = json.loads(testConfigFile.read())
testConfigFile.close()
'''
'''
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--custom_config', type=argparse.FileType())
#parser.add_argument("-с", "--config", help="path to *.json config file")
args = parser.parse_args()
if args.custom_config:
    print("config is used: " + str(args.custom_config))
'''


testingDomain = config.testConfigJson['DomainName']

'''
coreNode = 'core1@ecss1'
sipNode = 'sip1@ecss1'
dsNode = 'ds1@ecss1'
'''

colorama.init(autoreset=True)


def preconfigure():
    if ccn.domainDeclare(dom=testingDomain,removeIfExists = True):
        print(Fore.GREEN + 'Successful domain declare')
    else:
        print(Fore.RED + 'Smthing happen wrong with domain declaration...')
        return False

    cnt = 0
    time.sleep(2)
    while not ccn.checkDomainInit(dom=testingDomain):  # проверяем инициализацию домена
        print(Fore.YELLOW + 'Not inited yet...')
        cnt += 1
        if cnt > 5:
            print(Fore.RED + "Test domain wasn't inited :(")
            return False
        time.sleep(2)
    print(Fore.GREEN +'Domain inited!')

    time.sleep(2)
    print('Removing our test domain')
    if ccn.domainRemove(dom=testingDomain):
        print(Fore.GREEN + 'Successful domain remove')
    else:
        print(Fore.RED + 'Smthing happen wrong with domain removing...')
        return False

    time.sleep(7)
    if ccn.checkDomainExist(dom=testingDomain):
        print('Failed, domain exists')
        return False
    else:
        print('Domain is not exists in domain/list')

    returnedFromSSH = ccn.executeOnSSH('ls /domain/')
    print(returnedFromSSH)

    if testingDomain in returnedFromSSH:
        print('Domain exists in cocon!')
        return False
    else:
        print('Domain is not exsists in cocon! All ok!')
    return True


# def ccn_iface_preconfigure():


# logging.basicConfig(format = u'%(asctime)-8s %(levelname)-8s %(message)-8s', filemode='w', level = logging.INFO)
# logger = logging.getLogger("tester")
'''
test_var = {"%%DEV_USER%%":"admin", "%%DEV_PASS%%":"password", "%%SERV_IP%%":"192.168.118.49"}
coconInt = ccn_iface.coconInterface(test_var, show_cocon_output=True)
coconInt.eventForStop = threading.Event()
#Поднимаем thread
coconInt.myThread = threading.Thread(target=ccn_iface.ccn_command_handler, args=(coconInt,))
coconInt.myThread.start()
#Проверяем, что он жив.
time.sleep(0.2)
if not coconInt.myThread.is_alive():
	print('Can\'t start CCN configure thread')
	sys.exit(1)

test = '/node/uptime\nsystem-status\n'

# ccn_iface.cocon_push_string_command(coconCommands,coconInt)

ccn_iface.cocon_push_string_command(coconCommands=test, coconInt = coconInt)

print('recieved: ')
print(coconInt.data.decode('utf-8'))
'''

'''
testConfigFile = open('dom-remove.json')
testConfigStr = testConfigFile.read()
testConfigJson = json.loads(testConfigStr)
'''
# print('Readed json: ')
# print(testConfigJson)

# print(testingDomain)



print('-Start domain remove test-')
if not preconfigure():
    print(Fore.RED + 'Domain remove test failed')
    ccn.coconInt.eventForStop.set()
    sys.exit(1)
else:
    print('-Domain remove test done!-')
    time.sleep(1)

print(Fore.GREEN + 'It seems to be all FINE...')
print('We did it!!')

ccn.coconInt.eventForStop.set()

sys.exit(0)
