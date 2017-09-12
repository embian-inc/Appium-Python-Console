#-*- coding: utf-8 -*-
import unittest, time, os, re, codecs, sys, imp, errno
import native_manager, webview_manager, command
import code

from time import sleep
from appium import webdriver
from terminaltables import AsciiTable
from bs4 import BeautifulSoup

# from owyl_bt import ApptestBT, ApptestBTPageDetect
# from owyl_bt.owyl import blackboard

# monkey patching prettify
_stdin_encoding = sys.stdin.encoding or 'utf-8'
orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)

def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
BeautifulSoup.prettify = prettify

class CommandRunner(object):
    ## for Behavior Tree
    # apptestBTPageDetect = None
    # bb = blackboard.Blackboard('apptest')
    # bb['last_cmd'] = []
    behavior = None

    r_cnt = 0

    def __init__(self):
        self.line_num = 1
        self.screen_id = 'screen-0'
        self.stored_opt = {'detail': False}

    # Print action list table
    def print_action_table(self, pagedata, detail=None, mode=None):
        actions = pagedata['actions'] if 'actions' in pagedata else []
        header = ['No.','WIDGET', 'RESOURCE-ID', 'CONTENT-DESC', 'BOUNDS','ACTION', 'CONTEXT']
        if mode == 'dev':
            header = ['No.', 'DESC', 'LABEL', 'ACTION', 'BOUNDS', 'CONTEXT']

        print '\n'
        table = []
        keys = header[1:-1]
        if self.stored_opt['detail'] or detail == 'd':
            header.append('XPATH')
        table.append(header)

        for cnt, el in enumerate(actions):
            input_type = '-' if el['input-type'] == 'null' else el['input-type']
            # [
            #     '%03d' % cnt,
            #     el['desc'],
            #     el['label'],
            #     el['action'],
            #     el['widget'],
            #     el['resource-id'],
            #     el['bounds'],
            #     el['type']
            # ]
            row = ['%03d' % cnt]
            for key in keys:
                row.append(el[key.lower()])
            row.append(el['type'])

            if self.stored_opt['detail'] or detail == 'd':
                row.append(el['xpath'])
                table.append(row)
            else:
                table.append(row)

        at = AsciiTable(table, title="Action List")
        print at.table
        print '\n'

    # Print action group list table
    def print_action_group_table(self, pagedata):
        action_groups = pagedata['action_groups'] if 'action_groups' in pagedata else []

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
        print '%s' % png_filename

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
        print '%s' % xml_filename

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
        print '%s' % html_filename


    # if result is true, finish test
    def do_command(self, data):
        extra_sleep=0
        print "\n# About Manual Test Command - Enter 'help' or 'h' "

        print '[Current Context : %s]' % data['driver'].context
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

            elif command.is_page_source(choice):
                i = 0
                print "\nChoose Contexts List to bottom:"
                for c in data['contexts']:
                    print "%d. %s" % (i, c)
                    i = i + 1

                c_num = raw_input('\nContexts Number >> ')
                try:
                    num = int(c_num)
                except:
                    return False
                bs4_type = "xml" if data['contexts'][int(c_num)] == 'NATIVE_APP' else "lxml"
                now_context_num = data['now_context_num']
                orig_context = data['contexts'][now_context_num]
                data['driver'].switch_to.context(data['contexts'][int(c_num)])
                soup = BeautifulSoup(data['driver'].page_source, bs4_type, from_encoding='utf-8')
                print '\n'
                print soup.prettify
                print '\n'

                data['driver'].switch_to.context(orig_context)
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
                print 'Terminate Manual Test Mode.\n'
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
