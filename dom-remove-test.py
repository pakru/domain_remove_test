#!/usr/local/bin/python3.5

import config, time, sys, colorama, logging
#import os
from colorama import Fore, Back, Style
#import modules.cocon_interface as ccn_iface
#import threading
#import json
#import argparse
import ssh_cocon.ssh_cocon as ccn
#import argparse
# JSON parsing

testingDomain = config.testConfigJson['DomainName']

colorama.init(autoreset=True)

def preconfigure():
    if ccn.domainDeclare(dom=testingDomain,removeIfExists = True):
        print(Fore.GREEN + 'Successful domain declare')
        logging.info('Successful domain declare ' + testingDomain)
    else:
        print(Fore.RED + 'Smthing happen wrong with domain declaration...')
        logging.error('Failed to declare domain ' + testingDomain)
        return False

    cnt = 0
    time.sleep(2)
    while not ccn.checkDomainInit(dom=testingDomain):  # проверяем инициализацию домена
        #print(Fore.YELLOW + 'Not inited yet...')
        logging.info('Domain initialisation check')
        cnt += 1
        if cnt > 5:
            print(Fore.RED + "Test domain wasn't inited :(")
            logging.error('Domain '+ testingDomain +' was not initialised!')
            return False
        time.sleep(2)
    #print(Fore.GREEN +'Domain inited!')
    logging.info('Domain initialised successfully')

    time.sleep(2)
    print('Removing our test domain')
    if ccn.domainRemove(dom=testingDomain):
        print(Fore.GREEN + 'Successful domain remove')
        logging.info('Successful domain remove ' + testingDomain)
    else:
        print(Fore.RED + 'Smthing happen wrong with domain removing...')
        logging.error('Domain ' + testingDomain + ' failed to remove!')
        return False

    time.sleep(7)
    if ccn.checkDomainExist(dom=testingDomain):
        print(Fore.RED + 'Failed, domain exists!')
        logging.error('Domain ' + testingDomain + ' exists in domain list!')
        return False
    else:
        print(Fore.GREEN + 'Domain is not exists in domain/list')
        logging.info('Domain '+ testingDomain +' is not exists in domain/list')


    returnedFromSSH = ccn.executeOnSSH('ls /domain/')
    print(returnedFromSSH)

    if testingDomain in returnedFromSSH:
        print(Fore.RED +'Domain exists in cocon!')
        logging.error('Domain ' + testingDomain + ' is exists in cocon!')
        return False
    else:
        print(Fore.GREEN +'Domain is not exsists in cocon! All ok!')
        logging.info('Domain ' + testingDomain + ' is not exists in cocon')
    return True

print(Fore.LIGHTWHITE_EX +'-Start domain remove test-')
logging.info('Start domain remove test')
if not preconfigure():
    print(Fore.RED + 'Domain remove test failed')
    logging.error('Domain remove test failed!')
    #ccn.coconInt.eventForStop.set()
    sys.exit(1)
else:
    print('-Domain remove test done!-')
    logging.info('Domain remove test done!')
    time.sleep(1)

print(Fore.GREEN + 'It seems to be all FINE...')
print('We did it!!')

sys.exit(0)
