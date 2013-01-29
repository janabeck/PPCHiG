import argparse
from lxml import etree
import re

class Token():
    """A Perseus dependency tree."""

    def __init__(self):

        self.id = ""

        self.dependencies = {}

        self.list_form = {}

class Subtree():
    """A subtree encoded with head, inclusive dependents, relation, postag, lemma, and continuity."""

    def __init__(self):

        self.root = 0

        self.head = 0

        self.deps = []

        self.relation = ""

        self.postag = ""

        self.lemma = ""

        self.continuity = False

    def print_subtree(self):

        print "Root: " + self.root
        print "Head: " + self.head
        print str(self.deps) + ", " + self.relation + ", " + self.postag + ", " + self.lemma + ", " + str(self.continuity)
        print

class Seeker():
    """Utility for searching the Perseus Ancient Greek Dependency Treebanks."""

    RE = dict(re="http://exslt.org/regular-expressions")

    def __init__(self, xml_name):

        self.doc = etree.parse(xml_name)

        # temp variable for returning recursive list of a head's dependents
        # also used for returning extra coding strings
        # kind of a klugey solution, tbh
        self.tmp = []

        self.recursed = False

        self.sentences = self.doc.xpath("//sentence/@id")

        self.trees = {}

        for token in self.sentences:
            tok = Token()
            tok.id = token
            self._map_tree(token, tok)
            self.trees[token] = tok

    def _print_all(self):
        """Print all Token instances."""

        for ident in self.sentences:
            print "Sentence ID #" + ident + ":"
            for key,s in self.trees[ident].dependencies.items():
                print key + ": " + str(s.deps) + ", " + s.relation + ", " + s.postag + ", " + s.lemma + ", " + str(s.continuity)
            print

    def _map_tree(self, ident, tok):
        """Map all the dependencies (recursively) in dependency tree with @id = ident."""

        heads = self.doc.xpath("//sentence[@id=" + ident + "]/word/@id")

        full_tree = {}

        list_form = {}

        for head in heads:
            dependents = self._get_dependents(ident, head)
            self._turtles(ident, dependents, dependents)
            recurs_deps = self.tmp
            recurs_deps.append(int(head))
            recurs_deps.sort()
            subtree = Subtree()
            subtree.root = head
            subtree.head = self.doc.xpath("//sentence[@id=" + ident + "]/word[@id=" + head + "]/@head")[0]
            subtree.deps = recurs_deps
            subtree.relation = self.doc.xpath("//sentence[@id=" + ident + "]/word[@id=" + head + "]/@relation")[0]
            subtree.postag = self.doc.xpath("//sentence[@id=" + ident + "]/word[@id=" + head + "]/@postag")[0]
            subtree.lemma = self.doc.xpath("//sentence[@id=" + ident + "]/word[@id=" + head + "]/@lemma")[0]
            subtree.continuity = self._check_sequence(recurs_deps)
            full_tree[head] = subtree
            # list form for easier unit test
            lst = [recurs_deps]
            lst = lst + [head, subtree.head, subtree.relation, subtree.postag, subtree.lemma, subtree.continuity]
            list_form[head] = lst

        tok.dependencies = full_tree
        tok.list_form = list_form

    def _turtles(self, ident, deps, new_deps):
        """Facilitate recursive getting of dependents."""

        all_next = []

        for idx in new_deps:
            next_level = self._get_dependents(ident, idx)
            if next_level:
                all_next = all_next + next_level

        if all_next:
            deps = deps + all_next
            self._turtles(ident, deps, all_next)
        else:
            self.tmp = deps

    def _get_dependents(self, ident, head):
        """Return a list of the @ids of the dependents of the @id ('head') passed in."""

        dependents = self.doc.xpath("//sentence[@id=" + ident + "]/word[@head=" + str(head) + "]/@id")

        return [int(idx) for idx in dependents]

    def _check_sequence(self, lst):
        """Check if all the dependents of (and including) the head are in sequence."""

        last_index = 0

        for index in lst:
            if index != last_index + 1 and last_index != 0:
                return False
            last_index = index

        return True

    def _classify_root(self, ident):
        """Return the @id (index) of the root and its relation as a tuple."""

        ids = self.doc.xpath("//sentence[@id=" + ident + "]/word[@head='0']/@id")

        if len(ids) > 2:
            print "More than 2 roots in this sentence!"
        else:
            for i in ids:
                rel = self.doc.xpath("//sentence[@id=" + ident + "]/word[@id=" + i + "]/@relation")
                if rel != 'AuxK':
                    return (i, rel[0])

    def _split_coord(self, ident):
        """Return a list of @ids (indices) of words with PRED_CO relation."""

        return self.doc.xpath("//sentence[@id=" + ident + "]/word[@relation='PRED_CO']/@id")

    def _code_clause(self, ident, root):
        """Returns a coding string identical to that produced by clause_types.c."""

        coding_string = ""

        rtree = self.trees[ident].dependencies[root]

        subj_head = ""
        obj_head = ""

        # type of verb
        # 'v' must be finite, non-imperative
        finite_verb = re.compile('v...[iso].---')

        if finite_verb.match(rtree.postag):
            if rtree.lemma.find('ei)mi/') == -1:
                coding_string += "v:"
            else:
                coding_string += "b:"
        else:
            coding_string += "o:"

        pronoun = re.compile('p..---..-')

        article = re.compile('l-.---..-')

        found = False

        additional_clauses = []

        # type of subject
        for stree in self.trees[ident].dependencies.values():
            if stree.relation == "SBJ" and stree.head == rtree.root:
                subj_head = stree.root
                sbj = self.trees[ident].dependencies[subj_head]
                found = True
                if not stree.continuity:
                    coding_string += "t:"
                else:
                    if len(stree.deps) > 1:
                        coding_string += "n:"
                    elif len(stree.deps) == 1:
                        if pronoun.match(stree.postag):
                            coding_string += "p:"
                        elif article.match(stree.postag):
                            coding_string += "p:"
                        else:
                            coding_string += "n:"
            # looks for embedded finite clauses in e.g., relative or adverbial clauses
            if finite_verb.match(stree.postag) and int(stree.root) in rtree.deps and not self.recursed:
                additional_clauses.append(stree.root)

        if not self.recursed:
            self.recursed = True
            self.tmp = []
            for a in additional_clauses:
                #print(self._code_clause(ident, a), self.trees[ident].dependencies[a].lemma)
                self.tmp.append(self._code_clause(ident, a))

        if not found:
            coding_string += "e:"

        found = False

        # type of object (first object only considered, if more than one)
        for stree in self.trees[ident].dependencies.values():
            if stree.relation == "OBJ" and stree.head == rtree.root:
                obj_head = stree.root
                obj = self.trees[ident].dependencies[obj_head]
                found = True
                if not stree.continuity:
                    coding_string += "t:"
                    break
                else:
                    if len(stree.deps) > 1:
                        coding_string += "n:"
                        break
                    elif len(stree.deps) == 1:
                        if pronoun.match(stree.postag):
                            coding_string += "p:"
                            break
                        elif article.match(stree.postag):
                            coding_string += "p:"
                            break
                        else:
                            coding_string += "n:"
                            break

        if not found:
            coding_string += "-:"

        found = False

        # order of subject and verb
        if subj_head:
            if int(sbj.root) < int(rtree.root):
                coding_string += "s:"
            else:
                coding_string += "v:"
        else:
            coding_string += "-:"

        # order of object and verb (first object only considered, if more than one)
        if obj_head:
            if int(obj.root) < int(rtree.root):
                coding_string += "o:"
            else:
                coding_string += "v:"
        else:
            coding_string += "-:"

        # order of subject and object (first object only considered, if more than one)
        if subj_head and obj_head:
            if int(sbj.root) < int(obj.root):
                coding_string += "s:"
            else:
                coding_string += "o:"
        else:
            coding_string += "-:"

        # more than one object
        obj_heads = []

        for stree in self.trees[ident].dependencies.values():
            if stree.relation == "OBJ" and stree.head == rtree.root:
                obj_heads.append(stree.root)

        if len(obj_heads) > 1:
            coding_string += "t:"
        elif len(obj_heads) == 1:
            coding_string += "f:"
        else:
            coding_string += "-:"

        # verb is first in clause
        if int(rtree.root) == 1:
            coding_string += "t:"
        elif int(rtree.root) > 1:
            coding_string += "f:"
        else:
            coding_string += "-:"

        # verb is last in clause
        heads = []

        for stree in self.trees[ident].dependencies.values():
            if stree.head == rtree.root:
                heads.append(int(stree.root))
                
        if max(heads) < int(rtree.root):
            coding_string += "t"
        elif max(heads) > int(rtree.root):
            coding_string += "f"
        else:
            coding_string += "-"

        return coding_string

    def clause_types(self):
        """Returns a dict where keys = sentence IDs and values = coding strings identical to that produced by clause_types.c."""

        results = {}

        for ident in self.sentences:
            root_id, root_type = self._classify_root(ident)
            if root_type == "PRED":
                results[ident] = [self._code_clause(ident, root_id)]
                results[ident] += self.tmp
                self.recursed = False
            elif root_type.find('ExD') != -1:
                results[ident] = [self._code_clause(ident, root_id)]
                results[ident] += self.tmp
                self.recursed = False
            else:
                lst = []
                for clause_head in self._split_coord(ident):
                    lst.append(self._code_clause(ident, clause_head))
                    lst = lst + self.tmp
                    self.recursed = False
                results[ident] = lst

        return results

def main():

    parser = argparse.ArgumentParser(description='Process the input files.')
    parser.add_argument('-x', '--xml', action = 'store', dest = "xml_name", help='name of Perseus XML file')
    args = parser.parse_args()

    seeker = Seeker(args.xml_name)

    dct = seeker.clause_types()

    print
    print dct
    print

    #seeker._print_all()

if __name__ == '__main__':
    main()