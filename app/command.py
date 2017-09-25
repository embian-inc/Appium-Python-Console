#-*- coding: utf-8 -*-

import sys, ko, en

command = en.command
for v in sys.argv:
    if '-kor' in v:
        self.lang = 'ko-kr'
        command = ko.command

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
    cmd = command['SAVE_ALL']['cmd']
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
