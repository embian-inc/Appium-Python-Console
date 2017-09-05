# -*- coding: utf-8 -*-

import re, sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Tokenizer(object):
    CLEAN_WORKDS = [
        'layout',
        'll',
        'img',
        'btn'
    ]
    
    KOR_REGEX = u'[ㄱ-ㅎㅏ-ㅣ가-힣]'
    
    def korean_len(self, sentense):
        return len(re.findall(self.KOR_REGEX, sentense))
        
    def has_korean(self, sentense):
        return self.korean_len(sentense) > 0
    
    def tokenize(self, sentense, sep_regex):
        return re.sub(sep_regex, ' ', sentense.lower()).split()
        
    def clean(self, tokens):
        for word in self.CLEAN_WORKDS:
            if word in tokens:
                tokens.remove(word)
            
        return tokens