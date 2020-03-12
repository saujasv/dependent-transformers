class Word:
    def __init__(self, text, index, governor, dep_rel):
        self.text = text
        self.index = index
        self.governor = governor
        self.dependency_relation = dep_rel

class Sentence:
    def __init__(self, words):
        self.words = words

def linearize_dep_tree(sentence, lexicalized=True):
    tree = {int(word.index): list() for word in sentence.words}
    tree[0] = list()
    # print(tree)
    for word in sentence.words:
        if word.governor == 0:
            tree[0].append(int(word.index))
        else:
            tree[int(word.governor)].append(int(word.index))
    # print(tree)
    
    def traverse(tree, node, linearization, sentence, lexicalized=True):
        if node != 0:
            linearization += '(_'
            linearization += sentence.words[node - 1].dependency_relation + ' '
        if lexicalized:
            if node != 0:
                linearization += sentence.words[node - 1].text + ' '
        for child in tree[node]:
            linearization = traverse(tree, child, linearization, sentence, lexicalized)
        linearization += ') '
        
        return linearization
    
    return traverse(tree, 0, '', sentence, lexicalized)

"""
<Word index=1;text=I;lemma=I;upos=PRON;xpos=PRP;feats=Case=Nom|Number=Sing|Person=1|PronType=Prs;governor=2;dependency_relation=nsubj>
<Word index=2;text=declare;lemma=declare;upos=VERB;xpos=VBP;feats=Mood=Ind|Tense=Pres|VerbForm=Fin;governor=0;dependency_relation=root>
<Word index=3;text=resumed;lemma=resume;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part;governor=2;dependency_relation=xcomp>
<Word index=4;text=the;lemma=the;upos=DET;xpos=DT;feats=Definite=Def|PronType=Art;governor=5;dependency_relation=det>
<Word index=5;text=session;lemma=session;upos=NOUN;xpos=NN;feats=Number=Sing;governor=3;dependency_relation=obj>
"""

if __name__ == '__main__':
    import stanfordnlp
    nlp = stanfordnlp.Pipeline(processors='tokenize,pos,lemma,depparse', lang='en')
    doc = nlp("Barack Obama was born in Hawaii.")
    print(linearize_dep_tree(doc.sentences[0], False))