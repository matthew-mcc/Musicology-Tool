#! /usr/bin/python3
# -*- coding: utf-8 -*-

#imports 
import os
import sys
import time
import json


import subprocess
subprocess.Popen([R'C:\Program Files (x86)\Audacity\audacity.exe'])
time.sleep(10)

#path to copy
#C:\GIT\2021Research\Our_Program\dataFiles
#mic_121617_103906-stereo-extract
# PATH = ""
# while not os.path.isdir(PATH):
#     PATH = os.path.realpath(input('Path to test folder: '))
#     print(PATH)
#     if not os.path.isdir(PATH):
#         print('Invalid path. Try again.')
# #print('Test folder: ' + PATH)
#could select a path using gui to get opath and name?
PATH_HERE = R"C:\GIT\2021Research\Our_Program\dataFiles"
INFILE_HERE = "mic_121617_103906-stereo"

def import_method(PATH, INFILE):
    while not os.path.isfile(os.path.join(PATH, INFILE)):
        #INFILE = input('Name of input WAV file: ')
        INFILE = INFILE
        # Ensure we have the .wav extension.
        INFILE = os.path.splitext(INFILE)[0] + '.wav'
        if not os.path.isfile(os.path.join(PATH, INFILE)):
            print(f"{os.path.join(PATH, INFILE)} not found. Try again.")
        else:
            print(f"Input file: {os.path.join(PATH, INFILE)}")
    # Remove file extension.
    INFILE = os.path.splitext(INFILE)[0]

    #Platform Constants
    if sys.platform == 'win32':
        print("recording-test.py, running on windows")
        PIPE_TO_AUDACITY = '\\\\.\\pipe\\ToSrvPipe'
        PIPE_FROM_AUDACITY = '\\\\.\\pipe\\FromSrvPipe'
        EOL = '\r\n\0'

    #ensuring the pipe is working fine
    print("Write to  \"" + PIPE_TO_AUDACITY +"\"")
    if not os.path.exists(PIPE_TO_AUDACITY):
        print(""" ..does not exist.
        Ensure Audacity is running with mod-script-pipe.""")
        sys.exit()

    print("Read from \"" + PIPE_FROM_AUDACITY +"\"")
    if not os.path.exists(PIPE_FROM_AUDACITY):
        print(""" ..does not exist.
        Ensure Audacity is running with mod-script-pipe.""")
        sys.exit()

    print("-- Both pipes exist.  Good.")

    #not sure if we need this part
    TOPIPE = open(PIPE_TO_AUDACITY, 'w')
    print("-- File to write to has been opened")
    FROMPIPE = open(PIPE_FROM_AUDACITY, 'r')
    print("-- File to read from has now been opened too\r\n")


    #here we are going to make the functions that react with audacity
    def send_command(command):
        """Send a command to Audacity"""
        print("Send: -> "+command)
        TOPIPE.write(command + EOL)
        TOPIPE.flush()

    def get_response():
        """Get response from Audacity"""
        line = FROMPIPE.readline()
        result = ""
        while True:
            result += line
            line = FROMPIPE.readline()
            if line == '\n':
                return result

    def do_command(command):
        """Do the command and return the response"""
        send_command(command)
        #time.sleep(0.1) might be required on slow machines
        response = get_response()
        print("Recieved: <- " + response)
        return response

    #now we make our funcs to actually do shit - we are connected now bb

    def import_track(filename):
        """Import track."""
        do_command(f"Import2: Filename={os.path.join(PATH, filename + '.wav')}")
        #do_command("Select: Track=0")
        #do_command("SelTrackStartToEnd")
        #do_command("Select: Region")
        do_command("SetLeftSelection") # - > looking for a way to set an input through python
        do_command("SetRightSelection")
        do_command("Trim")
        
        #find the length
        #clipsinfo = do_command("GetInfo: Type=Clips")
        #lipsinfo = clipsinfo[:clipsinfo.rfind('BatchCommand finished: OK')]
        #clips = json.loads(clipsinfo)
        #duration = clips[0]['end'] - clips[0]['start']
        #time.sleep(duration + 0.1)

    def quick_test():
        """Quick test to ensure no pipe burst"""
        do_command('Help: CommandName=Help')

    quick_test()
    import_track(INFILE)


if __name__ == '__main__':
    import_method(PATH=PATH_HERE, INFILE=INFILE_HERE)