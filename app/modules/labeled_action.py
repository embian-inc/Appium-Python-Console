# -*- coding: utf-8 -*-
import os,sys
from bs4 import BeautifulSoup
from app.modules.rect import Bounds, Point

from labeled_element import LabeledElement
from webview_element import WebviewElement

reload(sys)
sys.setdefaultencoding('utf-8')

class LabeledAction(LabeledElement):
    def __init__(self, element, atype, no):
        super(LabeledAction, self).__init__()
        self.no = no
        self.element = element
        self.atype = atype

        self.clazz = self.element['class'].split('.')[-1].lower()
        self.elem_bounds = Bounds.to_bounds(self.element['bounds'])

        self.traversal_after = None
        self.traversal_before = None

    def set_traversal_after(self, after):
        self.traversal_after = after
        if after is not None:
            after.traversal_before = self

    #implementation
    @property
    def bounds(self):
        return self.elem_bounds

    @property
    def text(self):
        if isinstance(self.element, WebviewElement):
            return self.content_desc

        return self.element['text']

    @property
    def content_desc(self):
        return self.element['content-desc']

    @property
    def resource_id(self):
        # if isinstance(self.element, WebviewElement):
        #     return ''

        return self.element['resource-id']

    @property
    def target(self):
        if isinstance(self.element, WebviewElement):
            return self.element['target']
        return self.element

    @property
    def input_type(self):
        if self.element['password'] == 'true':
            return 'password'

        elif self.element.has_attr('input-type'):
            return self.element['input-type'].lower()

        return ''

    @property
    def e_class(self):
        return self.element['class']


    @property
    def widget(self):
        return self.clazz

    #override
    @property
    def alias(self):
        label = self.label
        if self.input_type == 'password':
            label = self.input_type

        alias = self.ALIAS_TABLE.alias(label)
        if alias is None:
            return None

        return alias[0]

    @property
    def xpath(self):
        if isinstance(self.element, WebviewElement):
            return self.element['xpath']

        return self._to_xpath(self.element)

    @property
    def x_order(self):
        return self.bounds.right

    @property
    def y_order(self):
        return self.bounds.bottom # - (self.bounds.center.y - self.bounds.top)

    @property
    def desc(self):
        return "/alias:%s/pos:%s/widget:%s" % (self.alias, self.label_pos, self.widget)

    @property
    def action_id(self):
        return "/label:%s/pos:%s/widget:%s" % (self.unique_label, self.label_pos, self.widget)

    #override
    def __str__(self):
        return "Element[class:%s, type: %s, bounds:%s] Label[alias:%s, label:%s, pos:%s, bounds:%s]" % (self.element['class'], self.atype, self.bounds, self.alias, self.label, self.label_pos, self.label_bounds)

    def __repr__(self):
        return "Element[class:%s, type: %s, bounds:%s] Label[alias:%s, label:%s, pos:%s, bounds:%s]" % (self.element['class'], self.atype, self.bounds, self.alias, self.label, self.label_pos, self.label_bounds)

    def __eq__(self, other):
        if not isinstance(other, LabeledAction):
            return False

        return self.element == other.element

    def __hash__(self):
        return hash(self.element['class'], self.atype, self.bounds, self.alias, self.label, self.label_pos, self.label_bounds)

    ####################################################################################
    def _to_element_xpath(self, element):
        return "%s[@index=\"%s\"]" % (element.name, element['index'])

    def _to_xpath(self, element, root_tag=['hierarchy']):
        xpath = []
        p = element
        while (p is not None and (p.name not in root_tag)):
            xpath.append( self._to_element_xpath(p) )
            p = p.parent
        return "//%s" % '/'.join(reversed(xpath))

    #action_table is dict: key=>bs4_element or hashcode, value=>instance of LabeledAction
    def select_label_element_by(self, action_table):
        for label_element in self.label_elements:
            action = action_table.get_action_in_table_for(label_element['element'])
            if action is not None:
                if action.label_element:
                    self.label_element = action.label_element.copy()
                    self.label_element['pos'] = self.bounds.relative_pos(self.label_element['bounds'])
                    self.add_label_element(self.label_element)
                    return self.label_element

        # clazz
        self.label_elements.sort(key = lambda k: (k['pos']), reverse=True)
        self.label_element = self.label_elements[0]
        return self.label_element

    ####################################################################################
