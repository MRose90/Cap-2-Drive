from PIL import ImageGrab
from pyHook import HookManager
import pythoncom
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import tempfile
import shutil
import sys


folder = 'Cap-to-Drive'


g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)
tempLoc = tempfile.mkdtemp()
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
created = False
for file1 in file_list:
    if file1['title'] == folder:
        created = True
if not created:
    folder_metadata = {'title': folder, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
for file1 in file_list:
    if file1['title'] == folder:
        fid = file1['id']

def pressed(event):
    if event.KeyID == 44:
        im = ImageGrab.grab()
        fname = datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.jpeg'
        path = os.path.join(tempLoc, fname)
        im.save(path, 'JPEG')
        f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}], 'title': datetime.now().strftime("%y-%m-%d")+'.jpeg'})
        f.SetContentFile(path)
        f.Upload()
        print "Uploaded"
    if event.KeyID == 27:
        shutil.rmtree(tempLoc)
        sys.exit()


# create a hook manager
hm = HookManager()
# watch for all mouse events
hm.KeyDown = pressed
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
