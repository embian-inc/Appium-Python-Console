#-*- coding: utf-8 -*-
import os, sys
from os.path import expanduser

##################################################################
# PLEASE DO NOT CHANGE THIS SECTION. INSTEAD, USE SYMLYNK
#  use  your personal directory. use symlink!
##################################################################
PROJECT_ROOT_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
DOC_SAVE_DIR = os.path.join(PROJECT_ROOT_PATH, 'doc_file')
APK_FILE_DIR = os.path.join(PROJECT_ROOT_PATH, 'apk_files')


##################################################################
# Only Change following line (apk file name)
# Apk File's location is under the APK_FILE_DIR ('/RootProject/apk_files')
##################################################################
# APK_FILE_NAME = 'com.abc.app.apk'
# APK_FILE_NAME = 'embian.only.apk'
APK_FILE_NAME = 'bbc.mobile.news.ww.apk'


##################################################################
# DO NOT CHANGE FOLLOWING LINES WHEN THERE ARE ONLY ONE DEVICE
# following two arguments are automatically overrided
# when there is only one device attached to your pc
##################################################################
PLATFORM_NAME = 'Android'
DEVICE_NAME = 'Device UDID'
PLATFORM_VERSION = 'Device Platform Version (ex. 8, 8.1, 9, etc...)'
