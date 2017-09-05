import os, sys, codecs
from modules.rect import Bounds, Point
from time import sleep
from time import time
from selenium.webdriver.common.action_chains import ActionChains

_stdin_encoding = sys.stdin.encoding or 'utf-8'
input_type_text_list = ["text", "search", "password", "textarea", "email", "number", "tel"]
input_type_etc_list = ["date", "color", "datetime", "month", "range", "time", "week"]

def set_js_script():
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    print file_dir
    file_path = os.path.join(file_dir, 'app/execute_script.js')
    with open(file_path, 'r') as ac_script:
        js_script = ac_script.read()

    return js_script

def get_actions(driver, curr_context):
    script = set_js_script()
    ws = driver.window_handles
    actions = []
    for w in ws:
        driver.switch_to_window(w)
        res = driver.execute_script(script, curr_context)
        act = {
            'key': w,
            'window_width': res['window_width'],
            'window_height': res['window_height'],
            'actions': res['action_list']
        }
        actions.append(act)

    return actions

def get_elements(driver, curr_context):
    script = set_js_script()
    ws = driver.window_handles
    actions = []
    elements = []
    for w in ws:
        driver.switch_to_window(w)
        # t1 = time()
        res = driver.execute_script(script, curr_context)
        # t2 = time()
        # print '\nEcecute Script Running time : ', t2-t1
        # print '\nElapsed time (Js for loop): ', res['elapsed_time']
        act = {
            'key': w,
            'window_width': res['window_width'],
            'window_height': res['window_height'],
            'actions': res['action_list']
        }

        el = {
            'key': w,
            'window_width': res['window_width'],
            'window_height': res['window_height'],
            'actions': res['dom_list']
        }

        actions.append(act)
        elements.append(el)

    return actions, elements


def exec_action(data, idx):
    action = data['actions'][idx]
    if action['type'].find('WEBVIEW') == -1:
        return False
    if data['now_context_num'] == 0:
        data['driver'].switch_to.context(data['contexts'][1])
    action_type = action['action']
    input_type = action['input-type']
    tmp = action['xpath'].split(':')
    action_xpath = tmp[1]
    target_element = data['driver'].find_element_by_xpath(action_xpath)

    # do action
    if action_type == 'input':
        print ( '# Selected Input_%s Action >> %03d. %s - %s %s' % (action_type, idx, str(action_type), str(target_element.tag_name), target_element.text) )
        if 'value' in action and action['value'] is not None:
            input_val = action['value']
        else:
            input_val = raw_input("# Enter the Input Value >> ").decode(_stdin_encoding)
        print '=' * 80
        data['driver'].execute_script('arguments[0].value = arguments[1];', action['target'], input_val)
        # target_element.clear()
        # target_element.send_keys(input_val)
    elif action_type == 'spinner':
        print ( '# Selected Spinner Action >> %03d. %s - %s %s' % (idx, str(action_type), str(target_element.tag_name), target_element.text) )
        print '=' * 80

        target_element.click()

    elif action_type == 'input' and input_type in input_type_etc_list:
        print ( '# Selected Input_%s Action >> %03d. %s - %s %s' % (action_type, idx, str(action_type), str(target_element.tag_name), target_element.text) )
        print '=' * 80

        target_element.click()

    elif action_type == 'click' or action_type == 'checkbox':
        print ( '# Selected Execute_Script Click Action >> %03d. %s - %s %s' % (idx, str(action_type), str(target_element.tag_name), target_element.text) )
        print '=' * 80
        data['driver'].execute_script('if(!arguments[0].checked) { arguments[0].click(); }', action['target'])

        # ac = ActionChains(data['driver'])
        # ac.move_to_element(target_element).click().perform()

        # target_element.click()

    return True
