# Appium-Python-Console

[TOC]


APC(Appium Python Console) is a python port of famous ARC(Appium Ruby Console), which
provides easy to use interactive REPL-scripting environment for Android GUI test
automation.  (Note: Current version of APC doesn't support iOS yet.)

If you want to test your Android App without user interaction but with python scripting,
now it can be done easily with APC. With APC, you can not only automate the sequence of
GUI operations such as pressing image button or entering specific texts, but also  
can examine DOM XML elements of App interactively. Thus it makes debugging or stepwise testing
so much easier in interactive session.


## 1. Install Appium-Python-Console
### 번역본 [Korean](https://github.com/embian-inc/Appium-Python-Console/blob/master/README_ko.md)

In order to install Appium,  Oracle-Java8-Installer, Android-SDK, Node.js, NPM must be installed in advance,
and your $PATH environment must be properly configured.

If you haven't done so, please jump to "[Appium Setup Manual](https://github.com/embian-inc/Appium-Python-Console/blob/master/README-AppiumSetup.md)" instruction and do that first and come back here.

Python Version : 2.7 require

##### 1) Download APC source into your PC

###### git clone following link.

```
# Git Clone
$ git clone git@github.com:embian-inc/Appium-Python-Console.git

$ cd Appium-Python-Console
```

##### 2) Python Virtualenv Setting

###### We always recommend python virtual environment.

```
# make virtualenv
$ virtualenv venv

# activate virtualenv
# (venv)$ 						// virtualenv is activated prompt
$ . venv/bin/activate

# deactivate
(venv)$ deactivate

```

##### 3) pip install -r requirements.txt

###### Above will install any dependant python modules for APC.


```
$ pip install -r requirements.txt
```

##### 4) Connect your PC and your Android Phone with USB cable

###### Go Android Settings> and turn on Developer Options>.  (Please refer to your smart phone manual.)

```
# check the connected device
$ adb devices

List of devices attached
	7387d0d19904	device # ok
```

##### 5) Edit config.py

###### Please change 5 env settings in <your APC>/app/config.py



###### DEVICE_NAME : your smartphone device id, issuing 'adb devices', i.e.  "abd3fe8f8fb3"
###### PLATFORM_VERSION : android platform version,  i.e.  "7.0" for android 7.0
###### DOC_SAVE_DIR : temporary directory path for saving captured XML, HTML, screenshot images, i.e. "/tmp"
###### APK_FILE_DIR : your app binary directory (.apk) path, i.e.  "/home/john/apks"
###### APK_FILE_NAME : your app binary filename in APK_FILE_DIR path, "myAndroidApp.apk"

```
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
##################################################################
APK_FILE_NAME = 'your_apk_file_name.apk'


##################################################################
# DO NOT CHANGE FOLLOWING LINES WHEN THERE ARE ONLY ONE DEVICE
# following two arguments are automatically overrided
# when there is only one device attached to your pc
##################################################################
PLATFORM_NAME = 'Android'
DEVICE_NAME = '7387d0d19904'
PLATFORM_VERSION = '6.0'

```



###### 6) Run Appium for first time.
```
# Start Appium
$ appium &

# If you see following messages, Appium started successfully.
[Appium] Welcome to Appium v1.6.5
[Ap﻿pium] Appium REST http interface listener started on 0.0.0.0:4723

```

###### 7) Now Start your APC from terminal

```
$ python main.py
```



## 2. APC(Appium-Python-Console) Methods

| Name |
|------|
| ```help()```|
| ```clear()```|
| ```exit()```|
| ```page()```|
| ```action_table()```|
| ```manual_test(mode='h')```|
| ```methods()```|
| ```methods(num)```|
| ```driver```|



* ```help() ``` : Help. Print all available APC commands and methods
* ```clear()``` : Clear Console.  (Similar to 'clear' command in terminal)
* ```exit()``` : Terminate APC.
* ```page()``` : Print XML of current mobile page.  It prints DOM of current pages showing Resource-id, Content-desc, Text, Action(Clickable, Scrollable)
  * Columns includes: classname, resource_id, content-desc, text, bounds, (Clickable), (Scrollable)
* ```action_table()``` : Print action table of current page.  Action table is simplified view of current XML where row in the table represents only actionable XML element
	* Usage
  	* action_table() - Print "Class, Resource-id, Content-desc, Text, Bounds, Action Type, Context" columns
  	* action_table('d') - Print above columns with Xpath.

* ```manual_test(mode='h')``` : Enter manual test mode, where you can interact with APC with simple-and-guided command.
  * mode='n' - Action table view is created by UIAutomator only [Default]
  * mode='h' - Action table view is created by both of UIAutomator and Chromedriver (Note: Good for webview)

* ```methods()``` : List python methods of WebDriver
* ```methods(num)``` : View detailed information of designed method with key='num'  
  * Usage
  	* methods(94)

* ```driver``` : WebDriver Object
  * Usage
    * driver.contexts
    * driver.find_element_by_id('RESOURCE_ID')

## 3. Manual Test Mode Usage

1)	During Manul Test Mode, clickable/do-able actions in current page is listed as each row in the Action Table List.   
2)	If you want to execute the specific action in Action Table List, you can enter the row ID number.
3)	The row ID entered is action without additional input (such as button press), it execute the action by sending "button-pressed event". Otherwise,
if the row ID indicates "edittext", it immmediately asks you to type additional input and then proceeds to finish that action.
4)	When the action finishes, it refresh the page automatically, and repeat to step 1.
