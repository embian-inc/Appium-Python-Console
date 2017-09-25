#-*- coding: utf-8 -*-

# Code Interact Banner
APC_BANNER = u"""
************************************************************************************************************
*                                                                                                          *
*   Appium의 Python Client를 사용하여 테스트 스크립트를 작성하는 사용자들을 위한 콘솔 프로그램입니다.      *
*   본 Console은 Android 전용이며 IOS 관련 기능은 지원 하지않습니다.                                       *
*   본 Console을 통해 Python Client의 여러 Methods들을 직접 테스트 해보실 수 있습니다.                     *
*                                                                                                          *
*   콘솔 내부 명령 메소드에 대한 정보는 "help()" 를 입력해 주세요.                                         *
*   사용 가능한 Python Client의 메소드 정보를 보시길 원하시면 "methods()"를 입력해 주세요.                 *
*   콘솔의 종료를 원하실 경우 ctrl+d 혹은  "exit()"를 입력해 주세요.                                       *
*                                                                                                          *
************************************************************************************************************\n
Welcome Appium Python Console(APC) !\n
"""


# APC Mode Help
HELP_MSG = u"""

** HELP ***

 help()                  : 도움말. APC Command Methods 목록 출력
 clear()                 : Console Clear (terminal의 clear 같은 기능)
 exit()                  : APC 종료

 page()                  : 현재 페이지에서 Resource-id, Content-desc, Text, Action(Clickable, Scrollable) 값이 있는 요소들의 정보 출력
 action_table()          : 현재 페이지에서 Action 수행이 가능한 Element의 List를 Table형식으로 제공
    사용법 :
        action_table() - Class, Resource-id, Content-desc, Text, Bounds, Action Type, Context 출력
        action_table('d') - 위 항목에 추가로 Xpath를 함께 출력

 manual_test(mode='h')   : 별도의 Test Script 작성없이 사용자와의 Interaction을 통해 간단한 test를 진행해 볼 수 있는 모드
        mode='n' - UIAutomator를 통해 수행가능한 Action 정보 추출 [Default]
        mode='h' - UIAutomator와 Chromedriver를 통해 수행가능한 Action 정보 추출

 methods()               : Python Client를 통해 사용할 수 있는 WebDriver Methods 리스트 출력
 methods(num)            : methods()를 통해 출력된 리스트 중 특정 번호에 해당하는 Method의 상세 정보 출력
    사용법 :
        methods(42)

 driver                  : WebDriver Object.
    사용법 :
        driver.<Appium WebDriver Methods>
        driver.contexts
        driver.find_element_by_id('RESOURCE_ID')

"""

command = {
    'HELP'                  : { 'cmd': ['help', 'h'], 'desc': u'도움말' },
    'PAGE'                  : { 'cmd': ['page_source', 'p'], 'desc': u'appium page_source' },
    'DETAIL'                : { 'cmd': ['detail', 'd'], 'desc': u'액션 테이블 상세보기' },
    'BACK'                  : { 'cmd': ['back', 'b'], 'desc': u'뒤로가기' },
    'REFRESH'               : { 'cmd': ['refresh', 'r'], 'desc': u'액션 리스트 다시 가져오기' },
    'SCROLL_UP'             : { 'cmd': ['sup', 'scrollup', 'up'], 'desc': u'스크롤 UP' },
    'SCROLL_DOWN'           : { 'cmd': ['sdown', 'scrolldown', 'down'], 'desc': u'스크롤 Down'},
    'SAVE_ALL'              : { 'cmd': ['save_all'], 'desc': u'현재 페이지의 XML, HTML, Screen Shot 이미지를 파일로 저장하기' },
    'XML'                   : { 'cmd': ['xml_save'], 'desc': u'현재 페이지의 XML을 파일로 저장하기' },
    'HTML'                  : { 'cmd': ['html_save'], 'desc': u'현재 페이지의 HTML을 파일로 저장하기' },
    'SCREENSHOT'            : { 'cmd': ['screenshot_save', 'ss_save'], 'desc': u'현재 페이지의 Screen Shot 이미지를 파일로 저장하기' },
    'EXIT'                  : { 'cmd': ['exit', 'quit', 'q'], 'desc': u'테스트 종료' }
}
