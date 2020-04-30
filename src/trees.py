import re

class DependencyTree:
    def __init__(self, sentence=None):
        self.tree = None
        self.sentence = sentence

        if sentence:
            tree = {int(word.index): list() for word in sentence.words}
            tree[0] = list()
            for word in sentence.words:
                if word.governor == 0:
                    tree[0].append(int(word.index))
                else:
                    tree[int(word.governor)].append(int(word.index))
            self.tree = tree

    def __traverse(self, node, linearization, lexicalized=True):
        if node != 0:
            linearization += '(_'
            linearization += self.sentence.words[node - 1].dependency_relation + ' '
        if lexicalized:
            if node != 0:
                linearization += self.sentence.words[node - 1].text + ' '
        for child in self.tree[node]:
            linearization = self.__traverse(child, linearization, lexicalized)
        linearization += ') '
        
        return linearization
    
    def linearize(self, lexicalized=True):
        return self.__traverse(0, '', lexicalized)
    
    def to_conllu(self):
        return "\n".join(["\t".join([w.index, w.text, '_', '_', '_', '_', w.governor, '_', '_', '_']) for w in self.sentence])

class ConstituencyNode:
    def __init__(self, label, children=None, word=False):
        self.label = label
        self.word = word
        self.children = children
    
    def __repr__(self):
        return self.label

class ConstituencyTree:
    def __init__(self, linearized=None):
        self.tree = None
        if linearized:
            self.tree, _ = self.__build(re.findall('([^() \n\t]+|[()])', linearized), 0)
    
    def __build(self, l, i):
        # print(l[i])
        if l[i] == '(':
            subtrees = list()
            label = l[i + 1]
            j = i + 2
            while l[j] != ')':
                node, j = self.__build(l, j)
                subtrees.append(node)
            return ConstituencyNode(label, children=subtrees), j + 1
        else:
            return ConstituencyNode(l[i], children=list(), word=True), i + 1
    
    def __traverse(self, node, linearization, lexicalized=False, pos=False):
        if node.word:
            if lexicalized:
                return linearization + node.label + ') '
            else:
                return linearization + ') '
        elif len(node.children) == 1 and node.children[0].word == True:
            if pos:
                linearization = linearization + '(_' + node.label + ' '
            linearization = self.__traverse(node.children[0], linearization, lexicalized, pos)
            return linearization + ') '
        else:
            linearization += '(_' + node.label + ' '
            for c in node.children:
                linearization = self.__traverse(c, linearization, lexicalized, pos)
            return linearization
    
    def linearize(self, lexicalized=False, pos=False):
        return self.__traverse(self.tree, '', lexicalized, pos)

"""
<Word index=1;text=I;lemma=I;upos=PRON;xpos=PRP;feats=Case=Nom|Number=Sing|Person=1|PronType=Prs;governor=2;dependency_relation=nsubj>
<Word index=2;text=declare;lemma=declare;upos=VERB;xpos=VBP;feats=Mood=Ind|Tense=Pres|VerbForm=Fin;governor=0;dependency_relation=root>
<Word index=3;text=resumed;lemma=resume;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part;governor=2;dependency_relation=xcomp>
<Word index=4;text=the;lemma=the;upos=DET;xpos=DT;feats=Definite=Def|PronType=Art;governor=5;dependency_relation=det>
<Word index=5;text=session;lemma=session;upos=NOUN;xpos=NN;feats=Number=Sing;governor=3;dependency_relation=obj>
"""

if __name__ == '__main__':
    pass
    # import stanfordnlp
    # nlp = stanfordnlp.Pipeline(processors='tokenize,pos,lemma,depparse', lang='en')
    # doc = nlp("Barack Obama was born in Hawaii.")
    # print(DependencyTree(sentence=doc.sentences[0]).linearize(lexicalized=False))

    # s = "(ROOT\n  (S\n    (NP (NNP Ujwal))\n    (VP (VBZ is)\n      (NP (PRP$ my) (NN name)))))"
    # print(ConstituencyTree(s).linearize(lexicalized=False, pos=True))