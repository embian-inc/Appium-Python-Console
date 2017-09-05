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
APPIUM_HOME = HOME + '/Documents/appium-1.6.3/'

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
PLATFORM_VERSION = '6.0'

##################################################################
# Only Change following line (apk file name)
##################################################################
#APK_FILE_NAME = 'nl.apk'
#APK_FILE_NAME = 'line.apk'
# APK_FILE_NAME = 'musinsa.apk'

APK_FILE_NAME = 'findjob.apk'

##################################################################
# Appium Desired Capabilities Static Values
##################################################################

AUTO_GRANT_PERMISSIONS = True
ANDROID_INSTALL_TIMEOUT = 360000
AUTOMATION_NAME = 'uiautomator2'
NEW_COMMAND_TIMEOUT = 3600
APP_WAIT_ACTIVITY = '*'
NO_SIGN = True
