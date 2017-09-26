# Appium-Python-Console

[TOC]

## [APC](https://embian.com/apc.html)

Appium의 Python Client를 사용하여 테스트 스크립트를 작성하는 사용자들을 위한 콘솔 프로그램입니다.
본 Console은 Android 전용이며 IOS 관련 기능은 지원 하지 않습니다.
본 Console을 통해 Python Client의 여러 Methods들을 직접 테스트 해보실 수 있습니다.


## 1. Install Appium-Python-Console

Appium 설치를 위해서는 Oracle-Java8-Installer, Android-SDK, Node.js, NPM 의 설치 및 PATH설정이 선행되어 있어야 합니다.
위 항목이 아직 설치가 안되어 있다면 [Appium Setup Manual](https://github.com/embian-inc/Appium-Python-Console/blob/master/README_ko-AppiumSetup.md)을 통해 설치를 완료한 뒤 다음을 진행해 주시기 바랍니다.

Python 2.7 version을 이용해 주시기 바랍니다.

##### 1) Git Clone 및 Appium-Python-Console폴더로 이동

###### 아래 링크에 있는 APC Git Repository를 복제 합니다.

```
# Git 복제
$ git clone git@github.com:embian-inc/Appium-Python-Console.git

# APC 폴더로 이동
$ cd Appium-Python-Console
```

##### 2) Virtualenv(가상환경) Setting

###### Virtualenv 환경을 구성할 것을 권장합니다.

```
# 가상환경(venv) 생성
$ virtualenv venv

# 가상환경 활성화
# (venv)$				//가상환경 활성화 상태의 Prompt
$ . venv/bin/activate

# 비활성화
(venv)$ deactivate

```

##### 3) pip를 통한 requirements install

###### requirements.txt에 미리 지정되어 있는 의존성 패키지를 설치해 주세요.


```
$ pip install -r requirements.txt
```

##### 4) PC 에 Mobile Device 연결

###### 모바일 디바이스는 개발자옵션이 활성화 되어 있어야 됩니다.

```
# 디바이스 연결상태 확인
$ adb devices

List of devices attached
	7387d0d19904	device # ok
```

##### 5) Config 파일 Setting

###### Appium-Python-Console/app/config.py 파일을 열어 아래 5개 항목을 수정해 줍니다.

###### DEVICE_NAME : adb devices 를 통해 출력된 Device 고유번호 (혹은 이름)
###### PLATFORM_VERSION : 연결된 Device의 Android 플랫폼 버전
###### DOC_SAVE_DIR : APC의 manual test mode에서 수집된 XML, HTML, Screen Shot 파일이 저장 될 Directory 경로
###### APK_FILE_DIR : APC (Appium-Python-Console) 실행 시 Device에서 실행될 APK 파일이 PC에 위치한 경로
###### APK_FILE_NAME : APK_FILE_DIR 경로에 위치해 있는 실행시킬 APK 파일의 이름

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



###### 6) appium 실행
```
# appium 실행
$ appium &

# 아래와 같은 메세지가 출력 되면 Appium 실행 완료
[Appium] Welcome to Appium v1.6.5
[Ap﻿pium] Appium REST http interface listener started on 0.0.0.0:4723

```

###### 7) Appium-Python-Console 실행

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



* ```help() ``` : 도움말. APC Command Methods 목록 출력
* ```clear()``` : Console Clear ( terminal의 clear 같은 기능 )
* ```exit()``` : APC 종료
* ```page()``` : 현재 페이지에서 Resource-id, Content-desc, Text, Action(Clickable, Scrollable) 값이 있는 요소들의 정보 출력
  * 출력 정보 : class명, resource_id, content-desc, text, bounds, (Clickable), (Scrollable)
* ```action_table()``` : 현재 페이지에서 Action 수행이 가능한 Element의 List를 Table형식으로 제공
	* 사용법
  	* action_table() - Class, Resource-id, Content-desc, Text, Bounds, Action Type, Context 출력
  	* action_table('d') - 위 항목에 추가로 Xpath를 함께 출력

* ```manual_test(mode='h')``` : 별도의 Test Script 작성없이 사용자와의 Interaction을 통해 간단한 test를 진행해 볼 수 있는 모드
  * mode='n' - UIAutomator를 통해 수행가능한 Action 정보 추출 [Default]
  * mode='h' - UIAutomator와 Chromedriver를 통해 수행가능한 Action 정보 추출

* ```methods()``` : Python Client를 통해 사용할 수 있는 WebDriver Methods 리스트 출력
* ```methods(num)``` : methods()를 통해 출력된 리스트 중 특정 번호에 해당하는 Method의 상세 정보 출력
  * 사용법
  	* methods(94)

* ```driver``` : WebDriver Object
  * 사용법
    * driver.contexts
    * driver.find_element_by_id('RESOURCE_ID')

## 3. Manual Test Mode Usage

1)	Manual Test Mode가 실행되면 App의 현재 페이지 에서 수행 가능한 Elements의 목록이 Action List Table로 출력 됩니다.
2)	Action Table List에 표시된 정보를 보고 액션을 수행하길 원하는 Table row의 번호를 입력 합니다.
3)	입력한 번호의 Action이 Input이 아닌 경우는 바로 액션을 수행하게 되고, Input 일 경우는 Input value를 한번더 입력하면 해당 액션을 수행하게 됩니다.
4)	수행이 완료 되면 다시 Step 1 부터 진행되게 됩니다.
