# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Tag
from modules.rect import Bounds, Point
import traceback

from modules.action_table import ActionTable

from appium.webdriver.common.touch_action import TouchAction
from time import sleep
import sys,os,re, codecs

_stdin_encoding = sys.stdin.encoding or 'utf-8'

NATIVE_CONTEXT = 'NATIVE_APP'

##################### ActionExecutor #######################################################################
class ActionExecutor(object):
    def __init__(self, driver, action, index):
        self.driver = driver
        self.action = action
        self.index = index
        self.action_type = self.action['action']

    def find_element(self):
        elem = None

        if self.action is None:
            return elem

        event = self.action['xpath']
        if event is None:
            return elem

        return self.driver.find_element_by_xpath(event)

    def to_action_info(self):
        return " %03d. %s - %s %s" % (self.index, self.action_type, self.action['desc'], self.action['bounds'])

    # exec actions: 'click|scroll|swipe|input|spinner|checkbox'
    def do_touch(self):
        bounds = Bounds.to_bounds(self.action['bounds'])
        val = bounds.to_touch_val()

        print ( '# Selected Click Action >> %s' % self.to_action_info() )
        print '=' * 80

        touch = TouchAction(self.driver)
        touch.tap(x=val.x, y=val.y).perform()

        return True

    def do_scroll(self):
        bounds = Bounds.to_bounds(self.action['bounds'])
        val = bounds.to_scroll_val()

        print ( '# Selected Scroll Action >> %s' % self.to_action_info() )
        print '=' * 80

        self.driver.swipe(val.p1.x, val.p1.y, val.p2.x, val.p2.y, 3000)
        sleep(1)

        return True

    def do_swipe(self):
        bounds = Bounds.to_bounds(self.action['bounds'])
        val = bounds.to_swipe_val()

        print ( '# Selected Swipe Action >> %s' % self.to_action_info() )
        print '=' * 80

        self.driver.swipe(val.p1.x, val.p1.y, val.p2.x, val.p2.y)
        sleep(1)

        return True

    def do_input(self):
        el = self.find_element()
        if el is None:
            return False

        print ( '# Selected Input Action >> %s' % self.to_action_info() )
        input_val = ""
        if 'value' in self.action and self.action['value'] is not None:
            input_val = self.action['value']
        else:
            input_val = raw_input("# Enter the Input Value >> ").decode(_stdin_encoding)
        print '=' * 80
        el.click()
        el.set_text(input_val)
        sleep(1)
        return True

    def do_checkbox(self):
        el = self.find_element()
        if el is None:
            return False

        print ( '# Selected Checkbox Action >> %s' % self.to_action_info() )
        print '=' * 80

        el.click()
        sleep(1)

        return True

    def execute(self):
        try:
            if self.action_type == 'input':
                return self.do_input()

            elif self.action_type == 'click' or self.action_type == 'long-click':
                return self.do_touch()

            elif self.action_type == 'spinner':
                return self.do_touch()

            elif self.action_type == 'swipe':
                return self.do_swipe()

            elif self.action_type == 'scroll':
                return self.do_scroll()

            elif self.action_type == 'checkbox':
                return self.do_checkbox()
            else:
                print("# Execute Fail(Unknown Action): %s" % str(self.action))

        except:
            print("# Execute Fail: %s" % str(traceback.format_exc()))

        return False
##################### ActionExecutor #######################################################################

def has_visible_node(soup):
    fnode = soup.findAll(attrs={'z-index': '1'})
    return len(fnode) > 0

def clean_invisible_nodes(node):
    action_attrs = ['enabled', 'checkable', 'clickable', 'long-clickable', 'scrollable']
    for c in list(node.children):
        if not isinstance(c, Tag):
            continue

        #webview는 제외
        if c.name == 'android.webkit.WebView':
            continue

        # 이전 xml 때문
        if not c.has_attr('z-index'):
            return None

        if len(list(c.children)) > 0:
            found = c.find(attrs={'z-index': '-1'})
            if found:
                found = c.find(attrs={'z-index': '1'})
                if not found:
                    c.decompose()
                # for attr in action_attrs:
                #     c[attr] = 'false'
        else:
            if c['z-index'] == '-1':
                for attr in action_attrs:
                    c[attr] = 'false'

        clean_invisible_nodes(c)

def xml_doc_save(self, data):
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
    return xml


def _remove_webview(soup):
    webviews = soup.find_all('android.webkit.WebView')
    [w.extract() for w in webviews]


def to_clean_xml(xml, without_webview=False):
    # clean webview
    soup = BeautifulSoup(xml, "xml", from_encoding="utf-8")
    if without_webview:
        _remove_webview(soup)

    if has_visible_node(soup):
        clean_invisible_nodes(soup.hierarchy)

    return str(soup)

def get_actions(driver, xml, without_webview=True, context='NATIVE_APP'):
    actions = []

    # clean webview
    soup = BeautifulSoup(xml, "xml", from_encoding="utf-8")
    if without_webview:
        _remove_webview(soup)

    if has_visible_node(soup):
        clean_invisible_nodes(soup.hierarchy)

    # print str(soup)
    action_table = ActionTable( str(soup) ).to_table()

    #action_table to actions
    for action in action_table:
        actions.append({
            'target': action.target,
            'action': action.atype,
            'input-type': action.input_type,
            'bounds': str(action.bounds),
            'xpath': action.xpath,
            'desc': action.desc,
            'label': action.label,
            'type': context
        })
    return actions

def get_actions_only_native(driver, xml, context='NATIVE_APP'):
    actions = []

    # clean webview
    soup = BeautifulSoup(xml, "xml", from_encoding="utf-8")

    if has_visible_node(soup):
        clean_invisible_nodes(soup.hierarchy)

    # print str(soup)
    action_table = ActionTable( str(soup) ).to_table()

    #action_table to actions
    for action in action_table:
        actions.append({
            'target': action.target,
            'action': action.atype,
            'input-type': action.input_type,
            'bounds': str(action.bounds),
            'xpath': action.xpath,
            'desc': action.desc,
            'label': action.label,
            'type': context
        })
    return actions


def exec_action(data, idx):
    action = data['actions'][idx]
    if action['type'] != NATIVE_CONTEXT:
        print "Action is not native type: %s" % str(action)
        return False

    action_type = action['action']

    #context switching to native
    if data['now_context_num'] != 0:
        data['driver'].switch_to.context(data['contexts'][0])

    return ActionExecutor(data['driver'], action, idx).execute()
#####################################################################################################################################


def get_window_list(data):
    driver = data['driver']
    print '# CURRENT_WINDOW', driver.current_window_handle
    i = 0
    w = driver.window_handles
    for h in w:
        print '# Window %d: %s' % (i, h)
        i = i + 1

    driver.switch_to_window(w[1])
    print '# CURRENT_WINDOW (s)', driver.current_window_handle
    sleep(2)
    driver.switch_to_default_content()
    print '# CURRENT_WINDOW (d)', driver.current_window_handle
    return driver.window_handles


def scroll(data, direction):
    data['driver'].switch_to.context(data['contexts'][0])
    win_size = data['driver'].get_window_size()

    x1 = int(win_size['width'] * 0.5)
    x2 = x1
    y1 = int(win_size['height'] * 0.80)
    y2 = int(win_size['height'] * 0.25)

    if direction == 'DOWN':
        data['driver'].swipe(x1, y1, x2, y2, 800)
    else:
        data['driver'].swipe(x2, y2, x1, y1, 800)


def do_action(data):
    choice = raw_input('\n# Input Action Number >> ')

    if choice == 'exit':
        print 'exit'
        return False

    idx = None
    try:
        idx = int(choice)
    except:
        if choice == 'w-list':
            #switching window
            wlist = get_window_list(data)
            return True
        else:
            print 'exit'
            return False

    # do action
    if not exec_action(data, idx):
        return False

    sleep(1)
    return True


############################################################################################################
