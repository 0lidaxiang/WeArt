# this file should be moved to git server user home directory

# make the parent dir of book folder according to month
#def mkClassedDir():
import datetime
import os

userDir = "lidaxiang"

now = datetime.datetime.now()
yearClassedDirName = "/home/" + userDir + "/" + str(now.year)
monthClassedDirName = yearClassedDirName + "/" + str(now.month)

try:
    if not os.path.exists(yearClassedDirName):
        os.makedirs(yearClassedDirName)
        os.makedirs(monthClassedDirName)
        #return True
    else:
        if not os.path.exists(monthClassedDirName):
            os.makedirs(monthClassedDirName)
            #return True
        #else:
            #return True
except Exception as e:
    print e
    #return False
