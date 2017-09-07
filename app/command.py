#-*- coding: utf-8 -*-

command = {
    'HELP'                  : { 'cmd': ['help', 'h'], 'desc': '도움말' },
    'PAGE'                  : { 'cmd': ['page_source', 'p'], 'desc': 'appium page_source' },
    'DETAIL'                : { 'cmd': ['detail', 'd'], 'desc': '액션 테이블 상세보기' },
    'BACK'                  : { 'cmd': ['back', 'b'], 'desc': '뒤로가기' },
    'REFRESH'               : { 'cmd': ['refresh', 'r'], 'desc': '액션 리스트 다시 가져오기' },
    'SCROLL_UP'             : { 'cmd': ['sup', 'scrollup', 'up'], 'desc': '스크롤 UP' },
    'SCROLL_DOWN'           : { 'cmd': ['sdown', 'scrolldown', 'down'], 'desc': '스크롤 Down'},
    'SAVE'                  : { 'cmd': ['save', 's', '-save'], 'desc': '현재 페이지의 XML, HTML, Screen Shot 이미지를 파일로 저장하기' },
    'XML'                   : { 'cmd': ['xml'], 'desc': '현재 페이지의 XML을 파일로 저장하기' },
    'HTML'                  : { 'cmd': ['html'], 'desc': '현재 페이지의 HTML을 파일로 저장하기' },
    'SCREENSHOT'            : { 'cmd': ['screenshot', 'ss'], 'desc': '현재 페이지의 Screen Shot 이미지를 파일로 저장하기' },
    'EXIT'                  : { 'cmd': ['exit', 'quit', 'q'], 'desc': '테스트 종료' }
}

bt_command = {
    'LOAD'                  : { 'cmd': ['load','l'], 'desc': 'Behavior 읽어오기' },
    'EXPLAIN'               : { 'cmd': ['exp', 'x'], 'desc' : 'Behavior Task 설명하기' },
    'NEXT'                  : { 'cmd': ['next','n'], 'desc' : '다음 Behavior Task 실행하기' },
    'BT'                    : { 'cmd': ['bt'], 'desc' : 'Jung의 Page에 대한 Behavior Tree 실행하기' },
    'RESETBT'               : { 'cmd': ['rbt'], 'desc' : 'Jung의 Page에 대한 Behavior Tree 실행 리셋하기' }
}

# Help
def is_help( arg):
    cmd = command['HELP']['cmd']
    if arg in cmd:
        for value in command.itervalues():
            print ( '%30s : %s' % (', '.join(value['cmd']), value['desc']) )
        return True
    else:
        return False

def is_page_source( arg):
    cmd = command['PAGE']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# 액션 리스트 상세보기
def is_detail( arg):
    cmd = command['DETAIL']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# Back Button
def is_back( arg):
    cmd = command['BACK']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# 액션 리스트 새로고침
def is_refresh( arg):
    cmd = command['REFRESH']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# Scroll Up action
def is_scroll_up( arg):
    cmd = command['SCROLL_UP']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# Scroll Down Action
def is_scroll_down( arg):
    cmd = command['SCROLL_DOWN']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# 현재 화면의 XML, HTML, Screenshot Image File Save
def is_save_all( arg):
    cmd = command['SAVE']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# 현재 화면의 XML File Save
def is_save_xml( arg):
    cmd = command['XML']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# 현재 화면의 HTML File Save
def is_save_html( arg):
    cmd = command['HTML']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# 현재 화면의 Screenshot Image File Save
def is_save_ss( arg):
    cmd = command['SCREENSHOT']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# 테스트 종료
def is_exit( arg):
    cmd = command['EXIT']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# behavior 읽어오기
def is_load( arg):
    cmd = bt_command['LOAD']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# behavior task 설명하기
def is_explain( arg):
    cmd = bt_command['EXPLAIN']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# behavior task 실행하기
def is_next( arg):
    cmd = bt_command['NEXT']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# behavior tree로 action 실행하기
def is_bt( arg):
    cmd = bt_command['BT']['cmd']
    if arg in cmd:
        return True
    else:
        return False

# behavior tree 실행 reset하기
def is_empty_bt( arg):
    cmd = bt_command['RESETBT']['cmd']
    if arg in cmd:
        return True
    else:
        return False
