class Word:
    def __init__(self, text=None, index=None, governor=None, dep_rel=None):
        self.text = text
        self.index = index
        self.governor = governor
        self.dependency_relation = dep_rel
    
    def __repr__(self):
        return "<Word index={:s};text={:s};governor={:s};dependency_relation={:s}>".format(self.index, self.text, self.governor, self.dependency_relation)

class Sentence:
    def __init__(self, words, from_parsed=False):
        if from_parsed:
            word_objects = list()
            for w in words:
                match = re.match("<Word index=([0-9]+);text=(.+);lemma=.+;upos=.+;xpos=.+;feats=.+;governor=([0-9]+);dependency_relation=(.+)>", w)
                if not match:
                    raise FormatError
                
                word_objects.append(Word(match.group(2), match.group(1), match.group(3), match.group(4)))

            self.words = sorted(word_objects, key=lambda x: x.index)
        else:
            self.words = words
    
    def __repr__(self):
        return "\n".join([str(w) for w in self.words])
    
    def get_words(self):
        return [w.text for w in self.words]

class CountError(Exception):
    pass

class FormatError(Exception):
    pass

def get_line_count(f):
    i = 0
    for line in f:
        i += 1
    return i