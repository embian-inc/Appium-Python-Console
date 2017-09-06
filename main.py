#-*- coding: utf-8 -*-

import traceback, unittest, sys
from app.apc import AppiumPythonConsole
import app.command as command
import app.ko as ko

sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(AppiumPythonConsole)
        unittest.TextTestRunner(verbosity=2).run(suite)
    except:
        print traceback.format_exc()
        pass
