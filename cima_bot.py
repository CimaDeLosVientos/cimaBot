# coding=utf-8
####################################
##############CIMABOT###############
###ASOCIACIÓN CIMA DE LOS VIENTOS###
####### @Luis_gar # @Seind #########
####################################

import json
import requests
import time
import urllib
import sys
import math

from handler import *
#import aposteitor as app


def main():

    last_update_id = None
    clearSignal = int(sys.argv[1])
    print("Estoy vivo")

    while True:
        updates = get_updates(last_update_id)
        print(updates)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            if clearSignal == 1:
                updates["result"][0].clear()
                clearSignal = 0
            for update in updates["result"]:
                handle(update)


if __name__ == '__main__':
    main()
