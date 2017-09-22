#-*- coding: utf-8 -*-

from os.path import expanduser

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

HOME = expanduser("~")

##################################################################
# PLEASE DO NOT CHANGE THIS SECTION. INSTEAD, USE SYMLYNK
#  use  your personal directory. use symlink!
##################################################################
DOC_SAVE_DIR = HOME + '/Documents/doc_file'
APK_FILE_DIR = HOME + '/Downloads/webview_apps/'

##################################################################
# DO NOT CHANGE FOLLOWING LINES WHEN THERE ARE ONLY ONE DEVICE
# following two arguments are automatically overrided
# when there is only one device attached to your pc
##################################################################

# PLATFORM_NAME = 'Android'
# DEVICE_NAME = '7387d0d19904'
# PLATFORM_VERSION = '6.0'

PLATFORM_NAME = 'Android'
DEVICE_NAME = '7387d0d19904'
PLATFORM_VERSION = '7.1'

##################################################################
# Only Change following line (apk file name)
##################################################################
# APK_FILE_NAME = 'com.abc.app.apk'
APK_FILE_NAME = 'findjob.apk'
