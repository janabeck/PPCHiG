import argparse
from lxml import etree
import re
import sys

class Token():
    """A Perseus dependency tree."""

    def __init__(self):

        self.id = ""

        self.dependencies = {}

        # key = [recurse_deps, head/root, subtree.head, subtree.relation, subtree.postag, subtree.lemma, subtree.continuity]
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

    def __init__(self, file_base, xml_name, n):

        self.FINITE_VERB = re.compile('v...[iso].---')

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

        self.log = open("logs/" + file_base[:2] + "_log" + str(n) + ".txt", 'w')

        self.codings = open("codings/" + file_base[:2] + "_codings" + str(n) + ".txt", 'w')

        self.discontinuous = open("tallies/" + file_base[:2] + "_discont" + ".txt", 'w')

        self.coding_strings = []

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

        true_roots = []

        for i in ids:
            rel = self.doc.xpath("//sentence[@id=" + ident + "]/word[@id=" + i + "]/@relation")
            if not rel[0].startswith('Aux'):
                true_roots.append((i, rel[0]))

        if len(true_roots) == 1:
            return true_roots[0]
        elif len(true_roots) > 1:
            # don't care if sentence doesn't have a finite verb
            # 'v' must be finite, non-imperative

            verb = False

            for i in true_roots:
                if self.FINITE_VERB.match(i[1]):
                    verb = True
                    break

            if verb:
                print "More than 2 roots here: " + ident
                print
                sys.exit(0)
            else:
                print >> self.log, "Skipped sentence " + ident + " because no finite verb."
                print >> self.log
                return None

        else:
            print >> self.log, "Skipped " + ident + " because no 'true' root."
            print >> self.log

    def _split_coord(self, ident):
        """Return a list of @ids (indices) of words with PRED_CO relation."""

        lst = self.doc.xpath("//sentence[@id=" + ident + "]/word[@relation='PRED_CO']/@id")

        if lst:
            return lst
        else:
            return self.doc.xpath("//sentence[@id=" + ident + "]/word[@relation='PRED']/@id")

    def _code_clause(self, ident, root):
        """Returns a coding string identical to that produced by clause_types.c."""

        coding_string = ""

        rtree = self.trees[ident].dependencies[root]

        subj_head = ""
        obj_head = ""

        # type of verb
        # 'v' must be finite, non-imperative

        if self.FINITE_VERB.match(rtree.postag):
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
            if self.FINITE_VERB.match(stree.postag) and int(stree.root) in rtree.deps and not self.recursed and not stree.root == rtree.root:
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
            if found:
                break
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

        try:
            if max(heads) < int(rtree.root):
                coding_string += "t"
            elif max(heads) > int(rtree.root):
                coding_string += "f"
            else:
                coding_string += "-"
        except ValueError:
            coding_string += "-" 

        return coding_string

    def clause_types(self):
        """Returns a dict where keys = sentence IDs and values = coding strings identical to that produced by clause_types.c."""

        results = {}

        for ident in self.sentences:
            try:
                root_id, root_type = self._classify_root(ident)
                if root_type == "PRED":
                    results[ident] = [self._code_clause(ident, root_id)]
                    results[ident] += self.tmp
                    self.recursed = False
                elif root_type.find('ExD') != -1:
                    results[ident] = [self._code_clause(ident, root_id)]
                    results[ident] += self.tmp
                    self.recursed = False
                elif root_type.find('COORD') != -1 or root_type.find('PRED_CO') != -1:
                    lst = []
                    for clause_head in self._split_coord(ident):
                        lst.append(self._code_clause(ident, clause_head))
                        lst = lst + self.tmp
                        self.recursed = False
                    results[ident] = lst
                elif root_type.find('ADV') != -1 or root_type.find('ATR') != -1 or root_type.find('APOS') != -1 or root_type.find('SBJ') != -1:
                    results[ident] = [self._code_clause(ident, root_id)]
                    results[ident] += self.tmp
                    self.recursed = False
                elif root_type.find('OBJ') != -1:
                    print >> self.log, "Skipped " + ident + " because no 'true' root."
                    print >> self.log
                else:
                    print "Found an unknown root type!"
                    print ident, root_id, root_type
                    sys.exit(0)
            except TypeError:
                pass

        for ident in results:
            if not results[ident]:
                print >> self.log, "No coding string for " + ident + "."
                print >> self.log
            for i in results[ident]:
                if len(i) > 18:
                    print ident, i
                self.coding_strings.append(i)

        return results
                        
    def print_coding_strings(self):
        """Print coding strings, one per line."""

        for s in self.coding_strings:
            print >> self.codings, s

    def classify_discontinuous(self, rel):
        """Classify discontinuous phrases with relation 'rel'."""

        yxxv = 0
        xxv = 0
        yxvx = 0
        xvx = 0
        vxx = 0

        rel_re = re.compile(rel)

        try:
            for tok in self.trees.values():
                for s in tok.list_form.values():
                    if rel_re.match(s[3]) and s[6] == False:
                        disc_root = s[1]
                        disc_min = min(s[0])
                        disc_max = max(s[0])
                        if self.FINITE_VERB.match(tok.list_form[s[2]][4]):
                            verb_index = int(s[2])
                            clause = tok.list_form[s[2]][0]
                            if tok.list_form[s[2]][2] != '0':
                                clause.append(int(tok.list_form[s[2]][2]))
                            clause_beginning = min(clause)
                        
                            try:
                                if disc_max < verb_index and disc_min > clause_beginning:
                                    yxxv +=1
                                    #print "yxxv " + tok.id
                                    #print disc_root, disc_min, disc_max
                                    #print verb_index, clause_beginning
                                    #print
                                elif disc_max < verb_index:
                                    xxv += 1
                                    #print "xxv " + tok.id
                                    #print disc_root, disc_min, disc_max
                                    #print verb_index, clause_beginning
                                    #print
                                elif disc_min < verb_index and disc_max > verb_index and disc_min > clause_beginning:
                                    yxvx += 1
                                    #print "yxvx " + tok.id
                                    #print disc_root, disc_min, disc_max
                                    #print verb_index, clause_beginning
                                    #print
                                elif disc_min < verb_index and disc_max > verb_index:
                                    xvx += 1
                                    #print "xvx " + tok.id
                                    #print disc_root, disc_min, disc_max
                                    #print verb_index, clause_beginning
                                    #print
                                elif verb_index > disc_min:
                                    vxx += 1
                                    #print "vxx " + tok.id
                                    #print disc_root, disc_min, disc_max
                                    #print verb_index, clause_beginning
                                    #print
                            except UnboundLocalError:
                                pass             
        except KeyError:
            pass

        print "#...X...X...V: " + str(yxxv)
        print
        print "#X...X...V: " + str(xxv)
        print
        print "#...X...V...X: " + str(yxvx)
        print
        print "#X...V...X: " + str(xvx)
        print
        print "#(...)V...X...X: " + str(vxx)
        print

        return {'yxxv': yxxv, 'xxv': xxv, 'yxvx': yxvx, 'xvx': xvx, 'vxx': vxx}

    def classify_multicomps(self):
        """Classify ordering of direct and indirect objects in clauses with both."""

        pronoun = re.compile('p..---..-')

        acc_nom = re.compile('n-.---.a-')

        dat_nom = re.compile('n-.---.d-')

        verb = re.compile('[vt].......-')

        # list_form: [recurs_deps, head/root, subtree.head, subtree.relation, subtree.postag, subtree.lemma, subtree.continuity]

        do_first = 0
        io_first = 0

        try:
            for tok in self.trees.values():
                tok_objects = []

                for s in tok.list_form.values():
                    if s[3] == 'OBJ':
                        tok_objects.append(s)

                obj_pairs = []
                for s1 in tok_objects:
                    for s2 in tok_objects:
                        # check to see that both have the same head and that pair is non-trivial
                        if (s1[2] == s2[2] and s1[1] != s2[1] 
                            # check to see if head is verbal (incl. participle)
                            and verb.match(tok.list_form[s1[2]][4]) 
                            # check to see if either of the pair is a pronoun
                            and not pronoun.match(s1[4]) and not pronoun.match(s2[4]) 
                            # check to see if either of the pair is discontinuous and that one is dative and one is accusative
                            and s1[6] and s2[6]) and acc_nom.match(s1[4]) and dat_nom.match(s2[4]):
                            # prevents both (a,b) and (b,a) pairs being added
                            if (s2, s1) not in obj_pairs:
                                obj_pairs.append((s1, s2))

                for pair in obj_pairs:
                    print tok.id, pair
                    print
                    if max(pair[0][0]) < min(pair[1][0]):
                        do_first += 1
                    else:
                        io_first += 1

        except KeyError:
            pass

        return do_first, io_first

def main():

    parser = argparse.ArgumentParser(description='Process the input files.')
    parser.add_argument('-f', '--file_base', action = 'store', dest = "file_base", help='base of file names')
    parser.add_argument('-x', '--xml_file', action = 'store', dest = "xml_name", help='XML file')
    parser.add_argument('-d', '--classify_discontinuous', action = 'store_true', dest = "disc", help='Classify discontinuous DPs?')
    args = parser.parse_args()

    disc_master = {'yxxv': 0, 'xxv': 0, 'yxvx': 0, 'xvx': 0, 'vxx': 0}

    mult_master = {'DO_first': 0, 'IO_first': 0}

    if args.xml_name:
        seeker = Seeker('TS', args.xml_name, 0)

        file_base = args.xml_name.split('/')[1]

        disc_log = open("tallies/" + file_base[:2] + "_discont.txt", 'w')
        mult_log = open("tallies/" + file_base[:2] + "_mult.txt" , 'w')

        if args.disc:
            dct = seeker.classify_discontinuous('OBJ')
            
            for kind in dct:
                disc_master[kind] += dct[kind]
        do, io = seeker.classify_multicomps()
        mult_master['DO_first'] += do
        mult_master['IO_first'] += io
        #seeker.clause_types()
        #seeker.print_coding_strings()
    elif args.file_base:
        n = 1

        disc_log = open("tallies/" + args.file_base[:2] + "_discont.txt", 'w')
        mult_log = open("tallies/" + args.file_base[:2] + "_mult.txt" , 'w')

        while n < 25:
            seeker = Seeker(args.file_base, "xml/" + args.file_base + str(n) + ".xml", n) 
            if args.disc:
                dct = seeker.classify_discontinuous('OBJ')
                for kind in dct:
                    disc_master[kind] += dct[kind]
            seeker.classify_multicomps()
            do, io = seeker.classify_multicomps()
            mult_master['DO_first'] += do
            mult_master['IO_first'] += io
            #seeker.clause_types()
            #seeker.print_coding_strings()
            n += 1

        print '\a'

    print >> mult_log, "DO before IO = " + str(mult_master['DO_first'])
    print >> mult_log
    print >> mult_log, "IO before DO = " + str(mult_master['IO_first'])
    print >> mult_log

    if args.disc:
        print >> disc_log, "#...X...X...V: " + str(disc_master['yxxv'])
        print >> disc_log
        print >> disc_log, "#X...X...V: " + str(disc_master['xxv'])
        print >> disc_log
        print >> disc_log, "#...X...V...X: " + str(disc_master['yxvx'])
        print >> disc_log
        print >> disc_log, "#X...V...X: " + str(disc_master['xvx'])
        print >> disc_log
        print >> disc_log, "#(...)V...X...X: " + str(disc_master['vxx'])
        print >> disc_log

if __name__ == '__main__':
    main()