#-*- coding: utf-8 -*-

import unittest, time, sys, os, re, imp, glob, subprocess, platform, code, codecs, traceback, pydoc, pprint, inspect, types
import driver_setup, ko
import native_manager, webview_manager

from driver_methods import METHODS
from code_setting import PS1LineCounter, PS2LineCounter
from appium import webdriver
from desired_capabilities import get_desired_capabilities
from command_runner import CommandRunner
from modules.action_collector import ActionCollector
from bs4 import BeautifulSoup
from apptestai_modules.utils.rect import Bounds, Point

class AppiumPythonConsole(unittest.TestCase):
    apk_filename = ''
    apk_file_dir = ''
    doc_save_dir = ''
    js_script = ''
    page_contexts = None
    now_context_num = 0
    adb_cmd = 'adb'
    RE_PARSER_METHODS = re.compile(r'([^\']*)\((.*)\)')

    # #######################################################
    # 1. Set Up : set Config & Desired Capabilities
    def setUp(self):
        # Driver Set Up
        driver_setup.setUp(self)
        # CommandRunner
        self.command_runner = CommandRunner()
        # Action Collector
        self.action_collector = ActionCollector(self)

    # Tear Down
    def tearDown(self):
        self.driver.quit()

    # Test_
    def test_manual(self):
        self.finish = True
        self.cmd = {
            'help': self._help,
            'clear': self._clear,
            'exit': self._exit,
            'pprint': pprint.pprint,
            'manual_test': self._manual_test,
            'page': self._page,
            'action_table': self._capable_action_table,
            'methods': self._methods,
            'driver': self.driver
        }
        self._rlcomplete(self.cmd)
        try:
            sys.ps1 = PS1LineCounter()
            sys.ps2 = PS2LineCounter()
            code.interact(ko.APC_BANNER, readfunc=self._read_func(), local = self.cmd)
        except SystemExit:
            self.finish = True
            print "Terminate APC.."

    # Code.interact's readfunc
    #   Write the '--mode=m' option on executing main.py
    #   if you want to start Manual Test Mode
    def _read_func(self):
        if self.mode == 'Manual_Test' or self.mode == 'dev':
            return self._manual_test()
        else:
            return None

    # HELP Command
    def _help(self):
        print ko.HELP_MSG

    # Clear Console Command
    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # APC Terminate Command
    def _exit(self):
        self.finish = True
        raise SystemExit
    # Change Manual Test Mode Command
    def _manual_test(self, mode='h'):
        self.finish = False
        self.driver.switch_to.context('NATIVE_APP')
        self.native_only = False if mode is 'h' else True
        try:
            while(not self.finish):
                self.finish = self.collect_actions()
        except:
            print traceback.format_exc()

    # Page Command
    def _page(self, cond=None):
        orig_c = self.set_context_to_native()
        xml = self.driver.page_source
        soup = BeautifulSoup(xml, "xml", from_encoding='utf-8')

        els = soup.find_all(self.has_id_desc_bounds_text)
        for e in els:
            if str(e.attrs['class']) is not '':
                print "\n\001\033[4;32m\002%s\001\033[0m\002" % e.attrs["class"]
            if str(e.attrs['resource-id']) is not '':
                print "  id: %s" % e.attrs["resource-id"]
            if str(e.attrs['content-desc']) is not '':
                print "  desc: %s" % e.attrs["content-desc"]
            if str(e.attrs['text']) is not '':
                print "  text: %s" % e.attrs["text"]
            if str(e.attrs['bounds']) is not '':
                print "  bounds: %s" % e.attrs["bounds"]
            if str(e.attrs['clickable']) == 'true':
                print "  \001\033[90m\002clickable: %s\001\033[0m\002" % e.attrs["clickable"]
            if str(e.attrs['scrollable']) == 'true':
                print "  \001\033[90m\002scrollable: %s\001\033[0m\002" % e.attrs["scrollable"]
        print '\n'

        self.restore_context(orig_c)

    # Check has attribute resource_id or content-desc or text or Bounds ( For Page Command )
    def has_id_desc_bounds_text(self, tag):
        return tag.has_attr('class') and (tag.has_attr('resource-id') or tag.has_attr('content-desc') or tag.has_attr('text') or tag.has_attr('bounds'))

    # Capable action Table Display command
    def _capable_action_table(self, detail = None):
        orig_c = self.set_context_to_native()
        self.native_only = True
        data = self.get_pagedata()
        self.command_runner.print_action_table(data, detail=detail)
        self.restore_context(orig_c)

    # Appium Driver's Methods display Command
    def _methods(self, item=None):
        idx = 0
        print '\n'
        if item is not None:
            name, args, usage = self.get_methods_info(METHODS[item])
            print "[%3d] \001\033[35m\002%s\001\033[0m\002%s" % (item, name, args)
            if "Desc" in METHODS[item].keys():
                print "\n      Desc :"
                for d in METHODS[item]["Desc"]:
                    print "        %s" % d
            if "Args" in METHODS[item].keys():
                print "\n      Args :"
                for key,value in METHODS[item]["Args"].items():
                    print "        %s : %s" % (key, value)
            if "Usage" in METHODS[item].keys():
                print "\n      Usage :"
                print "        %s" % (METHODS[item]["Usage"])
        else:
            for m in METHODS:
                name, args, usage = self.get_methods_info(m)
                print "[%3d] \001\033[35m\002%40s\001\033[0m\002%s" % (idx, name, args)
                idx = idx + 1
        print '\n'

    def get_methods_info(self, methods):
        name = ""
        args = ""
        usage = ""
        if "Name" in methods:
            m = methods["Name"]
            if self.RE_PARSER_METHODS.match(m):
                name = self.RE_PARSER_METHODS.match(m).group(1)
                args = '(' + self.RE_PARSER_METHODS.match(m).group(2) + ')'
            else:
                name = m
        if "Usage" in methods:
            usage = methods["Usage"]

        return name,args,usage

    def set_context_to_native(self):
        orig_c = self.driver.context
        print 'Current Context is "%s"' % orig_c
        if orig_c != 'NATIVE_APP':
            print 'Switch to "NATIVE_APP" Context'
            self.driver.switch_to.context('NATIVE_APP')
        return orig_c

    def restore_context(self, orig_c):
        if orig_c != 'NATIVE_APP':
            print 'Switch to "%s" Context' % orig_c
            self.driver.switch_to.context(orig_c)

    def _rlcomplete(self, param):
        try:
            import readline
        except ImportError:
            print "Module readline not available."
        else:
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(param).complete)
            readline.parse_and_bind("tab: complete")
            readline.parse_and_bind("bind ^I rl_complete") # for Mac OS X


    # ######################## Manual Test Mode ###############################
    def collect_actions(self):
        data = self.get_pagedata()
        self.command_runner.print_action_table(data, mode=self.mode)
        if self.mode == 'dev':
            self.command_runner.print_action_group_table(data)
        return self.command_runner.do_command(data)

    def get_pagedata(self, screen_id=None):
        with_webview = True
        if not screen_id :
            screen_id = self.command_runner.screen_id

        # Get Current Screen's Contexts
        self.page_contexts = self.driver.contexts

        # Check Native App | Hybrid App
        # Context's len is 1 : Only Native App
        # Context's len is over 1 : Hybrid App
        if self.native_only or len(self.page_contexts) <= 1:
            with_webview = False

        # init Now Context for NATIVE_CONTEXT
        if self.now_context_num != 0:
            self.driver.switch_to.context(self.page_contexts[0])
            self.now_context_num = 0

        # Save Doc files (XML, Screenshot)
        xml = self.driver.page_source
        # xml = self.xml_doc_save()
        # self.screen_shot_save()

        webview_elements = []
        if with_webview:
            webviews = self.find_webview(self.page_contexts, xml)
            idx = 1
            for w in webviews:
                elements = self.get_webview_elements(w, idx, xml)
                webview_elements = webview_elements + elements
                idx = idx + 1

        clean_xml = native_manager.to_clean_xml(xml, without_webview=with_webview)
        return self.action_collector.pagedata(clean_xml, webview_elements=webview_elements, screen_id=screen_id)

    def find_webview(self, contexts, xml):
        webviews = []
        if len(self.get_enable_webview_list(xml)) == 0: return webviews
        for c in contexts:
            for p in self.package_name:
                if 'WEBVIEW' in c and p in c: webviews.append(c)
        return webviews

    def get_enable_webview_list(self, xml):
        soup = BeautifulSoup(xml, "xml", from_encoding='utf-8')

        webviews = soup.find_all('android.webkit.WebView')
        enabled_webviews = []
        package_names = []
        for w in webviews:
            if len(w.find_all('android.webkit.WebView')): continue
            if w['focused'] is False: continue
            for ew in enabled_webviews[:]:
                wb = Bounds.to_bounds(w['bounds'])
                ewb = Bounds.to_bounds(ew['bounds'])
                if wb.relative_pos(ewb) == 5: enabled_webviews.remove(ew)
            enabled_webviews.append(w)
            package_names.append(w['package'])

        self.package_name = list(set(package_names))
        return enabled_webviews

    def get_webview_elements(self, w, idx, xml):
        if self.now_context_num != idx:
            self.driver.switch_to.context(self.page_contexts[idx])
            self.now_context_num = idx

        self.driver.switch_to.context(self.page_contexts[idx])
        self.now_context_num = idx
        # self.html_doc_save()

        actions, elements = webview_manager.get_elements(self.driver, self.page_contexts[idx])
        webview_list = self.get_enable_webview_list(xml)
        actions = self.matching_actions(actions, webview_list)
        elements = self.matching_actions(elements, webview_list)
        return actions + elements

    # Convert Bounds from Webview to Native
    def convert_bounds(self, webview, h_w, h_h, bounds):
        w_bounds = Bounds.to_bounds(webview['bounds'])
        h_bounds = Bounds.to_bounds(bounds)
        r_w = w_bounds.p2.x - w_bounds.p1.x
        r_h = w_bounds.p2.y - w_bounds.p1.y

        x1 = r_w * h_bounds.p1.x / h_w + w_bounds.p1.x;
        x2 = r_w * h_bounds.p2.x / h_w + w_bounds.p1.x;
        y1 = r_h * h_bounds.p1.y / h_h + w_bounds.p1.y;
        y2 = r_h * h_bounds.p2.y / h_h + w_bounds.p1.y;

        new_bounds = Bounds(Point(x1,y1), Point(x2,y2))
        return new_bounds

    def matching_actions(self, action_group, wlist):
        max_avg = 0
        max_actions = action_group[0]
        for actions in action_group:
            for w in wlist:
                cnt = 0
                for a in actions['actions']:
                    b = self.convert_bounds(w, actions['window_width'], actions['window_height'], a['bounds'])
                    #ADDED BY MO: 보정된 bounds로 교체
                    a['web_bounds'] = a['bounds']
                    a['bounds'] = str(b)
                    if len(w.find_all(attrs={'bounds': b})):
                        cnt = cnt + 1
                if len(actions['actions']) > 0:
                    avg = int(float(cnt) / len(actions['actions']) * 100)
                    # print '@@@@@@@@ AVG:', avg
                    if avg > max_avg:
                        max_avg = avg
                        max_actions = actions

        key = max_actions['key']
        self.driver.switch_to_window(key)
        return max_actions['actions']

    ##### Doc Save (XML, ScreenShot, Html) ####
    def screen_shot_save(self):
        filename = '%s.png' % (self.command_runner.screen_id)
        png_filename = os.path.join(self.doc_save_dir, filename)

        self.driver.save_screenshot(png_filename)
        print '# Screen Shot Save OK'

    def xml_doc_save(self):
        filename = '%s.xml' % (self.command_runner.screen_id)
        xml_filename = os.path.join(self.doc_save_dir, filename)
        xml = ''
        with codecs.open(xml_filename, 'w', 'utf-8') as xml_file:
            xml = self.driver.page_source
            xml_file.write(xml)

        print '# XML Save OK'
        return xml

    def html_doc_save(self):
        filename = '%s.html' % (self.command_runner.screen_id)
        html_filename = os.path.join(self.doc_save_dir, filename)
        with codecs.open(html_filename, 'w', 'utf-8') as html_file:
            html_file.write(self.driver.page_source)

        print '# HTML Save OK'
