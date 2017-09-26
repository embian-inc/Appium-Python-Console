#-*- coding: utf-8 -*-

# Code Interact Banner
APC_BANNER = """
********************************************************************************************************************
*                                                                                                                  *
*   APC(Appium Python Console) is a python port of famous ARC(Appium Ruby Console), which                          *
*   provides easy to use interactive REPL-scripting environment for Android GUI test                               *
*   automation.  (Note: Current version of APC doesn't support iOS yet.)                                           *
*                                                                                                                  *
*   If you want to test your Android App without user interaction but with python scripting,                       *
*   now it can be done easily with APC. With APC, you can not only automate the sequence of                        *
*   GUI operations such as pressing image button or entering specific texts, but also                              *
*   can examine DOM XML elements of App interactively. Thus it makes debugging or stepwise testing                 *
*   so much easier in interactive session.                                                                         *
*                                                                                                                  *
*   To understand what APC can do, you can glance through the console commands it provides.                        *
*   For information about the console command method, type "help()".                                               *
*   Also, if you want to check the available Appium's native python client method including Appium and WebDriver,  *
*   you can check through "methods()".  To exit the console, type ctrl -d or "exit ()".                            *
*                                                                                                                  *
********************************************************************************************************************\n
Welcome Appium Python Console(APC) !\n
"""


# APC Mode Help
HELP_MSG = """

** HELP ***

 help()                  : Help. Print all available APC commands and methods
 clear()                 : Clear Console.  (Similar to 'clear' command in terminal)
 exit()                  : Terminate Console Program

 page()                  : Print XML of current mobile page.
                           It prints DOM of current pages showing Resource-id, Content-desc, Text, Action(Clickable, Scrollable)
 action_table()          : Print action table of current page.
                           Action table is simplified view of current XML where row in the table represents only actionable XML element
    Usage :
        action_table() - Print "Class, Resource-id, Content-desc, Text, Bounds, Action Type, Context" columns
        action_table('d') - Print above columns with Xpath.

 manual_test(mode='h')   : Enter manual test mode, where you can interact with APC with simple-and-guided command.
        mode='n' - Action table view is created by UIAutomator only [Default]
        mode='h' - Action table view is created by both of UIAutomator and Chromedriver (Note: Good for webview)

 methods()               : List python methods of WebDriver
 methods(num)            : View detailed information of designed method with key='num'
    Usage :
        methods(42)

 driver                  : WebDriver Object.
    Usage :
        driver.<Appium Driver Methods>
        driver.contexts
        driver.find_element_by_id( RESOURCE_ID )

"""

command = {
    'HELP'                  : { 'cmd': ['help', 'h'], 'desc': 'Help. Print all available Manual Test Mode commands' },
    'PAGE'                  : { 'cmd': ['page_source', 'p'], 'desc': 'Appium WebDriver\'s page_source' },
    'DETAIL'                : { 'cmd': ['detail', 'd'], 'desc': 'Print Action Table with Xpath' },
    'BACK'                  : { 'cmd': ['back', 'b'], 'desc': 'Mobile Back Button' },
    'REFRESH'               : { 'cmd': ['refresh', 'r'], 'desc': 'Retry ' },
    'SCROLL_UP'             : { 'cmd': ['sup', 'scrollup', 'up'], 'desc': 'Scroll UP' },
    'SCROLL_DOWN'           : { 'cmd': ['sdown', 'scrolldown', 'down'], 'desc': 'Scroll Down'},
    'SAVE_ALL'              : { 'cmd': ['save_all'], 'desc': 'Save All Files (XML, HTML, ScreenShot Image) of Current page' },
    'XML'                   : { 'cmd': ['xml_save'], 'desc': 'Save XML on Current Page' },
    'HTML'                  : { 'cmd': ['html_save'], 'desc': 'Save HTML on Current Page' },
    'SCREENSHOT'            : { 'cmd': ['screenshot_save', 'ss_save'], 'desc': 'Save Screenshot Image on Current Page' },
    'EXIT'                  : { 'cmd': ['exit', 'quit', 'q'], 'desc': 'Terminate Manual Test Mode and Return to APC Mode' }
}
