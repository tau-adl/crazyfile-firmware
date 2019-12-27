# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2016 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Simple example that connects to one crazyflie (check the address at the top
and update it to your crazyflie address) and send a sequence of setpoints,
one every 5 seconds.

This example is intended to work with the Loco Positioning System in TWR TOA
mode. It aims at documenting how to set the Crazyflie in position control mode
and how to send setpoints.
"""
import time
import json
import sys
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/E7E7E7E704'


def param_callback(name, value):
    """Generic callback registered for all the groups"""
    print('parameter updated {0}: {1}'.format(name, value))

def update_parameters(scf,data):
    cf = scf.cf
    
    print('\n\n')
    print('------------------------------- parameters prior to update--------------------------------')
    print('\n\n')
    
    p_toc = cf.param.toc.toc
    for group in sorted(p_toc.keys()):
        #print('{}'.format(group))
        for param in sorted(p_toc[group].keys()):
            #print('\t{}'.format(param))
            if '{0}.{1}'.format(group,param) in data.keys():
                cf.param.add_update_callback(group=group, name=param,cb=param_callback)            
     
    time.sleep(2)
     
    print('\n\n')
    print('------------------------------- parameters updated on request--------------------------------')
    print('\n\n')
     
    for key in sorted(data.keys()):
        key_split = key.split(".")
        if len(key_split) is not 2:
            print('Format error! no in correct format : ' + key)
            break
        if key_split[0] in p_toc.keys():
            if key_split[1] in p_toc[key_split[0]].keys():
                if p_toc[key_split[0]][key_split[1]].access is 0:
                    cf.param.set_value(key, data[key])
            else:
                print('No such param in TOC: ' + key)
                break
        else:
            print('No such param in TOC: ' + key)
            break
            
    time.sleep(2)   
        
if __name__ == '__main__':
    
    if (len(sys.argv) - 1) is not 1:
        print('Missing argument!')
        print('correct usage: python3 updateParameters.py json_file.json') 
    else:   
        with open(sys.argv[1]) as json_file:
            data = json.load(json_file)
        
        cflib.crtp.init_drivers(enable_debug_driver=False)
        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
            update_parameters(scf,data)        
         
        
