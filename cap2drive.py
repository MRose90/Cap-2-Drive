import os
import tempfile
import shutil
import sys
import pythoncom
from PIL import ImageGrab
from pyHook import HookManager
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Google Drive folder name
folder = 'Cap-to-Drive'
# Log in and get access to write to Google Drive
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

# Temp local directory to store pictures
directory = tempfile.gettempdir() + "/cap2drive"
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    # Deletes the folder and all its contents before recreating the folder
    shutil.rmtree(directory)
    os.makedirs(directory)

# Only create the folder on Google Drive if it doesn't exist
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
created = False
for file1 in file_list:
    if file1['title'] == folder:
        created = True
if not created:
    folder_metadata = {'title': folder, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
# Get the folder id
for file1 in file_list:
    if file1['title'] == folder:
        fid = file1['id']


def pressed(event):
    # 44 = Print Screen
    # Moves screenshot to Google Drive
    if event.KeyID == 44:
        # Copy the image from the clipboard
        im = ImageGrab.grab()
        fname = datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.jpeg'
        path = os.path.join(directory, fname)
        # Save the image in the temp directory
        im.save(path, 'JPEG')
        # Upload the file to Google Drive in the folder with a title of the date
        f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}], 'title': datetime.now().strftime("%y-%m-%d")+'.jpeg'})
        f.SetContentFile(path)
        f.Upload()
    # 27 = Escape
    # Cleans up the temp folder and exists
    if event.KeyID == 27:
        shutil.rmtree(directory)
        sys.exit()


# Create a hook manager
hm = HookManager()
# Watch for all keyboard events
hm.KeyDown = pressed
# Set the hook
hm.HookKeyboard()
# Wait forever (Exits on Escape)
pythoncom.PumpMessages()
