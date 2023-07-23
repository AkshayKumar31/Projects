# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 15:08:33 2023

@author: aksha
"""

import pysftp
import os
import time

def import_folder(host, user, password, port, remote_folder, destination_folder):
    
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  
    
    curr_path = os.getcwd()
    os.chdir(destination_folder)
    new_folder = destination_folder 
    #os.mkdir(new_folder)
    os.chdir(new_folder)
    
    with pysftp.Connection(host=host, username=user, password=password, port=port, cnopts=cnopts) as sftp:
        print('connection made')
        
        dir_list = sftp.listdir(remote_folder)
        print(dir_list)
        
        input_files = input("\nEnter comma-separated values of the files to copy without space after comma: ")
        
        remote_files_to_copy = input_files.split(',')
        print("    \n\n")
        print(remote_files_to_copy)
        
        for file in remote_files_to_copy:
            print(file)
            sftp.get(remote_folder + '/' + file)
        
    os.chdir(curr_path)


# Calling import_folder function
host = 'Your pi ip address on local network'
user = 'user name of your pi'
password = 'password for your pi'
port = 22
remote_folder = 'Location of remote folder on pi from which the scripts has to be copied'
destination_folder = 'Location of the folder in which the script should be copied to on local machine'

import_folder(host, user, password, port, remote_folder, destination_folder)
