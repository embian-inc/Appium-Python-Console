
import time, os, re, codecs, sys, traceback
from time import sleep, localtime, strftime
from appium import webdriver
from bs4 import BeautifulSoup
from rect import Bounds, Point
# from app.owyl_bt.ActionObject import ActionObject
# from app.owyl_bt.ActionGroupObject import ActionGroupObject
from action_table import ActionTable

#Vitual Appium driver
class VirtualAppiumTestCase(object):
    NATIVE_CONTEXT = 'NATIVE_APP'
    def __init__(self):
        self.driver = self
        self.page_contexts = [self.NATIVE_CONTEXT]
        self.now_context_num = 0
        self.apk_filename = None
        self.apk_file_dir = None
        self.doc_save_dir = None

    @property
    def contexts(self):
        return self.page_contexts

class ActionCollector(object):
    NATIVE_CONTEXT = VirtualAppiumTestCase.NATIVE_CONTEXT
    def __init__(self, appium_testcase=None):
        self.appium_testcase = appium_testcase
        if self.appium_testcase is None:
            self.appium_testcase = VirtualAppiumTestCase()

    @property
    def page_contexts(self):
        return self.appium_testcase.page_contexts

    @property
    def driver(self):
        return self.appium_testcase.driver

    @property
    def now_context_num(self):
        return self.appium_testcase.now_context_num

    @property
    def apk_filename(self):
        return self.appium_testcase.apk_filename

    @property
    def apk_file_dir(self):
        return self.appium_testcase.apk_file_dir

    @property
    def doc_save_dir(self):
        return self.appium_testcase.doc_save_dir


    def pagedata(self, xml, webview_elements=[], behavior=None, screen_id=None):
        action_table, action_groups = ActionTable( xml, webview=webview_elements ).to_table()

        #action_table to actions
        actions = []
        # obj_action_groups = []
        for cnt, action in enumerate(action_table):
            context = self.NATIVE_CONTEXT
            if 'type' in action.element:
                context = action.element['type']
            actions.append({
                'target': action.target,
                'action': action.atype,
                'input-type': action.input_type,
                'bounds': str(action.bounds),
                'xpath': action.xpath,
                'desc': action.desc,
                'label': action.label,
                'type': context,
                'screen_id': screen_id,
                'resource-id': action.resource_id,
                'content-desc': action.content_desc,
                'widget': action.e_class
                # 'obj_actions':ActionObject(cnt,
                #        action.desc,
                #        action.atype,
                #        action.input_type,
                #        action.bounds,
                #        action.label
                #        )
            })

        # for action_group in action_groups:
        #     obj_action_groups.append(
        #         ActionGroupObject(action_group.gtype,
        #                           action_group.desc,
        #                           action_group.label,
        #                           action_group.pre_actions,
        #                           action_group.final_actions
        #       )
        #     )

        data = {
            'actions': actions,
            'action_groups': action_groups,
            'driver': self.driver,
            'contexts': self.page_contexts,
            'now_context_num': self.now_context_num,
            'apk_filename': self.apk_filename,
            'apk_file_dir': self.apk_file_dir,
            'doc_save_dir': self.doc_save_dir,
            'screen_id': screen_id,
            'behavior' : behavior,
            # 'obj_action_groups': obj_action_groups,
        }
        return data
