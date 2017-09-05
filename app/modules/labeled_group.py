# -*- coding: utf-8 -*-
import os,sys
from bs4 import BeautifulSoup
from app.modules.rect import Bounds, Point

from labeled_element import LabeledElement

reload(sys)
sys.setdefaultencoding('utf-8')

class LabeledGroup(LabeledElement):
    #group: {'gtype':'selection|sequence', 'pre':[LabeledAction, ...], 'final':[(LabeledAction, {'a': angle, 'p':pos, 'd':distnace}), ...]}
    def __init__(self, group):
        super(LabeledGroup, self).__init__()
        self.group = group
        self._init_label_elements()

    def _init_label_elements(self):
        actions = self.pre_actions
        _filter = [Bounds.RELATIVE_POS_LEFT, Bounds.RELATIVE_POS_TOP]
        if len(actions) == 1:
            _filter.append(self.RELATIVE_POS_EQUAL)

        self.label_elements = filter(lambda k: k['pos'] in _filter , actions[0].label_elements)
        self.select_label_element()

    #override
    def select_label_element(self):
        if self.label_elements is None or len(self.label_elements) == 0:
            return None

        # self
        self.label_elements.sort(key = lambda k: (k['pos']), reverse=True)
        self.label_element = self.label_elements[0]
        if self.label_element['pos'] == self.RELATIVE_POS_EQUAL:
            if len(self.label_element['text']) > 0 or len(self.label_element['desc']) > 0 or len(self.label_element['rid']) > 0:
                return self.label_element

        # text or description
        self.label_elements.sort(key = lambda k: (k['pos'], k['selected'], -k['dist']), reverse=True)
        self.label_element = self._select_first_by(['text', 'desc'], self.label_elements)
        if self.label_element is not None:
            return self.label_element

        # resource-id
        self.label_elements.sort(key = lambda k: (k['pos'], k['selected'], -k['dist']), reverse=True)
        self.label_element = self._select_first_by(['rid'], self.label_elements)
        if self.label_element is not None:
            return self.label_element

        return None


    @property
    def bounds(self):
        return self.pre_actions[0].bounds

    @property
    def gtype(self):
        return self.group['gtype']

    @property
    def desc(self):
        return "/alias:%s/pos:%s" % (self.alias, self.label_pos)

    @property
    def pre_actions(self):
        return self.group['pre']

    @property
    def pre_desc(self):
        return [ action.no for action in self.pre_actions ]

    @property
    def final_actions(self):
        return self.group['final']

    @property
    def final_desc(self):
        return [ (f[0].no, f[1]) for f in self.final_actions ]
