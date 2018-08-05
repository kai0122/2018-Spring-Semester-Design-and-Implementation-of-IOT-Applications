import time
import DAN
import requests
import IDA
import subprocess
import msvcrt          #Windows only
import threading
import os
import pyautogui as pygui
import sys
import random


DAN.profile['dm_name']='KAI_OUT'
DAN.profile['d_name']='kai'
DAN.profile['df_list']=['KAI_OUT0', 'KAI_OUT1', 'KAI_OUT2' ,'KAI_OUT3', 'KAI_OUT4', 'KAI_OUT5', 'KAI_OUT6' ,'KAI_OUT7', 'KAI_OUT8' ,'KAI_OUT_MODE', 'KAI_OUT_IDF']
DAN.device_registration_with_retry('140.113.199.249')


# ifSound
sound = 0

# play Mode
mode = 0

# OPEN EXE
def openPicman():   
    process = subprocess.Popen('./game/picman.exe')
    time.sleep(1)
    #library:pyautogui
    IDA.press('tab')
    IDA.press('enter')
    time.sleep(5)
    IDA.press('right_arrow')


def openDown():
    process = subprocess.Popen('./game/down.exe')
    time.sleep(1)
    IDA.press('enter')
    IDA.press('enter')
    time.sleep(2)
    
    # k.press_key(k.right_key)
    # while 1:
    #     pass


memoryGameIndex = 0
memoryGame = ['left_arrow','right_arrow','up_arrow','down_arrow','enter','5','6','7','8']
def playMemory():
	print ("Play Memory Game: ")
	random.shuffle(memoryGame)
	memoryGameIndex = 0


def shutDown():
	if mode == 1:
		os.system('TASKKILL /F /IM down.exe')
	if mode == 2:
		os.system('TASKKILL /F /IM picman.exe')



def open_ppt():
    cmd=r'.\painting\ppt.ppsx'    #symble 'r' indicates python to recognize the follows as a pure string
    #print(cmd)
    #print(os.path.join('.', 'painting', 'ppt.ppsx')) #path example, is sutiable for multiple OSs.
    while 1:
        str='N'
        while (str!='n'):
            str=msvcrt.getch()    #Windows only
        subprocess.call(cmd.split(), shell=True)

thx=threading.Thread(target=open_ppt)
thx.daemon = True
thx.start()

permission=1
while True:
    try:
        DAN.push('KAI_OUT_IDF', sound)
        if sound == 1:
        	print ("wrong!!!")

    	modeNew=DAN.pull('KAI_OUT_MODE')
        if modeNew != None:
            if modeNew[0] == 0:
                shutDown()
                mode = 0
            if modeNew[0] == 1:
                openDown()
                mode = 1
            if modeNew[0] == 2:
                openPicman()
                mode = 2
            if modeNew[0] == 3:
                playMemory()
                mode = 3


        for odf_name, key in [
                    ('KAI_OUT0', 'left_arrow'),
                    ('KAI_OUT1', 'right_arrow'),
                    ('KAI_OUT2', 'up_arrow'),
                    ('KAI_OUT3', 'down_arrow'),
                    ('KAI_OUT4', 'enter'),
                    ('KAI_OUT5', '5'),
                    ('KAI_OUT6', '6'),
                    ('KAI_OUT7', '7'),
                    ('KAI_OUT8', '8')
                ]:
            tmp = DAN.pull(odf_name)
            if tmp != None and str(tmp[0]) != "0.0" :
                print(odf_name + ' ' + str(tmp[0]))
                if tmp[0] > 0 and permission==1:
	                IDA.press(key)
	                if mode == 3:
	                    if key == memoryGame[memoryGameIndex]:
	                        memoryGameIndex += 1
	                        if memoryGameIndex == 9: sound = 0
	                    else: sound = 1
                else:
                    print ('Permission denied!')

    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError")
        DAN.device_registration_with_retry()


    time.sleep(0.2)
