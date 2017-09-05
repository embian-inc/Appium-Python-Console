#-*- coding: utf-8 -*-

import traceback, unittest, sys
from app.apc import ManualTest, AppiumPythonConsole
import app.command as command
import app.ko as ko
# from app.manual_test_with_bt import BTTest

sys.setdefaultencoding('utf-8')

def select_mode():
    promp = "[Python] >> "
    choice = raw_input(promp).strip()

    try:
        idx = int(choice)
        idx = idx - 1
    except:
        ### 종료 Command ###
        if command.is_exit(choice):
            return True
        else:
            idx = -1

    ####### 잘못된 번호 혹은 Command 입력 시 #########
    if idx < 0:
        return select_mode()

    if idx >= len(ko.MENU):
        return select_mode()
    ############################################

    print "Selected Mode: %s" % ko.MENU[ idx ]

    # Mode 0 : Manual Test Mode
    if idx == 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(ManualTest)
        unittest.TextTestRunner(verbosity=2).run(suite)

    # Mode 1 : APC (Appium Python Console) Mode
    if idx == 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(AppiumPythonConsole)
        unittest.TextTestRunner(verbosity=2).run(suite)

    return idx

if __name__ == "__main__":
    # 환영 Msg 및 도움말 사용법
    # print ""
    # print ko.HELP_1

    # Mode 선택 안내 Msg
    # print ko.MSG_1

    # 선택 가능한 Mode 출력
    # for m in ko.MENU:
    #     print "\n\t" + m
    # print ""

    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(AppiumPythonConsole)
        unittest.TextTestRunner(verbosity=2).run(suite)
        # mode = select_mode()
    except:
        print traceback.format_exc()
        pass



    # if mode == 2:
    #     suite = unittest.TestLoader().loadTestsFromTestCase(BTTest)
    #     unittest.TextTestRunner(verbosity=2).run(suite)
