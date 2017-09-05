#-*- coding: utf-8 -*-
import unittest, time, os, re, codecs, sys, imp, errno
from time import sleep
from appium import webdriver
from terminaltables import AsciiTable
import native_manager, webview_manager, command
# from owyl_bt import ApptestBT, ApptestBTPageDetect
# from owyl_bt.owyl import blackboard

from bs4 import BeautifulSoup

import code

# monkey patching prettify

_stdin_encoding = sys.stdin.encoding or 'utf-8'
orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)

def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
BeautifulSoup.prettify = prettify

class CommandRunner(object):
    behavior = None
    # apptestBTPageDetect = None
    # bb = blackboard.Blackboard('apptest')
    # bb['last_cmd'] = []
    r_cnt = 0
    ACTION_DESC_RE = re.compile(r'/alias\:(.*)/pos\:(.*)/widget\:(.*)$')
    ACTION_GROUP_DESC_RE = re.compile(r'/alias\:(.*)/pos\:(.*)$')

    def __init__(self):
        self.line_num = 1
        self.screen_id = 'screen-0'
        self.stored_opt = {'detail': False}

    #show actions
    def print_action_table(self, pagedata):
        actions = pagedata['actions'] if 'actions' in pagedata else []
        action_groups = pagedata['action_groups'] if 'action_groups' in pagedata else []

        print '\n'
        table = []
        header = ['No.', 'DESC', 'LABEL', 'ACTION', 'INPUT-TYPE', 'BOUNDS', 'CONTEXT']
        if self.stored_opt['detail']:
            header.append('XPATH')

        table.append(header)
        for cnt, el in enumerate(actions):
            input_type = '-' if el['input-type'] == 'null' else el['input-type']
            if self.stored_opt['detail']:
                table.append(['%03d' % cnt, el['desc'], el['label'], el['action'], input_type, el['bounds'], el['type'], el['xpath']])
            else:
                table.append(['%03d' % cnt, el['desc'], el['label'], el['action'], input_type, el['bounds'], el['type']])

        at = AsciiTable(table, title="Action List")
        # at.inner_row_border = True
        print at.table


        print '\n'
        table = []
        header = ['TYPE', 'DESC', 'LABEL', 'PRE', 'FINAL']
        table.append(header)
        no = 0
        for group in action_groups:
            table.append( [group.gtype, group.desc, group.label, group.pre_desc, group.final_desc] )
            no = no + 1

        at = AsciiTable(table, title="Action Groups")
        # at.inner_row_border = True
        print at.table
        print '\n'

    def touch_back_btn(self, data):
        if data['now_context_num'] != 0:
            data['driver'].switch_to.context(data['contexts'][0])
            data['now_context_num'] = 0

        data['driver'].press_keycode(4)

    def screen_shot_save(self, data, idx=None):
        if data['now_context_num'] != 0:
            data['driver'].switch_to.context(data['contexts'][0])
            data['now_context_num'] = 0

        filename = '%s.png' % (self.screen_id)
        png_filename = os.path.join(data['doc_save_dir'], filename)

        orig_context = data['driver'].current_context
        if 'WEBVIEW' in orig_context:
            data['driver'].switch_to.context(data['contexts'][0])

        data['driver'].save_screenshot(png_filename)
        data['driver'].switch_to.context(orig_context)
        print '# Screen Shot Save OK'

    def xml_doc_save(self, data, idx=None):
        if data['now_context_num'] != 0:
            data['driver'].switch_to.context(data['contexts'][0])
            data['now_context_num'] = 0;

        filename = '%s.xml' % (self.screen_id)

        xml_filename = os.path.join(data['doc_save_dir'], filename)
        xml = ''
        with codecs.open(xml_filename, 'w', 'utf-8') as xml_file:
            xml = data['driver'].page_source
            xml_file.write(xml)
        print '# XML File Save OK'

    def html_doc_save(self, data, idx=None):
        for c in data['driver'].contexts:
            if 'WEBVIEW' in c:
                if data['contexts'].index(c) != data['now_context_num']:
                    data['driver'].switch_to.context(c)
                    data['now_context_num'] =  data['contexts'].index(c)

                filename = '%s.html' % (self.screen_id)
                html_filename = os.path.join(data['doc_save_dir'], filename)
                with codecs.open(html_filename, 'w', 'utf-8') as html_file:
                    html_file.write(data['driver'].page_source)
        print '# HTML File Save OK'


    # if result is true, finish test
    def do_command(self, data):
        extra_sleep=0
        print ''
        print '# Manual Test Command 정보 - help 또는 h 를 입력하세요.'

        promp = '\n[App-Manual-Test] Input Action Number #%d >> ' % self.line_num

        self.line_num = self.line_num + 1
        self.screen_id = 'screen-' + str(self.line_num)
        choice = raw_input(promp).strip()
        print "Selected Command: %s" % str(choice)

        idx = None
        try:
            idx = int(choice)
        except:
            if command.is_help(choice):
                idx= -1
            elif command.is_apc_mode(choice):
                print 'exit'
                return True

            elif command.is_page_source(choice):
                soup = BeautifulSoup(data['driver'].page_source, "xml")
                print soup.prettify()
                return False

            elif command.is_detail(choice):
                self.stored_opt['detail'] = not self.stored_opt['detail']
                return False

            elif command.is_back(choice):
                self.touch_back_btn(data)
                sleep(1)
                return False

            elif command.is_refresh(choice):
                sleep(1)
                return False

            elif command.is_scroll_up(choice):
                native_manager.scroll(data, 'UP')
                sleep(1)
                return False

            elif command.is_scroll_down(choice):
                native_manager.scroll(data, 'DOWN')
                sleep(1)
                return False

            elif command.is_save_all(choice):
                self.xml_doc_save(data, self.line_num-1)
                self.html_doc_save(data, self.line_num-1)
                self.screen_shot_save(data, self.line_num-1)
                sleep(1)
                idx= -1

            elif command.is_save_xml(choice):
                self.xml_doc_save(data, self.line_num-1)
                sleep(1)
                idx= -1

            elif command.is_save_html(choice):
                self.html_doc_save(data, self.line_num-1)
                sleep(1)
                idx= -1

            elif command.is_save_ss(choice):
                self.screen_shot_save(data, self.line_num-1)
                sleep(1)
                idx= -1

            elif command.is_exit(choice):
                print 'exit'
                return True

            # elif command.is_load(choice):
            #     print 'loading behavior'
            #     self.behavior=behavior._sample_behavior(behavior.aliases)
            #     behavior._print_behavior(self.behavior)
            #     return False

            # elif command.is_explain(choice):
            #     print 'explaining behavior'
            #     behavior._explain_behavior(data)
            #     return False
            #
            # elif command.is_next(choice):
            #     print 'next task'
            #     behavior._print_behavior(self.behavior)
            #     new_task=behavior._next_behavior(data)
            #     if new_task['cmd'] < 0:
            #         return False
            #
            #     # otherwise, just execute with predefined value
            #     idx=new_task['cmd']
            #     extra_sleep=new_task['sleep']
            #     data['actions'][idx]['value']=new_task['edit']

            # elif command.is_bt(choice):
            #     if self.r_cnt > 1:
            #         print "Action does not exist...Terminate apc.py !"
            #         return True
            #     if len(data['actions']) < 1:
            #         self.r_cnt += 1
            #         sleep(3)
            #         return False
            #     self.r_cnt = 0
            #     print '......:: Behavior Tree Recommandation'
            #     self.apptestBTPageDetect = ApptestBTPageDetect.ApptestBTPageDetect(self.bb)
            #     self.bb['page_info'] = data['actions']
            #     results = [x for x in self.apptestBTPageDetect.tree]
            #     if self.bb['recomm_idx'] < 0:
            #         print "Try all possible actions... Reset BT"
            #         return False
            #     else:
            #         idx = self.bb['recomm_idx']
            #         # print 'Behavior Tree Choose Action : %d'% idx
            # elif command.is_empty_bt(choice):
            #     self.bb = blackboard.Blackboard('apptest')
            #     self.bb['last_cmd'] = []
            #     self.apptestBTPageDetect = None
            #     self.r_cnt = 0

            else:
                idx = -1

        if idx < 0:
            self.line_num = self.line_num - 1
            return self.do_command(data)

        if idx >= len(data['actions']):
            print 'Enter the correct number.'
            return self.do_command(data)


        ### do action
        action = data['actions'][idx]
        if action is None:
            print 'Enter the correct number.'
            return False

        if action['type'] == native_manager.NATIVE_CONTEXT:
            native_manager.exec_action(data, idx)
        else:
            webview_manager.exec_action(data, idx)

        sleep(1)
        sleep(extra_sleep)
        return False
