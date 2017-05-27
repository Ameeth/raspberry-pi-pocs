from py_irsend import irsend
import time
TATASKY_REMOTE_NAME = 'TATASKY'
LGTV_REMOTE_NAME = 'LG_TV'

def sendKeyStrokes(remoteName, keyStrokes):
    print(keyStrokes)
    irsend.send_once(remoteName, keyStrokes)
    time.sleep(0.1)

def goto_channel(channel_no):
    keyStrokes = []
    for i in channel_no:
        keyCode = 'KEY_'+str(i)
        keyStrokes.append(keyCode)

    keyStrokes.append('KEY_SELECT')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)

def mute_ts():
    keyStrokes = []
    keyStrokes.append('KEY_MUTE')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)

def mute_tv():
    keyStrokes = []
    keyStrokes.append('KEY_MUTE')
    sendKeyStrokes(LGTV_REMOTE_NAME, keyStrokes)

def onoff():
    keyStrokes = []
    keyStrokes.append('KEY_POWER')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)
    sendKeyStrokes(LGTV_REMOTE_NAME, keyStrokes)

def volume_up_ts():
    keyStrokes = []
    keyStrokes.append('KEY_VOLUMEUP')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)

def volume_down_ts():
    keyStrokes = []
    keyStrokes.append('KEY_VOLUMEDOWN')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)

def volume_up_tv():
    keyStrokes = []
    keyStrokes.append('KEY_VOLUMEUP')
    sendKeyStrokes(LGTV_REMOTE_NAME, keyStrokes)

def volume_down_tv():
    keyStrokes = []
    keyStrokes.append('KEY_VOLUMEDOWN')
    sendKeyStrokes(LGTV_REMOTE_NAME, keyStrokes)

def channel_up():
    keyStrokes = []
    keyStrokes.append('KEY_CHANNELUP')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)

def channel_down():
    keyStrokes = []
    keyStrokes.append('KEY_CHANNELDOWN')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)

def go_back():
    keyStrokes = []
    keyStrokes.append('KEY_BACK')
    sendKeyStrokes(TATASKY_REMOTE_NAME, keyStrokes)
