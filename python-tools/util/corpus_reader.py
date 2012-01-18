# This Python file uses the following encoding: utf-8

"""
corpus_reader2.py
Created 2011/12/14
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import sys
import re
from sets import Set
import nltk.tree as T

class myT(T.ParentedTree):

    def get_siblings(self):
        """Return a list of all the children of the top node."""

        subtrs = self.subtrees()

        # pop the first
        subtrs.next()

        first = subtrs.next()

        sibs = [first]

        curr = first

        done = False

        while not done:
            new = curr.right_sibling
            if new == None:
                done = True
            else:
                sibs.append(new)
                curr = new

        return sibs

class Token():
    """A class for Penn-style parsed trees."""
    #TODO: represent lemmas in the data structure separately from pos?
    
    def __init__(self, str):
        """Initialize a token."""

        # _tree contains the token as an nltk Tree
        self._tree = T.ParentedTree(str)
        
        # id contains the token's ID as a string "Corpus,Book:[milestones].num
        self.id = ""

        # id_num contains the numerical index of the ID as an integer
        self.id_num = 0

        # id_tree contains the ID subtree
        self.id_tree = ""
        
        # corpus contains the corpus part of the ID as a string
        self.corpus = ""

        # book contains the book (= filename) part of the ID as a string
        self.book = ""

        # milestones contains all the milestones in a particular token
        self.milestones = []
        
        # words contains all the words in a sentence token, exclusive of punctuation, as a list
        # excludes lemmas, if dash format
        self.words = []

        # text contains all the words in a sentence token, including punctuation, as a list
        # excludes lemmas, if dash format
        self.text = []
            
        # pos contains all the words in a sentence token with no punctuation or empty categories as a list of tuples
        # in which the first item is a Greek word and the second a POS tag
        self.pos = []

        # comments contains any comments in the token, as a list of strings
        self.comments = []

        # todos contains any TODOs in the token, as a list of strings
        self.todos = []

        # mans contains any MANs in the token, as a list of string
        self.mans = []

        # root contains the top-most phrase structure label, e.g., IP-MAT
        self.root = ""

        # main_tree contains the root subtree
        self.main_tree = ""

        # metadata contains the METADATA sub-tree if present
        self.metadata = ""

    def parse(self, tree, format):
        """Fill Token data structure."""
        
        # finds METADATA node, stores it, and then removes it so as not to interfere with word count, etc.
        for tr in tree.subtrees():
            if tr.node == "METADATA":
                self.metadata = tr
                self.main_tree = tr.right_sibling
                if self.main_tree.right_sibling:
                    self.id_tree = self.main_tree.right_sibling
                    tree = T.Tree("", [self.main_tree, self.id_tree])
                    tree = T.ParentedTree.convert(tree)
                else:
                    tree = T.Tree("", [self.main_tree])

        id_str = re.compile("^(.*),(.*):[0-9_;a-z]*\.([0-9]*)$")

        alt_id_str = re.compile("^(.*),(.*)\.([0-9]*)$")

        # finds $ROOT and stores in self.root

        subtrs = []

        for tr in tree.subtrees():
            subtrs.append(tr)

        self.main_tree = subtrs[1]

        self.root = self.main_tree.node

        ortho_lemma = re.compile("(.*)-(.*)")
        
        # gathers remaining info        
        for tup in tree.pos():
            tag = tup[1]
            leaf = tup[0]
            if leaf.find("{VS:") != -1:
                self.milestones.append(leaf)
            elif leaf.find("{COM:") != -1:
                self.comments.append(leaf)
            elif leaf.find("{MAN:") != -1:
                self.mans.append(leaf)
            elif leaf.find("{TODO:") != -1:
                self.todos.append(leaf)
            elif leaf.find("{BKMK}") != -1:
                pass
            elif tag == "ID":
                self.id = leaf
                try:
                    id_stuff = id_str.match(leaf)
                    self.corpus = id_stuff.group(1)
                    self.book = id_stuff.group(2)
                    self.id_num = id_stuff.group(3)
                except AttributeError:
                    id_stuff = alt_id_str.match(leaf)
                    self.corpus = id_stuff.group(1)
                    self.book = id_stuff.group(2)
                    self.id_num = id_stuff.group(3)                    
            # catches punctuation. allowed punctuation POS tags are , . "
            elif tag.find(",") != -1 or tag.find(".") != -1 or tag.find("\"") != -1:
                self.text.append(leaf)
            # catches empty categories so that they don't get added to text or words
            elif leaf.find("*") != -1 or leaf.find("0") != -1:
                self.pos.append((leaf, tag))
            # catches null pieces of split words so that they don't get added to text or words
            elif leaf == "@":
                self.pos.append((leaf, tag))
            # catches (FORMAT dash)
            elif leaf == "dash":
                break
            # deep format
            elif tag.find("ORTHO") != -1:
                if leaf.find("*") == -1 and leaf.find("0") == -1:
                    self.text.append(leaf)
                    self.words.append(leaf)
            # catches everything else = just words
            else:
                if format == "old":
                    self.text.append(leaf)
                    self.pos.append((leaf, tag))
                    self.words.append(leaf)
                elif format == "dash":
                    try:
                        match = ortho_lemma.match(leaf)
                        ortho = match.group(1)
                        lemma = match.group(2)
                        self.text.append(ortho)
                        self.pos.append(((ortho, lemma), tag))
                        self.words.append(ortho)
                    except AttributeError:
                        print "Something went wrong here:" + leaf
                        print
                        print "...in this tree:"
                        print
                        print self._tree.pprint()
                        print

    def has_milestone_first(self):
        """Check to see that the tree starts with a (CODE {VS:...}) milestone."""
        """Move any non-content (i.e., CODE) nodes preceding an initial milestone after the milestone."""

        tree = myT(self.main_tree.pprint())

        subtrs = tree.subtrees()

        # pop the first
        subtrs.next()

        count = 1

        content = False

        code_nodes = []

        # checking tokens to see if CODE and/or milestone first
        while not content:
            curr = subtrs.next()
            if curr.node == "FORMAT":
                return True
            elif curr.node == "CODE":
                if count == 1 and curr.pos()[0][0].find("VS:") != -1:
                    return True
                elif curr.pos()[0][0].find("VS:") != -1:
                    code_nodes.append(curr)
                    count += 1
                    mile = curr
                    content = True
                else:
                    code_nodes.append(curr)
                    count += 1
            else:
                return False

        sibs = tree.get_siblings()

        start = False

        new_tree = []

        for sib in sibs:
            if start:
                new_tree.append(sib)
            elif sib == mile:
                start = True
            else:
                pass

        for node in code_nodes:
            new_tree.insert(0, node)

        self.main_tree = T.Tree(self.root, new_tree)
        new_wrapped = T.Tree("", [self.metadata, self.main_tree, self.id_tree])
        self._tree = T.ParentedTree.convert(new_wrapped)

        print "Switching the order of some CODE nodes to put milestones first..."
        print
        return True

    def change_POS(self, new_tag, append, index, postr):
        """Change the POS tag of the given postr subtree to new_tag with any appends or indices provided."""

        new_postr = T.Tree(new_tag + append + index, [postr[0]])
        
        self._tree[postr.treepos] = T.ParentedTree.convert(new_postr)

class Corpus():
    """A class for a database of Penn-style parsed trees."""

    def __init__(self):

        # trees contains keys = numerical indices corresponding to sequence of tokens in file and values = Token instances
        self.tokens = {}
        
        self.format = ""

        self.re_index = re.compile("(.*)([-=][0-9])")

        self.re_pass = re.compile("(.*)-PASS.*")

    def load(self, trees):
        """Initializes Token objects and fills Corpus instance."""

        count = 0

        for tree in trees:
            if tree != "":
                tok = Token(tree)
                if count == 0:
                    if tree.find("VERSION") != -1:
                        self.parse_version(tok._tree)
                    else:
                        print
                        print "This corpus file is in the old format."
                        print
                        self.format = "old"
                tok.parse(tok._tree, self.format)
                self.tokens[count] = tok
                count += 1

    def parse_version(self, tree):
        """Record what format the corpus file is in."""

        pos_list = tree.pos()
        if pos_list[0][0] == "dash":
            print
            print "This corpus file is in the 'dash' format."
            print
            self.format = "dash"
        elif pos_list[0][0] == "deep":
            print
            print "This corpus file is in the 'deep' format."
            print
            self.format = "deep"
            
    def check_for_ids(self, output):
        """Check to see that all trees have ID nodes."""
        
        for key in self.tokens.keys():
            tree = self.tokens[key]
            if tree.id == "" and tree.root != "VERSION":
                print
                print "Missing ID node in tree!"
                print
                print tree._tree
                print
                if output:
                    print "From .out file."
                else:
                    print "From main corpus file."
                print
                print "Please run Corpus Reader with -i flag to renumber IDs and then try again."
                print
                sys.exit()

        return True

    def check_seq_ids(self):
        """Check to see that all ID numbers are sequential."""

        old_num = 0

        for key in self.tokens.keys():
            tree = self.tokens[key]
            num = int(tree.id_num)
            if num != old_num + 1 and tree.id != "":
                print
                print "Tokens not sequentially numbered!"
                print
                print "Please run Corpus Reader with -i flag to renumber IDs and then try again."
                print
                sys.exit()
            old_num = num

        return True

    def check_milestones(self):
        """Check to see that every token starts with a (CODE {VS:...}) milestone."""

        for key in self.tokens.keys():
            tree = self.tokens[key]
            if not tree.has_milestone_first():
                print "Some token(s) didn't have milestones. Adding milestones now..."
                print
                return False

        return True

    def word_count(self):
        """Count all and only the words in the .psd file."""

        word_count = 0

        keys = self.tokens.keys()

        for key in keys:
            tok = self.tokens[key]
            for word in tok.words:
                word_count += 1
        
        print "# # # # # # # # # # # # # # # #"        
        print
        print "There are " + str(word_count) + " words in this file, excluding empty categories and punctuation."

        if self.check_for_ids(False):
            print
            print "All sentences have IDs!"

        if self.check_seq_ids():
            print
            print "All IDs in sequence!"
            print
            print "# # # # # # # # # # # # # # # #"

    def renumber_ids(self, filename):
        """Renumber/add IDs in the .psd file."""

        if not self.check_milestones():
            print
            print "Please run Corpus Reader with the -m option to add continuity \
milestones before you renumber and/or add ID nodes!"
            print
            sys.exit()
        else:
            milestone = re.compile("{VS:([0-9]+_[0-9]+[a-z]*)}")
            count = 1
            corp = ""
            bk = ""
            for key in self.tokens.keys():
                tree = self.tokens[key]
                num_milestones = len(tree.milestones)
                ms_lst = ""
                for ms in tree.milestones:
                    match = milestone.match(ms)
                    ms_lst = ms_lst + match.group(1) + ";"
                if tree.root != "VERSION":
                    if count == 1:
                        if tree.corpus == "" or tree.book == "":
                            tree.corpus = raw_input("What is the name of your corpus? ")
                            corp = tree.corpus
                            tree.book = raw_input("What is the book (= filename with the extension)? ")
                            bk = tree.book
                        else:
                            corp = tree.corpus
                            bk = tree.book
                    ## print "Old ID was " + tree.id
                    ## print
                    tree.id = corp + "," + bk + ":" + ms_lst[:-1] + "." + str(count)
                    tree.id_num = count
                    tree.id_tree = T.Tree("ID", [tree.id])
                    new_tree = T.Tree("", [tree.metadata, tree.main_tree, tree.id_tree])
                    tree._tree = T.ParentedTree.convert(new_tree)
                    ## print "New ID is " + tree.id
                    ## print
                    count += 1

            self.print_trees(filename)
                
    def add_milestones(self, filename):
        """Add continuity milestones in the .psd file."""

        milestone = re.compile("{VS:([0-9]+_[0-9]+)([a-z]*)}")

        if not self.check_milestones():
            lst_milestone = ""
            lst_letter = 96
            for key in self.tokens.keys():
                tree = self.tokens[key]
                num_milestones = len(tree.milestones)
                # when milestones in the tree
                try:
                    match = milestone.match(tree.milestones[num_milestones - 1])
                    if not tree.has_milestone_first():
                        if lst_letter != 97:
                            lst_letter += 1
                        leaf = T.ParentedTree("CODE", ["{VS:" + lst_milestone + chr(lst_letter) + "}"])
                        tree.milestones.insert(0, "{VS:" + lst_milestone + chr(lst_letter) + "}")
                        # insert milestone as first leaf of main tree
                        tree.main_tree.insert(0, leaf)
                        # rebuild tree with wrapper
                        new_tree = T.Tree("", [tree.metadata, tree.main_tree, tree.id_tree])
                        tree._tree = T.ParentedTree.convert(new_tree)
                    elif match.group(2) != "":
                        lst_letter += 1
                        leaf = T.ParentedTree("CODE", ["{VS:" + lst_milestone + chr(lst_letter) + "}"])
                        tree.milestones[0] = "{VS:" + lst_milestone + chr(lst_letter) + "}"
                        # replace milestone as first leaf of main tree
                        tree.main_tree[0] = leaf
                        # rebuild tree with wrapper
                        new_tree = T.Tree("", [tree.metadata, tree.main_tree, tree.id_tree])
                        tree._tree = T.ParentedTree.convert(new_tree)
                    lst_milestone = match.group(1)
                    try:
                        lst_letter = ord(match.group(2))
                    except TypeError:
                        lst_letter = 96
                # when no milestones in the tree
                except IndexError:
                    if tree.root != "VERSION":
                        lst_letter += 1
                        leaf = T.ParentedTree("CODE", ["{VS:" + lst_milestone + chr(lst_letter) + "}"])
                        tree.milestones.append(lst_milestone)
                        # insert milestone as first leaf of main tree
                        tree.main_tree.insert(0, leaf)
                        # rebuild tree with wrapper
                        new_tree = T.Tree("", [tree.metadata, tree.main_tree, tree.id_tree])
                        tree._tree = T.ParentedTree.convert(new_tree)
                        
        self.print_trees(filename)

    def print_trees(self, filename):
        """Just print the trees from an input file."""
        # (i.e., remove CS comment blocks from .out files)

        out_name = filename + ".new"

        out_file = open(out_name, "w")

        for key in self.tokens.keys():
            tree = self.tokens[key]
            print >> out_file, tree._tree,
            print >> out_file, "\n\n",

    def replace_tokens(self, filename, corpus2):
        """Replace tokens in .psd file with edited tokens from output file."""

        self.word_count()

        out_name = filename + ".new"

        out_file = open(out_name, "w")

        index = 0

        out_ids = []

        for key in corpus2.tokens.keys():
            tree = corpus2.tokens[key]
            out_ids.append(tree.id)

        if self.check_for_ids(False) and corpus2.check_for_ids(True) and self.check_seq_ids():
            for key in self.tokens.keys():
                tree = self.tokens[key]
                if tree.id in out_ids and tree.id == corpus2.tokens[index].id:
                    print >> out_file, corpus2.tokens[index]._tree,
                    print >> out_file, "\n\n",
                    index += 1
                else:
                    print >> out_file, tree._tree,
                    print >> out_file, "\n\n",

    def swap(self, filename, map_file):
        """Insert the POS tags from the map file into the corpus file."""
        
        lemmatized = False
        lem = raw_input("Is your current .psd file lemmatized? Please enter t or f. ")
        print
        if lem == "t":
            lemmatized = True

        new_tags = []

        for line in map_file:
            pair = line.split()
            word_lemma = pair[0]
            tag = pair[1]
            if not lemmatized:
                wl = word_lemma.split("-")
                word = wl[0]
                new_tags.append((word, word_lemma, tag))
            else:
                new_tags.append((word_lemma, word_lemma, tag))

        for key in self.tokens.keys():
            tree = self.tokens[key]
            leaves = tree._tree.leaves()
            # get all the subtrees at the POS level
            for tr in tree._tree.subtrees():
                if tr[0] in leaves:
                    word = tr[0]
                    tag = tr.node
                    ind_match = re_index.match(tag)
                    pass_match = re_pass.match(tag)
                    if ind_match:
                        index = ind_match.group(2)
                    else:
                        index = ""
                    if pass_match:
                        append = "-PASS"
                    else:
                        append = ""
                    if word == new_tags[0][0]:
                        tree.change_POS(new_tags[0][2], append, index, tr)
                        new_tags.pop(0)

        self.print_trees(filename)

    def correct_by_lemma(self, filename, lem_file):
        """Replace the POS tags of words having certain lemmas."""
        
        #TODO: make this not hard-coded?
        comp_and_sup = ["ADJR","ADJS","ADVR","ADVS","QR","QS"]

        lemmas = {}

        for line in lem_file:
            triple = line.split()
            lemmas[triple[0]] = [triple[2], False, False]
            attrs = triple[1].split(",")
            if "case" in attrs:
                lemmas[triple[0]][1] = True
            if "number" in attrs:
                lemmas[triple[0]][2] = True

        for key in self.tokens.keys():
            tree = self.tokens[key]
            leaves = tree._tree.leaves()
            # get all the subtrees at the POS level
            for tr in tree._tree.subtrees():
                if tr[0] in leaves:
                    pair = tr[0]
                    if "-" in pair:
                        spl = pair.split("-")
                        word = spl[0]
                        lemma = spl[1]
                    else:
                        lemma = ""
                    tag = tr.node
                    ind_match = self.re_index.match(tag)
                    pass_match = self.re_pass.match(tag)
                    if ind_match:
                        index = ind_match.group(2)
                        tag = ind_match.group(1)
                    else:
                        index = ""
                    if pass_match:
                        append = "-PASS"
                        tag = pass_match.group(1)
                    else:
                        append = ""
                    if lemma in lemmas.keys():
                        lem_to_change = lemmas[lemma]
                        new_tag = lem_to_change[0]
                        case = lem_to_change[1]
                        number = lem_to_change[2]
                        if case and number:
                            if tag.endswith("S$"):
                                tree.change_POS(new_tag + "S$", append, index, tr)
                            elif tag.endswith("SA"):
                                tree.change_POS(new_tag + "SA", append, index, tr)
                            elif tag.endswith("SD"):
                                tree.change_POS(new_tag + "SD", append, index, tr)
                            elif tag.endswith("S"):
                                tree.change_POS(new_tag + "S", append, index, tr)
                            elif tag.endswith("$"):
                                tree.change_POS(new_tag + "$", append, index, tr)
                            elif tag.endswith("A"):
                                tree.change_POS(new_tag + "A", append, index, tr)
                            elif tag.endswith("D"):
                                tree.change_POS(new_tag + "D", append, index, tr)
                            elif tag in comp_and_sup:
                                pass
                            else:
                                tree.change_POS(new_tag, append, index, tr)
                        elif case:
                            if "$" in tag:
                                tree.change_POS(new_tag + "$", append, index, tr)
                            elif tag.endswith("A"):
                                tree.change_POS(new_tag + "A", append, index, tr)
                            elif tag.endswith("D"):
                                tree.change_POS(new_tag + "D", append, index, tr)
                            elif tag in comp_and_sup:
                                pass
                            else:
                                tree.change_POS(new_tag, append, index, tr)
                        else:
                            tree.change_POS(new_tag, append, index, tr)
                            
        self.print_trees(filename)
        
def main():

    flag = ""

    # boolean for whether file is CorpusSearch output file format
    out = False
    
    try:
        if sys.argv[1].startswith("-"):
            flag = sys.argv.pop(1)
        # name of main .psd file interested in reading
        filename = sys.argv.pop(1)
        in_trees = read(filename)
        corpus = Corpus()
        corpus.load(in_trees)
    except IndexError:
        print "usage: corpus-reader2.py [-flag] .psd-file [.psd.out-file]"
        print
        print "flags:"
        print "-c to count words"
        print "-i to renumber IDs"
        print "-m to add continuity milestones"
        print "-p to print just the trees from a CS .out file"
        print "-r to replace tokens from output file"
        sys.exit(1)

    if flag == "-c":
        corpus.word_count()
    elif flag == "-i":
        corpus.renumber_ids(filename)
    elif flag == "-m":
        corpus.add_milestones(filename)
    elif flag == "-p":
        corpus.print_trees(filename)
    elif flag == "-r":
        out = True
        output_filename = sys.argv.pop(1)
        out_trees = read(output_filename, out)
        corpus2 = Corpus()
        corpus2.load(out_trees)
        corpus.replace_tokens(filename, corpus2)
    else:
        select(corpus, filename)

def read(filename):
    """Read in a .psd file and return a list of trees as strings."""

    in_str = ""
    
    # boolean for whether currently in comment block in CorpusSearch output file
    comment = False

    # method for getting trees out of CorpusSearch output file
    in_file = open(filename, "rU")

    for line in in_file:
        if line.startswith("/*") or line.startswith("/~*"):
            comment = True
        elif not comment:
            in_str = in_str + line
        elif line.startswith("*/") or line.startswith("*~/"):
            comment = False
        else:
            pass

    trees = in_str.split("\n\n")

    return trees

def select(corpus, filename):
    """Select another CR function from a menu."""

    #TODO: write the selector for less common functions!
    print "Select a function:"
    print "    a. Correct the POS tags of words bearing certain lemmas in a corpus file."""
    print "    b. Swap the POS tags in a corpus file with those from a map file."
    print

    selection = raw_input("Please enter the letter of the function you would like to run. ")
    print
    if selection == "a":
        try:
            lem_file = open(sys.argv.pop(1), "rU")
            corpus.correct_by_lemma(filename, lem_file)
        except IndexError:
            print "You need to enter the name of the map file on the command line to run this function!"
            print
    elif selection == "b":
        try:
            map_file = open(sys.argv.pop(1), "rU")
            corpus.swap(filename, map_file)
        except IndexError:
            print "You need to enter the name of the map file on the command line to run this function!"
            print
    else:
        print "I'm sorry--I don't understand what you entered."
        print
        sys.exit()

if __name__ == "__main__":
    main()


