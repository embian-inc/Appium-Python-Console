# -*- coding: utf-8 -*-

import sys, re, csv, codecs
import editdistance
reload(sys)
sys.setdefaultencoding('utf-8')

def codecs_open(file_path, mode='rb', encoding='utf-8'):
    with codecs.open(file_path, 'rb', encoding='utf-8') as f:
        for line in f:
            yield line.encode(encoding)


class AliasTable(object):
    VALUE_REGEX_PREFIX = 'REGEX://'
    def __init__(self, alias_file):
        self.alias_file = alias_file
        self.general_table = {}
        self.regex_table = {}
        self.load_alias()

    def load_alias(self):
        reader = csv.reader(codecs_open(self.alias_file, encoding='utf-8'), delimiter=',', quotechar='"')
        for row in reader:
            alias = row[0].strip().decode('utf-8')
            if len(alias) <= 0:
                continue

            self.general_table[alias] = alias
            for value in row[1:]:
                value = value.decode('utf-8')
                if len(value.strip()) > 0:
                    if value.startswith(self.VALUE_REGEX_PREFIX):
                        self.regex_table[value.replace(self.VALUE_REGEX_PREFIX, '')] = alias
                    else:
                        self.general_table[value] = alias


    def _editdistance(self, query, value):
        return editdistance.eval(query, value)

    #return (alias, distance)
    def alias(self, query):
        if query is None:
            return (query, 0.0)

        query = query.lower()
        # complete matching
        if query in self.general_table:
            return (self.general_table[query], 0.0)

        # regex matching
        for val, alias in self.regex_table.iteritems():
            if re.match(val, query):
                return alias, 0.0

        matches = {}
        # Levenshtein distance
        for val, alias in self.general_table.iteritems():
            if val in query:
                # len <= 3 exact matching
                dist = 0.0
                if len(val) <= 3:
                    if val == alias:
                        dist = 0.0
                    else:
                        continue

                else:
                    dist = self._editdistance(query, val)

                if alias not in matches:
                    matches[alias] = {'min_dist': 0.0, 'cnt': 0}
                matches[alias]['cnt'] += 1
                matches[alias]['min_dist'] = min(dist, matches[alias]['min_dist'])

        if len(matches.keys()) > 0:
            matches = sorted(matches.items(), key=lambda k: (-k[1]['cnt'], k[1]['min_dist']) )
            return matches[0][0], matches[0][1]['min_dist']

        return (query, 0.0)
