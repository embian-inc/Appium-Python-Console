# -*- coding: utf-8 -*-
import os, sys, csv
from bs4 import BeautifulSoup, Tag
from rect import Bounds, Point, DistMatrix
from labeled_action import LabeledAction
from labeled_group import LabeledGroup
from tokenizer import Tokenizer
from webview_element import WebviewElement
reload(sys)
sys.setdefaultencoding('utf-8')

class ActionTable(object):
    NOT_TOUCHIABLE_WIDGETS = [
        "android.view.ViewGroup",
        "android.webkit.WebView",
        "android.widget.ListView",
        "android.widget.ScrollView",
        "android.widget.ViewSwitcher",
        "android.support.v7.widget.RecyclerView",
        "android.widget.GridView",
        "android.widget.HorizontalScrollView",
        "android.support.v4.view.ViewPager",
        "com.toast.comico.widget.HorizontalScrollView"
    ]

    ACTION_GROUP_SELECTION_TYPE = 'selection'
    ACTION_GROUP_SEQUENCE_TYPE  = 'sequence'

    RADIO_WIDGETS = ["android.widget.RadioButton"]

    SWIPE_WIDGETS = ['android.widget.HorizontalScrollView', 'android.support.v4.view.ViewPager']
    INPUT_WIDGETS = LabeledAction.INPUT_WIDGETS
    SELECT_WIDGETS = ['android.widget.Spinner']

    RID_SEP_REGEX = r'([_\-])'
    TXT_SEP_REGEX = r'([\,\!\$\%\^\&\*\[\]\{\}\?\:\'\)\( \t"])'
    DEFAULT_MAX_DISTANCE = 0

    LARGE_BUTTON_MAX_SIZE = None
    LARGE_BUTTON_MIN_SIZE = None
    PAGE_BUTTON_BOUNDS    = None

    EN_MAX_WORD = 5
    EN_MAX_CHAR = 25
    EN_MIN_WORD = 1
    EN_MIN_CHAR = 1

    KO_MAX_WORD = EN_MAX_WORD
    KO_MAX_CHAR = 15
    KO_MIN_WORD = EN_MIN_WORD
    KO_MIN_CHAR = 1

    TRAVERSAL_SKIP_WIDGET   = ['radiobutton']
    TRAVERSAL_ATYPE         = ['input', 'spinner', 'checkbox']
    TRAVERSAL_FINISH_ATYPE  = ['click']

    #target 입장
    TRAVERSAL_POS           = [Bounds.RELATIVE_POS_LEFT, Bounds.RELATIVE_POS_RIGHT, Bounds.RELATIVE_POS_BOTTOM]

    #webview:
    # [
    #     {
    #         'target':appium_element,
    #         'input-type':'null|...',
    #         'checked':'true|false',
    #         'action':'none|input|click',
    #         'xpath':'...',
    #         'bounds': '[0,0][0,0]',
    #         'content-desc': '....',
    #         'type': 'WEBVIEW_XXXX',
    #         'class': tag_name,
    #         'resource-id': '...'
    #     },
    # ]
    def __init__(self, xml_data, webview=None):
        self.tree = BeautifulSoup(xml_data, "xml")
        self.webview = webview
        self.action_groups = []
        self._init()

    def _init(self):
        self.screen = {'width': 0, 'height': 0}
        for key in self.screen.keys():
            if self.tree.hierarchy.has_attr(key):
                try:
                    self.screen[key] = int(self.tree.hierarchy[key])
                except:
                    self.screen = {'width': 0, 'height': 0}
                    pass

        if self._has_screen_info():
            self.DEFAULT_MAX_DISTANCE = min(self.screen['width'], self.screen['height'])
            self.LARGE_BUTTON_MAX_SIZE = Point(self.screen['width'], self.screen['height']/10)
            self.LARGE_BUTTON_MIN_SIZE = Point(self.screen['width']/2, self.screen['height']/17)
            self.PAGE_BUTTON_BOUNDS = Bounds(Point(0, self.screen['height'] - (self.screen['height']/5)), Point(self.screen['width'], self.screen['height']))

        self.tokenizer = Tokenizer()
        self.action_list = []
        self.elements = []
        self.index_map = {}
        self.bounds_list = []

        self._extract_actions_for_webview(self.elements, self.index_map, self.bounds_list)
        self._extract_actions(self.tree.hierarchy, self.elements, self.index_map, self.bounds_list)
        #sort action_list by x-order, y-order
        self.action_list.sort(key = lambda k: (k.y_order, k.x_order))
        #update action no
        for no, action in enumerate(self.action_list):
            action.no = no

        # bounds_vec = map(lambda b: Point(b.left+(b.width/2), b.top), self.bounds_list)
        bounds_vec = map(lambda b: Point(b.left, b.top), self.bounds_list)
        self.dm = DistMatrix(bounds_vec)

    def _has_screen_info(self):
        return self.screen['width'] > 0 and self.screen['height'] > 0

    #TODO: screen size
    def _unbounded(self, bounds):
        if bounds.area <= 0:
            return True

        if bounds.p1.x < 0 or bounds.p1.y < 0 or bounds.p2.x < 0 or bounds.p2.y < 0:
            return True

        return False

    def _get_dictkey_value_from(self, element):
        if element.has_attr('hashcode'):
            return element['hashcode']

        return element

    def _extract_actions_for_webview(self, elements, index_map, bounds_list):
        if self.webview is None:
            return None

        for element in self.webview:
            w_element = WebviewElement(element)
            #TODO: xml과 형태를 맞추기 위해
            w_element['text'] = ''
            # w_element['resource-id'] = ''
            w_element['instance'] = '0'
            w_element['password'] = 'false'
            w_element['selected'] = 'false'
            if w_element['input-type'] == 'password':
                w_element['password'] = 'true'
            bounds = Bounds.to_bounds(w_element['bounds'])
            if self._unbounded(bounds):
                continue

            #add to elements
            elements.append(w_element)
            no = len(elements)-1
            index_map[self._get_dictkey_value_from(w_element)] = no
            bounds_list.append(bounds)

            if w_element['action'] != 'none':
                self.action_list.append(LabeledAction(w_element, w_element['action'], no))

    def _action_type(self, element):
        #for webviewelement
        if isinstance(element, WebviewElement):
            if 'action' in element and element['action'] != 'none':
                return element['action']

        if element['enabled'] == u'false':
            return None

        #editable
        if element['class'] in self.INPUT_WIDGETS:
            return 'input'

        #selectable
        elif element['clickable'] == u'true' and element['class'] in self.SELECT_WIDGETS:
            return 'spinner'

        #scrollable
        elif element['scrollable'] == u'true':
            if element['class'] in self.SWIPE_WIDGETS:
                return 'swipe'
            else:
                return 'scroll'

        #checkable
        elif element['checkable'] == u'true':
            return 'checkbox'

        #clickable
        elif element['clickable'] == u'true' and element['class'] not in self.NOT_TOUCHIABLE_WIDGETS:
            return 'click'

        # #long-clickable
        # elif attrib['long-clickable'] == u'true' and attrib['class'] not in self.NOT_TOUCHIABLE_WIDGETS:
        #     return 'long-click'

        return None

    def _extract_actions(self, element, elements, index_map, bounds_list):
        for c in element.children:
            if not isinstance(c, Tag):
                continue

            if c is None or not c.has_attr('bounds'):
                continue

            attrib = c

            bounds = Bounds.to_bounds(attrib['bounds'])
            if self._unbounded(bounds):
                continue

            #add to elements
            elements.append(c)
            no = len(elements)-1
            index_map[self._get_dictkey_value_from(c)] = no

            bounds_list.append(bounds)

            atype = self._action_type(c)
            if atype is not None:
                self.action_list.append(LabeledAction(c, atype, no))

            self._extract_actions(c, elements, index_map, bounds_list)

    def _get_element_index(self, element):
        key = self._get_dictkey_value_from(element)
        return self.index_map[key]

    def _get_element_bounds(self, element):
        return self._get_bounds( self._get_element_index(element) )

    def _get_bounds(self, index):
        return self.bounds_list[index]

    def _get_element(self, index):
        return self.elements[index]

    def _to_valid_string(self, sentense):
        tokens = self.tokenizer.tokenize(sentense, self.TXT_SEP_REGEX)
        f_tokens = filter(lambda k: len(k) > 1, tokens) if len(tokens) > 1 else tokens
        f_sentense = ''.join(f_tokens)

        max_word = self.EN_MAX_WORD
        max_char = self.EN_MAX_CHAR

        min_word = self.EN_MIN_WORD
        min_char = self.EN_MIN_CHAR
        if self.tokenizer.has_korean(sentense):
            max_word = self.KO_MAX_WORD
            max_char = self.KO_MAX_CHAR

            min_word = self.KO_MIN_WORD
            min_char = self.KO_MIN_CHAR

        if (len(f_sentense) < min_char) or (len(f_tokens) < min_word) or (len(f_sentense) > max_char) or (len(f_tokens) > max_word):
            return ''

        return ' '.join(tokens)

    def _to_label_string(self, sentense, sep_regex):
        tokens = self.tokenizer.tokenize(sentense, sep_regex)
        # self.tokenizer.clean(tokens)
        return ' '.join(tokens)

    def _to_label_element(self, element, label_bounds, inter, pos, distance):
        attrib = element

        selected = 1 if element['selected'] == 'true' else 0
        desc = self._to_valid_string(attrib['content-desc'])
        text = self._to_valid_string(attrib['text'])
        rid = attrib['resource-id'].split('id/')[-1]

        label_element = {
            'label'     : '',
            'element'   : element,
            'selected'  : selected,
            'pos'       : pos,
            'dist'      : distance,
            'inter'     : inter.area,
            'bounds'    : label_bounds,
            'desc'      : desc,
            'text'      : text,
            'rid'       : rid
        }

        if len(label_element['desc']) > 0:
            label_element['label'] = desc

        if len(label_element['label']) <= 0 and len(label_element['text']) > 0:
            label_element['desc'] = ''
            label_element['label'] = text

        if len(label_element['label']) <= 0 and len(label_element['rid']) > 0:
            label_element['desc'] = ''
            label_element['text'] = ''
            label_element['label'] = self._to_label_string(label_element['rid'], self.RID_SEP_REGEX)

        if len(label_element['label']) <= 0:
            label_element['desc'] = ''
            label_element['text'] = ''
            label_element['rid'] = ''
            label_element['label'] = "%s-%s" % (attrib['class'].split('.')[-1], attrib['instance'])

        return label_element

    def _find_label_element_candidates_for(self, action):
        element = action.element
        index = self._get_element_index(element)
        bounds = self._get_bounds(index)

        max_distance = self.DEFAULT_MAX_DISTANCE
        if max_distance <= 0:
            max_distance = max(bounds.width, bounds.height)


        padded_bounds = bounds.size_up(bounds.width*3, bounds.height)
        indexes = self.dm.select_in(index, max_distance)

        for idx in indexes:
            e = self._get_element(idx)
            b = self._get_bounds(idx)
            padded_b = b.size_up(b.width*3, b.height)

            #intersection
            i = padded_bounds.intersect(padded_b)
            if i.area <= 0:
                #TODO: LOGGING
                continue

            # p1 distance
            if bounds.p1.distance(b.p1) > max_distance:
                #TODO: LOGGING
                continue

            #position
            p = bounds.relative_pos(b)
            if e is element:
                p = LabeledAction.RELATIVE_POS_EQUAL

            #distance
            d = self.dm.distance(index, idx)

            #exception
            if p == Bounds.RELATIVE_POS_UNKNOWN:
                #TODO: LOGGING
                continue

            #filter: overlap
            if p == Bounds.RELATIVE_POS_OVERLAP:
                # not contains
                if (not bounds.contains(b)) and (not b.contains(bounds)):
                    #TODO: LOGGING
                    continue

                # label contains widget: size차이가 max_distance rect보다 큰경우 skip
                if b.contains(bounds) and (b.area > (max_distance * max_distance)):
                    #TODO: LOGGING
                    continue

            action.add_label_element( self._to_label_element(e, b, i, p, d) )

        # if element['bounds'] == '[45,1617][120,1692]':
        #     for c in action.label_elements:
        #         print "%s, %s, %s" % (c['bounds'], c['pos'], c['label'])
        return action


    #####################################################################################################
    def _is_large_button(self, action):
        if (self.LARGE_BUTTON_MAX_SIZE is None) or (self.LARGE_BUTTON_MIN_SIZE is None):
            return False

        if 'button' in action.widget or action.atype == 'click':
            if action.bounds.width <= self.LARGE_BUTTON_MAX_SIZE.width and action.bounds.width >= self.LARGE_BUTTON_MIN_SIZE.width:
                if action.bounds.height <= self.LARGE_BUTTON_MAX_SIZE.height and action.bounds.height >= self.LARGE_BUTTON_MIN_SIZE.height:
                    return True
        return False

    def _is_small_button(self, action):
        if (self.LARGE_BUTTON_MAX_SIZE is None) or (self.LARGE_BUTTON_MIN_SIZE is None):
            return False

        if 'button' in action.widget or action.atype == 'click':
            if action.bounds.width <= self.LARGE_BUTTON_MAX_SIZE.width/3 and action.bounds.width >= self.LARGE_BUTTON_MIN_SIZE.width/3:
                if action.bounds.height <= self.LARGE_BUTTON_MAX_SIZE.height/2 and action.bounds.height >= self.LARGE_BUTTON_MIN_SIZE.height/2:
                    return True
        return False

    def _is_page_finish_button(self, action):
        if self.PAGE_BUTTON_BOUNDS is None:
            return False

        if self.PAGE_BUTTON_BOUNDS.intersect(action.bounds).area != action.bounds.area:
            return False

        return self._is_large_button(action)

    def _is_traversal_finish(self, action_before, action_after):
        pos = action_before.bounds.relative_pos(action_after.bounds)

        padded_after_bounds = action_after.bounds.size_up(action_after.bounds.width, action_after.bounds.height)
        padded_before_bounds = action_before.bounds.size_up(action_before.bounds.width, action_before.bounds.height)

        inter = padded_after_bounds.intersect(padded_before_bounds).area

        text = action_after.text
        desc = action_after.content_desc

        if ('button' not in  action_after.widget)and (len(text) > 10 or len(desc) > 10):
            return False, Bounds.RELATIVE_POS_UNKNOWN

        if inter > 0:
            if pos == Bounds.RELATIVE_POS_RIGHT:
                if action_after.bounds.height >= action_before.bounds.height:
                    return True, pos

            elif pos == Bounds.RELATIVE_POS_BOTTOM:
                if self._is_large_button(action_after) or self._is_small_button(action_after):
                    return True, pos

        elif (pos == Bounds.RELATIVE_POS_BOTTOM) and (self._is_page_finish_button(action_after)):
            # 0: page_finish_buttom
            return True, 0

        return False, Bounds.RELATIVE_POS_UNKNOWN

    def find_traversal_finish(self, action):
        tfinish = []
        for action_after in self.action_list:
            if action_after.atype not in self.TRAVERSAL_FINISH_ATYPE:
                continue

            if (action_after.traversal_before is not None) or (action_after.traversal_after is not None):
                continue

            is_traversal_finish, pos = self._is_traversal_finish(action, action_after)
            if is_traversal_finish:
                # action, pos, angle, distance
                angle = round(action.bounds.center.angle(action_after.bounds.center), 2)
                dist = round(action.bounds.p2.distance(action_after.bounds.p2), 2)
                tfinish.append(  (action_after, pos, angle, dist)  )

        tfinish.sort(key = lambda k: (-k[1], k[3]))
        return tfinish

    def _is_traversal_after(self, action_before, action_after):
        pos = action_before.bounds.relative_pos(action_after.bounds)
        if pos not in self.TRAVERSAL_POS:
            return False

        # if action_before.atype != 'checkbox' and action_after.atype == 'checkbox':
        #     return False
        #
        # if action_before.atype == 'checkbox' and action_after.atype != 'checkbox':
        #     return False

        if (action_after.atype in self.TRAVERSAL_ATYPE) and (action_after.widget not in self.TRAVERSAL_SKIP_WIDGET):
            padded_bounds = action_before.bounds.size_up(action_before.bounds.width, action_before.bounds.height)
            inter = padded_bounds.intersect(action_after.bounds).area
            if inter > 0:
                return True

            padded_bounds = action_after.bounds.size_up(action_after.bounds.width, action_after.bounds.height)
            inter = padded_bounds.intersect(action_before.bounds).area
            if inter > 0:
                return True

        return False

    def find_traversal_after(self, action):
        # print "----------------"
        # print action
        # print "---"
        for action_after in self.action_list:
            if action_after == action:
                continue

            if  (action_after.traversal_before is not None) or (action_after.traversal_after is not None):
                continue

            if (action_after.atype not in self.TRAVERSAL_ATYPE) and (action.widget in self.TRAVERSAL_SKIP_WIDGET):
                continue

            if self._is_traversal_after(action, action_after):
                # print "1 => %s" % action_after
                return action_after

        return None

    def _to_finish_list(self, actions):
        return [ (_a[0], {'p':_a[1], 'a':_a[2], 'd':_a[3]}) for _a in actions ]

    ##### for radio group
    def _find_parents(self, bs4_node, pset={}):
        for parent in bs4_node.find_parents():
            if parent.has_attr('hashcode'):
                if parent['hashcode'] not in pset:
                    pset[parent['hashcode']] = []

                pset[parent['hashcode']].append(bs4_node['hashcode'])

        return pset

    def _list_remove_all(self, alist, other):
        return list(filter(lambda a: a not in other, alist))

    def _to_labeled_group(self, gtype, group, finish):
        return LabeledGroup({'gtype':gtype, 'pre':group, 'final':finish})


    def radio_action_grouping(self):
        #radio groups
        radio_widgets = self.tree.findAll(attrs={'class': self.RADIO_WIDGETS, 'clickable':'true'})
        parents_dict = {}
        for radio in radio_widgets:
            self._find_parents(radio, parents_dict)

        for p_hashcode in parents_dict.keys():
            for pp_hashcode in parents_dict.keys():
                if p_hashcode == pp_hashcode:
                    continue

                if len(parents_dict[p_hashcode]) <= 1:
                    continue

                if len(parents_dict[pp_hashcode]) >= len(parents_dict[p_hashcode]):
                    parents_dict[pp_hashcode] = self._list_remove_all(parents_dict[pp_hashcode], parents_dict[p_hashcode])


        for radio_group in parents_dict.values():
            if len(radio_group) <= 1:
                continue

            group = []
            for radio in radio_group:
                group.append(self.action_table[radio])

            if len(group) > 0:
                tfinish = self.find_traversal_finish(group[-1])
                self.action_groups.append( self._to_labeled_group(self.ACTION_GROUP_SELECTION_TYPE, group, self._to_finish_list(tfinish)) )

    def general_action_grouping(self):
        #other groups
        group_starter = []
        for action in self.action_list:
            if action.traversal_after is not None:
                continue

            if (action.atype in self.TRAVERSAL_ATYPE) and (action.widget not in self.TRAVERSAL_SKIP_WIDGET):
                tafter = self.find_traversal_after(action)
                if tafter is not None:
                    action.set_traversal_after(tafter)

                # start action
                if action.traversal_before is None:
                    group_starter.append(action)


        for action in group_starter:
            # subset인 경우 skip
            if action.traversal_before is not None:
                continue

            after = action.traversal_after
            group = [action]
            while after is not None:
                group.append(after)
                after = after.traversal_after

            tfinish = self.find_traversal_finish(group[-1])
            self.action_groups.append( self._to_labeled_group(self.ACTION_GROUP_SEQUENCE_TYPE, group, self._to_finish_list(tfinish)) )

    def action_grouping(self):
        self.radio_action_grouping()
        self.general_action_grouping()

    def get_action_in_table_for(self, element):
        key = self._get_dictkey_value_from(element)
        if key not in self.action_table:
            return None

        return self.action_table[key]

    def build_action_table(self):
        self.action_table = {}
        unique_id_table = {}

        for action in self.action_list:
            self._find_label_element_candidates_for(action)
            action.select_label_element()
            if action.label_element is None:
                action.select_label_element_by(self)

            action_id = action.action_id
            if action_id not in unique_id_table:
                unique_id_table[action_id] = 0
            else:
                unique_id_table[action_id] += 1

            action.unique_seq = unique_id_table[action_id]

            key = self._get_dictkey_value_from(action.element)
            self.action_table[key] = action

    def to_table(self):
        self.build_action_table()
        self.action_grouping()
        return self.action_list, self.action_groups
