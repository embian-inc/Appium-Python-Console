# -*- coding: utf-8 -*-
import os,sys
from bs4 import BeautifulSoup
from app.modules.rect import Bounds, Point

from alias_table import AliasTable
reload(sys)
sys.setdefaultencoding('utf-8')

class LabeledElement(object):
    ___CUR_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    INPUT_WIDGETS = ["android.widget.EditText", "android.widget.AutoCompleteTextView", "android.widget.MultiAutoCompleteTextView"]
    RELATIVE_POS_EQUAL = Bounds.RELATIVE_POS_OVERLAP+1
    ALIAS_TABLE = AliasTable(___CUR_FILE_PATH+'/alias.csv')

    def __init__(self):
        self.label_element = None
        self.label_elements = []
        self.unique_seq = 0

    def add_label_element(self, le):
        self.label_elements.append(le)

    @property
    def label(self):
        if self.label_element:
            return self.label_element['label']

        return ''

    @property
    def unique_label(self):
        if self.unique_seq == 0:
            return self.label

        return "%s-%d" % (self.label, self.unique_seq)

    @property
    def alias(self):
        alias = self.ALIAS_TABLE.alias(self.label)
        if alias is None:
            return ''

        return alias[0]

    @property
    def label_pos(self):
        if self.label_element:
            return self._pos_str(self.label_element)

        return ''

    @property
    def label_bounds(self):
        if self.label_element:
            return self.label_element['bounds']

        return None

    @property
    def bounds(self):
        raise RuntimeError('Implementation Required')
        return None

    def __str__(self):
        return "Label[alias:%s, label:%s, pos:%s, bounds:%s]" % (self.alias, self.label, self.label_pos, self.label_bounds)


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
        self.label_elements.sort(key = lambda k: (k['pos'], self._txtvalue_to_score('text', k), -k['dist']), reverse=True)
        self.label_element = self._select_first_by(['text', 'desc'], self.label_elements)
        if self.label_element is not None:
            return self.label_element

        # resource-id
        self.label_elements.sort(key = lambda k: (k['pos'], self._txtvalue_to_score('rid', k), -k['dist']), reverse=True)
        self.label_element = self._select_first_by(['rid'], self.label_elements)
        if self.label_element is not None:
            return self.label_element

        return None

    def _select_first_by(self, keys, label_elements):
        for l in label_elements:
            for key in keys:
                if (key in l) and (len(l[key]) > 0):
                    return l

        return None

    def _txtvalue_to_score(self, key, label_element):
        score = 0
        if key not in label_element:
            return score

        value_len = len(label_element[key])
        if value_len <= 0:
            return score

        if value_len > 0:
            score = 1
            if key == 'text':
                lbounds = label_element['bounds']
                # 30을 주는 이유는, padding때문 (len짧은경우, 판단하기 위해)
                padding = 30
                if label_element['element']['class'] in self.INPUT_WIDGETS:
                    padding += 90

                font_size = lbounds.height - padding
                if font_size <= 0:
                    font_size = 1

                wcnt = lbounds.width / font_size
                if value_len <= wcnt:
                    score += font_size

                else:
                    score += lbounds.width / value_len

        return score

    def _pos_str(self, label_element):
        pos = label_element['pos']
        if pos == self.RELATIVE_POS_EQUAL:
            return 'self'

        if int(pos) == Bounds.RELATIVE_POS_OVERLAP:
            e_bounds = self.bounds
            le_bounds = label_element['bounds']

            if le_bounds.contains(e_bounds):
                return 'contains'

            return 'contained_in'

        if pos == Bounds.RELATIVE_POS_LEFT:
            return 'right'

        if pos == Bounds.RELATIVE_POS_TOP:
            return 'bottom'

        if pos == Bounds.RELATIVE_POS_RIGHT:
            return 'left'

        if pos == Bounds.RELATIVE_POS_BOTTOM:
            return 'top'

        return 'unknown'
