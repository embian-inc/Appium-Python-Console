#-*- coding: utf-8 -*-

# Code Interact Banner
APC_BANNER_KR = """
************************************************************************************************************
*                                                                                                          *
*   Appium의 Python Client를 사용하여 테스트 스크립트를 작성하는 사용자들을 위한 콘솔 프로그램입니다.         *
*   본 Console은 Android 전용이며 IOS 관련 기능은 지원 하지않습니다.                              *
*   본 Console을 통해 Python Client의 여러 Methods들을 직접 테스트 해보실 수 있습니다.                     *
*                                                                                                          *
*   콘솔 내부 명령 메소드에 대한 정보는 "help()" 를 입력해 주세요.                                               *
*   사용 가능한 Python Client의 메소드 정보를 보시길 원하시면 "methods()"를 입력해 주세요.   *
*   콘솔의 종료를 원하실 경우 ctrl+d 혹은  "exit()"를 입력해 주세요.                                     *
*                                                                                                          *
************************************************************************************************************\n
Welcome Appium Python Console(APC) !\n
"""

# Code Interact Banner
APC_BANNER = """
************************************************************************************************************
*                                                                                                          *
*   A console program for users who write test scripts using the Appium Python Client.                     *
*   This console is for Android only and does not support IOS.                                             *
*   You can test various methods of Python Client directly through this console.                           *
*                                                                                                          *
*   For information about the Console Command method, type "help()".                                       *
*   If you want to see the available Python Client Method information, you can check through "methods()".  *
*   To exit the console, type ctrl -d or "exit ()".                                                        *
*                                                                                                          *
************************************************************************************************************\n
Welcome Appium Python Console(APC) !\n
"""

# APC Mode Help
HELP_MSG = """

** HELP ***

 help()                     : print this message
 clear()                    : Clear Screen for Console
 exit()                     : Terminate Console Program

 page()                     : Clickable Elements Info in current page
 action_table()             : Capable Table for Clickable Elements Info in current Page
     Usage:
         action_table() - Widget name, Resource-id, Content-desc, Bounds, Action, Context
         action_table('d') - with xPath

 manual_test(mode='h|n')    : Change Manual Test Mode
     Args:
         mode='n' - Extract Clickable Elements by only Xml [Default]
         mode='h' - Extract Clickable Elements by Xml and Chromedriver (for Hybrid App or WebApp)
     Usage:
         manual_test() - Default Mode
         manual_test(node='h') - for Hybrid and WebApp Mode


 methods()                  : Available Appium Driver Methods List
 methods(num)               : Specific Appium Driver Methods Desc (num is number of methods lists)

 driver                     : Appium Driver
     usage:
         driver.<Appium Driver Methods>
     example:
         1. driver.contexts
         2. driver.find_element_by_id( RESOURCE_ID )

"""
