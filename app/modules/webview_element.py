# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WebviewElement(object):
    def __init__(self, element):
        self.element = element
        
    #bs4 node의 methods
    def has_attr(self, attr):
        if attr == 'hashcode':
            return True
            
        return False
    
    def __hash__(self):
        return hash(self.element['xpath'])
        
    def __str__(self):
        return str(self.element)
    
    def __eq__(self, other):
        if isinstance(other, WebviewElement):
            return self.element == other.element
            
        return False
        
    def __getitem__(self, key):
        if key == 'hashcode':
            return str(hash(self))
            
        return self.element[key]
        
    def __setitem__(self, key, value):
        self.element[key] = value

    def __delitem__(self, key):
        del self.element[key]

    def __iter__(self):
        return iter(self.element)

    def __len__(self):
        return len(self.element)