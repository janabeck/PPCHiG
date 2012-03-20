# This Python file uses the following encoding: utf-8

"""
corpus_reader.py
Created 2011/12/14
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import sys
import re
import argparse
import datetime
import dateutil.parser
import operator
import traceback
import warnings
import codecs
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

    #END_DEF get_siblings

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

        # text contains all the words in a sentence token, including punctuation and milestones, as a list
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

    #END_DEF __init__

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

        punct_tags = [',', '.', '\'', '\"', '`', 'LPAREN', 'RPAREN']
        
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
            elif tag.find("CODE") != -1:
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
            # catches punctuation. allowed punctuation POS tags are , . ' " ` LPAREN RPAREN
            elif tag in punct_tags:
                self.text.append(leaf.split("-")[0])
            # catches empty categories so that they don't get added to text or words
            elif leaf.find("*") != -1 or leaf.find("0") != -1:
                pass
            # catches null pieces of split words so that they don't get added to text or words
            elif leaf == "@":
                pass
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
                        if lemma in corpus.lemmas:
                            forms = corpus.lemmas[lemma]
                            if ortho in forms:
                                forms[ortho] += 1
                            else:
                                forms[ortho] = 1
                        else:
                            corpus.lemmas[lemma] = {}
                            corpus.lemmas[lemma][ortho] = 1
                            
                    except AttributeError:
                        print "Something went wrong here:" + leaf
                        print
                        print "...in this tree:"
                        print
                        print self._tree.pprint()
                        print
    
    #END_DEF parse

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
                    # insert milestone CODE node to make sure it's always first
                    code_nodes.insert(0, curr)
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

        while len(code_nodes) > 0:
            length = len(code_nodes)
            # last in, first out
            this = code_nodes.pop(length - 1)
            new_tree.insert(0, this)

        self.main_tree = T.Tree(self.root, new_tree)
        new_wrapped = T.Tree("", [self.metadata, self.main_tree, self.id_tree])
        self._tree = T.ParentedTree.convert(new_wrapped)

        print "Switching the order of some CODE nodes to put milestones first..."
        print
        return True

    #END_DEF has_milestone_first

    def change_POS(self, new_tag, append, index, postr):
        """Change the POS tag of the given postr subtree to new_tag with any appends or indices provided."""

        new_postr = T.Tree(new_tag + append + index, [postr[0]])
        
        self._tree[postr.treepos] = T.ParentedTree.convert(new_postr)

    #END_DEF change_POS

    def split_POS(self, tag1, tag2, lem1, lem2, append, index, postr, word1, word2):
        """Split a word into two halves with the same lemma."""

        pair1 = str((unicode(word1.decode('utf-8')) + "-" + lem1).encode('utf-8'))

        pair2 = str((unicode(word2.decode('utf-8')) + "-" + lem2).encode('utf-8'))
        
        new_postr = T.Tree(tag1 + append + index, [pair1])

        new_postr2 = T.Tree(tag2 + append + index, [pair2])

        position = len(postr.treepos) - 1

        ins_point = postr.treepos[position] + 1

        new_treepos = list(postr.treepos)

        addy = new_treepos[:-1]

        addy = tuple(addy)
        
        ptree = self._tree[addy]

        ptree[ins_point - 1] = T.ParentedTree.convert(new_postr)

        ptree.insert(ins_point, T.ParentedTree.convert(new_postr2))

            #END_DEF split_POS
    
#END_DEF Token

class Corpus():
    """A class for a database of Penn-style parsed trees."""

    def __init__(self):

        # trees contains keys = numerical indices corresponding to sequence of tokens in file and values = Token instances
        self.tokens = {}
        
        self.format = ""

        self.re_index = re.compile("(.*)([-=][0-9])")

        self.re_pass = re.compile("(.*)-PASS.*")

        # lemmas is a dict keyed by the lemma, with the value itself a dict keyed by word-form (with freq as value)
        self.lemmas = {}

    #END_DEF __init__

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

    #END_DEF load

    def parse_version(self, tree):
        """Record what format the corpus file is in."""

        pos_list = tree.pos()
        if pos_list[0][0] == "dash":
            print
            print  "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"
            print
            print "This corpus file is in the 'dash' format."
            print
            self.format = "dash"
        elif pos_list[0][0] == "deep":
            print
            print  "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"
            print
            print "This corpus file is in the 'deep' format."
            print
            self.format = "deep"

    #END_DEF parse_version
            
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

    #END_DEF check_for_ids

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

    #END_DEF check_seq_ids

    def check_milestones(self):
        """Check to see that every token starts with a (CODE {VS:...}) milestone."""

        for key in self.tokens.keys():
            tree = self.tokens[key]
            if not tree.has_milestone_first():
                print "Some token(s) didn't have milestones. Adding milestones now..."
                print
                return False

        return True

    #END_DEF check_milestones

    def word_count(self):
        """Count all and only the words in the .psd file."""
        """Returns word_count."""

        word_count = 0

        keys = self.tokens.keys()
        
        split = False

        for key in keys:
            tok = self.tokens[key]
            for word in tok.words:
                if word.endswith("@") and word != "@":
                    split = True
                elif word.startswith("@") and word != "@":
                    split = False
                    word_count +=1
                else:
                    word_count += 1

        return word_count

    #END_DEF word_count

    def print_word_count(self, word_count):
        """Prints the word count to the terminal."""

        print  "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"        
        print
        print "There are " + str(word_count) + " words in this file, excluding empty categories and punctuation."

        if self.check_for_ids(False):
            # print
            # print "All sentences have IDs!"
            pass

        if self.check_seq_ids():
            # print
            # print "All IDs in sequence!"
            print
            print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"
            print
            
    #END_DEF print_word_count

    def words_per_hour(self, filename, timelog):
        """Calculates and returns words_per_hour."""

        wc = self.word_count()

        time = re.compile("^.*at\s(.*).")

        intervals = []

        if filename.startswith("/Users/"):
            filematch = re.search("^.*?([0-9A-Za-z\-\.]*)$", filename)
            filename = filematch.group(1)

        for line in timelog:
            if line.find(filename) != -1:
                if line.find("Started") != -1:
                    strt = dateutil.parser.parse(time.match(line).group(1))
                elif line.find("Idled") != -1:
                    stp = dateutil.parser.parse(time.match(line).group(1))
                    intervals.append(stp - strt)
                elif line.find("Resumed") != -1:
                    strt = dateutil.parser.parse(time.match(line).group(1))
                elif line.find("Stopped") != -1:
                    stp = dateutil.parser.parse(time.match(line).group(1))
                    intervals.append(stp - strt)
                elif line.find("Saved") != -1:
                    pass
                else:
                    print "I didn't understand one of the lines in your timelog!"
                    print
                    print line
                    print
                    sys.exit()

        duration = datetime.timedelta()

        for interval in intervals:
            duration = duration + interval

        rate = wc / (duration.total_seconds() / 3600)

        hours, remainder = divmod(duration.total_seconds(), 3600)  
        minutes, seconds = divmod(remainder, 60)   

        if minutes >= 10:
            duration_formatted = '%s:%s' % (int(hours), int(minutes))
        else:
            duration_formatted = '%s:0%s' % (int(hours), int(minutes))

        return (wc, duration_formatted, int(rate))

    #END_DEF words_per_hour

    def print_wph(self, wph):
        """Prints the parsing speed to the terminal."""
        print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"
        print
        print "You parsed " + str(wph[0]) + " words in " + str(wph[1]) + ", for a rate of " + str(wph[2]) + " words per hour!"
        print
        print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"
        print

    #END_DEF print_wph
                    
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
                            tree.book = raw_input("What is the book (= filename without the extension)? ")
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

    #END_DEF renumber_ids
                
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

    #END_DEF add_milestones

    def print_trees(self, filename):
        """Just print the trees from an input file."""
        # (i.e., remove CS comment blocks from .out files)

        out_name = filename + ".new"

        out_file = open(out_name, "w")

        for key in self.tokens.keys():
            tree = self.tokens[key]
            print >> out_file, tree._tree,
            print >> out_file, "\n\n",

    #END_DEF print_trees

    def replace_tokens(self, filename, corpus2):
        """Replace tokens in .psd file with edited tokens from output file."""

        self.print_word_count(self.word_count())

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

    #END_DEF replace_tokens

    def split_words(self, filename):
        """Generate a dialog on the command line to split words with more than one POS tag."""

        self.print_word_count(self.word_count())

        exclude = re.compile("VB.*|VPR.*|BE.*|BPR.*")

        non_words = re.compile("dash|{|\*|0|Herodotus|GreekNT|@")

        #cases = ["NOM","GEN","ACC","DAT"]

        # for key in self.tokens.keys():
        #     tree = self.tokens[key]
        #     leaves = tree._tree.leaves()
        #     for tr in tree._tree.subtrees():
        #         if tr[0] in leaves:
        #             word = unicode(tr[0].decode('utf-8'))
        #             pair = word.split("-")
        #             rword = unicode(pair[0])
        #             if not non_words.match(word):
        #                 print word
        #                 lemma = pair[1]    

        # try:
        for key in self.tokens.keys():
            tree = self.tokens[key]
            leaves = tree._tree.leaves()
            for tr in tree._tree.subtrees():
                #dontask = False
                with warnings.catch_warnings(record=True):
                    if tr[0] in leaves:
                        word = unicode(tr[0].decode('utf-8'))
                        pair = word.split("-")
                        rword = unicode(pair[0])
                        if not non_words.match(word):
                            lemma = pair[1]
                        tag = tr.node
                        #for case in cases:
                        #    if tag.find(case) != -1:
                        #        dontask = True
                        #if not dontask:
                        ind_match = self.re_index.match(tag)
                        if ind_match:
                            index = ind_match.group(2)
                            tag = tag.replace(index, "")
                        else:
                            index = ""
                        if tag.find("-") != -1:
                            pair2 = tag.split("-")
                            tag1 = pair2[0]
                            tag2 = pair2[1]
                            sep = "-"
                        elif tag.find("+") != -1:
                            pair2 = tag.split("+")
                            tag1 = pair2[0]
                            tag2 = pair2[1]
                            sep = "+"
                        if (not exclude.match(tag)) and (tag.find("-") != -1 or tag.find("+") != -1) and (not word.find("*") != -1):
                            try:
                                (w1, w2, lemma, corr) = self.get_split(rword, lemma, tag1, tag2, sep)
                                if corr and isinstance(w1, tuple):
                                    if isinstance(lemma, tuple):
                                        tree.split_POS(w1[0], w2[0], lemma[0], lemma[1], "", index, tr, w1[1], w2[1])
                                    else:
                                        tree.split_POS(w1[0], w2[0], lemma, "@" + lemma + "@", "", index, tr, w1[1], w2[1])
                                elif corr:
                                    tree.split_POS(tag1, tag2, lemma, "@" + lemma + "@", "", index, tr, w1, w2)
                                elif not corr:
                                    tree.change_POS(tag1 + "+" + tag2, "", index, tr)
                            except TypeError:
                                pass
                                
        self.print_trees(filename)

    #END_DEF split_words

    def check(self, tag1, tag2, w1, w2, rword, lemma, sep):
        """Confirms word split."""
        
        corr = raw_input("Is this correct? The first part of the word will be: " + tag1 + " " + w1.encode('utf-8') \
                        + "\nand the second part of the word will be: " + tag2 + " "  + w2.encode('utf-8') + " ")
        print
        if corr == "y":
            pos = raw_input("Do you need to edit the POS tag for either word? ")
            print
            if pos == "y":
                t1 = raw_input("Enter the POS tag for the first word. ENTER for no change. ")
                if t1 != "":
                    tag1 = t1
                print
                t2 = raw_input("Enter the POS tag for the second word. ENTER for no change. ")
                if t2 != "":
                    tag2 = t2
                print
            lem = raw_input("Do you need to edit the lemma for either word? ")
            print
            if lem == "y":
                l1 = raw_input("Enter the lemma for the first word. ENTER for no change. ")
                if l1 != "":
                    lem1 = unicode(l1.decode('utf-8'))
                else:
                    lem1 = lemma
                print
                l2 = raw_input("Enter the lemma for the second word. ENTER for no change. ")
                if l2 != "":
                    lem2 = unicode(l2.decode('utf-8'))
                else:
                    lem2 = lemma
                print
                return ((tag1,w1.encode('utf-8')),(tag2,w2.encode('utf-8')),(lem1,lem2), corr)
            if pos == "y":
                return ((tag1,w1.encode('utf-8')),(tag2,w2.encode('utf-8')), lemma, corr)
            else:
                return (w1.encode('utf-8'), w2.encode('utf-8'), lemma, corr)

        else:
            self.get_split(rword, lemma, tag1, tag2, sep)

    #END_DEF check

    def get_split(self, rword, lemma, tag1, tag2, sep):
        """Returns w1 and w2, the first and second halves a split word."""

        bool = raw_input("Do you want to split this word? " + rword.encode('utf-8') + " " + tag1 + sep + tag2 + " ")
        print
        if bool == "y":
            ind = int(raw_input("Enter the index of the first letter of the second half of the word. "))
            print
            w1 = rword[:ind] + "@"
            w2 = "@" + rword[ind:]
            return self.check(tag1, tag2, w1, w2, rword, lemma, sep)
        else:
            print "OK, we won't split this word."
            print
            if sep == "-":
                pl = raw_input("Do you want to change the separator to a '+'? ")
                print
                if pl == "y":
                    return ("", "", lemma, False)
                print

    #END_DEF get_split

    def transform_case(self, filename):
        """Change case tags from non-hyphenated suffixes to hyphenated extensions."""
        #TODO: remove this and other Greek-specific methods before releasing with Annotald

        participle = re.compile("VPR*|BPR*")

        adj = ["ADJ", "ADJ$", "ADJA", "ADJD"]

        be = ["BPR", "BPR$", "BPRA", "BPRD", "BPRP", "BPRP$", "BPRPA", "BPRPD"]

        clpro = ["CLPRO", "CLPRO$", "CLPROA", "CLPROD"]

        clq = ["CLQ", "CLQ$", "CLQA", "CLQD"]

        det = ["D", "D$", "DA", "DD", "DS", "DS$", "DSA", "DSD"]

        noun = ["N", "N$", "NA", "ND", "NS", "NS$", "NSA", "NSD"]

        prnoun = ["NPR", "NPR$", "NPRA", "NPRD", "NPRS", "NPRS$", "NPRSA", "NPRSD"]

        other = ["OTHER", "OTHER$", "OTHERA", "OTHERD"]

        pro = ["PRO", "PRO$", "PROA", "PROD"]

        quant = ["Q", "Q$", "QA", "QD"]

        vb = ["VPR", "VPR$", "VPRA", "VPRD", "VPRP", "VPRP$", "VPRPA", "VPRPD"]

        wadj = ["WADJ", "WADJ$", "WADJA", "WADJD"]

        wd = ["WD", "WD$", "WDA", "WDD"]

        wpro = ["WPRO", "WPRO$", "WPROA", "WPROD"]

        cats = [adj, be, clpro, clq, det, noun, prnoun, other, pro, quant, vb, wadj, wd, wpro]

        dashes = ["NOM","GEN","ACC","DAT"]

        for key in self.tokens.keys():
            tree = self.tokens[key]
            leaves = tree._tree.leaves()
            # get all the subtrees at the POS level
            for tr in tree._tree.subtrees():
                verb = False
                reflexive = False
                compound = False
                special = False
                remainder = ""
                no_change = False
                if tr[0] in leaves:
                    word = tr[0]
                    tag = tr.node
                    for dash in dashes:
                        if tag.find(dash) != -1:
                            no_change = True
                    ind_match = self.re_index.match(tag)
                    if ind_match:
                        index = ind_match.group(2)
                        tag = tag.replace(index, "")
                    else:
                        index = ""
                    if "+" in tag and "SLF" in tag:
                        comp_group = tag.partition("+")
                        tag = comp_group[0]
                        remainder = "+" + comp_group[2]
                        reflexive = True
                        compound = True
                    elif "+" in tag and "NEG" in tag:
                        comp_group = tag.partition("+")
                        tag = comp_group[2]
                        remainder = comp_group[0] + "+"
                        compound = True
                    elif tag.find("POS") != -1 or tag.find("RCP") != -1:
                        comp_group = tag.partition("-")
                        tag = comp_group[0]
                        remainder = "-" + comp_group[2]
                        special = True
                    if participle.match(tag):
                        verb = True
                        verb_group = tag.partition("-")
                        tag = verb_group[0]
                        remainder = verb_group[2]
                    for lst in cats:
                        if tag in lst:
                            if tag.endswith("$"):
                                coretag = tag[:-1]
                                dash = "GEN"
                            elif tag.endswith("A"):
                                coretag = tag[:-1]
                                dash = "ACC"
                            elif len(tag) > 1 and tag.endswith("D"):
                                coretag = tag[:-1]
                                dash = "DAT"
                            else:
                                coretag = tag
                                dash = "NOM"
                            if not no_change:
                                if verb:
                                    tag = "-".join([coretag, remainder, dash])
                                elif compound:
                                    if reflexive:
                                        tag = "".join([coretag, remainder, "-" + dash])
                                    else:
                                        tag = "".join([remainder, coretag, "-" + dash])
                                elif special:
                                    tag = "".join([coretag, "-" + dash, remainder])
                                else:
                                    tag = "-".join([coretag, dash])
                                tree.change_POS(tag, "", index, tr)

        self.print_trees(filename)

    #END_DEF transform_case

    def transform_back(self, filename):
        """Transforms case tags back from dash tags into suffixes."""
        
        dashes = ["NOM","GEN","ACC","DAT"]
        
        participle = re.compile("VPR*|BPR*")
        
        for key in self.tokens.keys():
            tree = self.tokens[key]
            leaves = tree._tree.leaves()
            #get all the subtrees at the POS level
            for tr in tree._tree.subtrees():
                if tr[0] in leaves:
                    word = tr[0]
                    tag = tr.node
                    ind_match = self.re_index.match(tag)
                    if ind_match:
                        index = ind_match.group(2)
                        tag = tag.replace(index, "")
                    else:
                        index = ""
                    for dash in dashes:
                        remainder = ""
                        if dash in tag:
                            if "SLF" in tag:
                                tag = tag.replace("+SLF","")
                                remainder = "+SLF"
                            elif "POS" in tag:
                                tag = tag.replace("-POS","")
                                remainder = "POS"
                            elif "RCP" in tag:
                                tag = tag.repalce("-RCP","")
                                remainder = "RCP"
                            elif participle.match(tag):
                                verb_group = tag.partition("-")
                                tag = verb_group[0]
                                tmp = verb_group[2]
                                vg2 = tmp.rpartition("-")
                                remainder = vg2[0]
                            if dash == "NOM":
                                tag = tag.replace("-" + dash, "")
                            elif dash == "GEN":
                                tag = tag.replace("-" + dash, "")
                                tag = tag + "$"
                            elif dash == "ACC":
                                tag = tag.replace("-" + dash, "")
                                tag = tag + "A"
                            elif dash == "DAT":
                                tag = tag.replace("-" + dash, "")
                                tag = tag + "D"
                            if remainder == "":
                                tree.change_POS(tag, "", index, tr)
                            elif remainder.find("+") != -1:
                                tree.change_POS(tag + remainder, "", index, tr)
                            else:
                                tree.change_POS(tag + "-" + remainder, "", index, tr)
                            
        self.print_trees(filename)
        
    #END_DEF transform_back

    def swap(self, filename, map_file):
        """Insert the POS tags from the map file into the corpus file."""
        
        lemmatized = False
        lem = raw_input("Is your current .psd file lemmatized? Please enter t or f. ")
        print
        if lem == "t":
            lemmatized = True

        new_tags = []

        count = 0

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
                    ind_match = self.re_index.match(tag)
                    pass_match = self.re_pass.match(tag)
                    if ind_match:
                        index = ind_match.group(2)
                    else:
                        index = ""
                    if pass_match:
                        append = "-PASS"
                    else:
                        append = ""
                    try:
                        if word == new_tags[0][0]:
                            tree.change_POS(new_tags[0][2], append, index, tr)
                            new_tags.pop(0)
                            count += 1
                    except IndexError:
                        print "I think I reached the end of the file!"
                        print
                        print "Word count is " + str(count) + "."
                        print
                        break

        self.print_trees(filename)

    #END_DEF swap

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
                                if tag == "ADJR" and new_tag == "Q":
                                    tree.change_POS(new_tag + "R", append, index, tr)
                                elif tag == "ADJS" and new_tag == "Q":
                                    tree.change_POS(new_tag + "S", append, index, tr)
                                elif tag == "ADVR" and new_tag == "Q":
                                    tree.change_POS(new_tag + "R", append, index, tr)
                                elif tag == "ADVS" and new_tag =="Q":
                                    tree.change_POS(new_tag + "S", append, index, tr)
                                elif word == "πάντως" and new_tag == "Q":
                                    tree.change_POS(new_tag + "V", append, index, tr)
                                else:
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

    #END_DEF correct_by_lemma

    def pos_concordance(self):
        """Print a concordance of lemmas and POS tags in the corpus."""
        
        # dictionary keyed by POS tag with all the lemmas the tag applies to as values
        concordance = {}

        # dictionary keyed by (POS tag, lemma) tuple with frequency of lemma (per POS tag) as value
        lemmas = {}

        #dictionary keyed by POS tag with frequency of tag as value
        pos_freq = {}

        index = re.compile(".*[-=][0-9]")

        lst = open("pos-list.txt", "w")

        pos_out = open("pos-concordance.txt", "w")

        for key in self.tokens.keys():
            tree = self.tokens[key]
            for tup in tree.pos:
                if self.format == "dash":
                    lemma = tup[0][1]
                elif self.format == "old":
                    lemma = tup[0]
                else:
                    #TODO: support deep format
                    pass
                postag = tup[1]
                if index.match(postag):
                    tmp = re.sub("[-=][0-9]", "", postag)
                    postag = tmp
                try:
                    pos_freq[postag] += 1
                except KeyError:
                    pos_freq[postag] = 1
                if postag in concordance:
                    concordance[postag].add(lemma)
                    if (postag, lemma) in lemmas.keys():
                        lemmas[(postag, lemma)] += 1
                    else:
                        lemmas[(postag, lemma)] = 1
                else:
                    concordance[postag] = Set([lemma])
                    lemmas[(postag, lemma)] = 1

        keys_list = []
                    
        for key in concordance:
            keys_list.append(key)

        keys_list.sort()

        for key in keys_list:
            print >> lst, key + " (" + str(pos_freq[key]) + ")"
            print >> pos_out, key + ": "
            lem_list = sorted(concordance[key])
            for lemma in lem_list:
                print >> pos_out, lemma + " (" + str(lemmas[(key, lemma)]) + ")"
            print >> pos_out

    #END_DEF pos_concordance

    def category_concordance(self, cat_file):
        """Print a concordance of lemmas per category as defined in a input category definition file."""

        cat_line = re.compile("^(.*):\s(.*)$")

        index = re.compile(".*-[0-9]")

        cat_out = open("category-concordance.txt", "w")
        
        # dictionary with key = category name from cat def file, value = tuple of either list of tags or RE and dictionary of lemmas with key = lemma, value = freq
        categories = {}

        for line in cat_file:
            content = cat_line.match(line)
            name = content.group(1)
            desc = content.group(2)
            if desc.find(",") != -1:
                tags = desc.split(",")
                categories[name] = (tags, {})
            else:
                reg_desc = re.compile(desc)
                categories[name] = (reg_desc, {})

        for key in self.tokens.keys():
            tree = self.tokens[key]
            for tup in tree.pos:
                if self.format == "dash":
                    lemma = tup[0][1]
                elif self.format == "old":
                    lemma = tup[0]
                else:
                    #TODO: support deep format
                    pass
                postag = tup[1]
                if index.match(postag):
                    tmp = re.sub("-[0-9]", "", postag)
                    postag = tmp
                for cat in categories:
                    desc = categories[cat][0]
                    lemmas = categories[cat][1]
                    if isinstance(desc, list):
                       for tag in desc:
                           if postag == tag:
                               try:
                                   lemmas[lemma] += 1
                               except KeyError:
                                   lemmas[lemma] = 1
                               break
                    else:
                        if desc.match(postag):
                            try:
                                lemmas[lemma] += 1
                            except KeyError:
                                lemmas[lemma] = 1

        for cat in categories:
            lemmas = categories[cat][1]
            if lemmas:
                # following 2 lines give a representation of the lemmas dict reverse sorted by value
                sorted_lemmas = sorted(lemmas.iteritems(), key=operator.itemgetter(1))
                sorted_lemmas.reverse()
                print >> cat_out, cat + ":"
                for s in sorted_lemmas:
                    print >> cat_out, s[0] + " (" + str(s[1]) + ")"
                print >> cat_out

    #END_DEF category_concordance

    def unique_lemmas(self, sort):
        """Print all the unique lemmas (and their frequencies) in a corpus file."""

        lemmas = {}

        lem_out = open("unique-lemmas.txt", "w")

        for key in self.tokens.keys():
            tree = self.tokens[key]
            for tup in tree.pos:
                if self.format == "dash":
                    lemma = tup[0][1]
                elif self.format == "old":
                    print
                    print "I'm sorry, but this function is not compatible with the old corpus format."
                    print
                    sys.exit()
                else:
                    #TODO: support deep format
                    pass
                try:
                    lemmas[lemma] += 1
                except KeyError:
                    lemmas[lemma] = 1

        if sort == "freq":
            sorted_lemmas = sorted(lemmas.iteritems(), key=operator.itemgetter(1))
            sorted_lemmas.reverse()

            for tup in sorted_lemmas:
                print >> lem_out, tup[0] + ": " + str(tup[1])
        elif sort == "alpha":
            lem_list = []
            for lemma in lemmas.keys():
                lem_list.append(lemma)
            lem_list.sort()
            for lemma in lem_list:
                print >> lem_out, lemma + ": " + str(lemmas[lemma])

    #END_DEF unique_lemmas

    def lemma_concordance(self, lemma):
        """Print a concordance of the word forms (and their frequencies) for the given lemma."""

        if self.format != "dash":
            print "I'm sorry, but only the 'dash' format is supported for this function at the moment."
            print
            sys.exit()

        out_name = lemma + "-concordance.txt"

        out_file = open(out_name, "w")

        if lemma in self.lemmas:
            forms = self.lemmas[lemma]
            sorted_forms = sorted(forms.iteritems(), key=operator.itemgetter(1))
            sorted_forms.reverse()
            for form in sorted_forms:
                print >> out_file, form[0] + ": " + str(form[1])
        else:
            print "I'm sorry. I couldn't find your lemma. Please check the spelling and try again."
            print

    #END_DEF lemma_concordance

    def print_text(self, filename):
        """Print just the text (words, punctuation, milestones)."""

        out_name = filename.replace(".psd",".txt")

        out_file = open(out_name, "w")

        for key in self.tokens.keys():
            token = self.tokens[key]
            for word in token.text:
                print >> out_file, word

    #END_DEF print_text
    
    def print_words(self, filename):
        """Print just the words."""
        
        out_name = filename.replace(".psd",".txt")

        out_file = open(out_name, "w")
        
        split = False
        
        for key in self.tokens.keys():
            token = self.tokens[key]
            for word in token.words:
                if split:
                    tmp2 = word.replace("@","")
                    print >> out_file, tmp + tmp2
                    tmp = ""
                    split = False
                elif word.find("@") != -1:
                    tmp = word.replace("@","")
                    split = True
                else:
                    print >> out_file, word
                    
    #END_DEF print_words
                    
#END_DEF Corpus

corpus = Corpus()
                                
def main():

    parser = argparse.ArgumentParser(description='Process the input files and command line options.')
    # TODO: maybe gather additional filenames in a remainder arguments (see docs) instead of gathering into psd list?
    parser.add_argument('-c', '--count', dest='count', action='store_true', help='Print the word count.')
    parser.add_argument('-i', '--ids', dest='renumber_ids', action='store_true', help='Renumber the IDs in the .psd file.')
    parser.add_argument('-m', '--milestones', dest='add_milestones', action='store_true', help='Add continuity milestones to the .psd file.')
    parser.add_argument('-p', '--print', dest='print_trees', action='store_true', help='Print all the trees in the .psd file.')
    parser.add_argument('-r', '--replace', dest='output_file', action='store', help='Insert the tokens from a CorpusSearch output file into the main .psd corpus file.')
    parser.add_argument('-t', '--timelog', dest='timelog', action='store_const', const='timelog.txt', help='Calculate words per hour parsed from a timelog.txt.')
    parser.add_argument('-l', '--split_POS', dest='split', action='store_true', help='Split words that have more than one POS tag.')
    parser.add_argument('psd', nargs='+')
    args = parser.parse_args()

    corpus = Corpus()

    if len(args.psd) == 1:
        filename = args.psd[0]
        in_trees = read(filename)
        corpus.load(in_trees)
    else:
        response = raw_input("Is this your main corpus file " + args.psd[0] + "?\
        Enter y or n. ")
        print

        if response == "y":
            filename = args.psd[0]
            in_trees = read(filename)
            corpus.load(in_trees)
        else:
            print "You should enter the name of your .psd file *before* you enter the name of an additional input file when not using a command line option."
            print
            sys.exit()

    picked = False

    if args.count:
        corpus.print_word_count(corpus.word_count())
        picked = True

    if args.renumber_ids:
        corpus.renumber_ids(filename)
        picked = True

    if args.add_milestones:
        corpus.add_milestones(filename)
        picked = True

    if args.print_trees:
        corpus.print_trees(filename)
        picked = True

    if args.output_file:
        out_trees = read(args.output_file)
        corpus2 = Corpus()
        corpus2.load(out_trees)
        corpus.replace_tokens(filename, corpus2)
        picked = True

    if args.timelog:
        corpus.print_wph(corpus.words_per_hour(filename, open(args.timelog, 'rU')))
        picked = True

    if args.split:
        corpus.split_words(filename)
        picked = True
        
    if not picked:
        if len(args.psd) == 1:
            select(corpus, filename, "")
        else:
            select(corpus, filename, args.psd[1])

#END_DEF main

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

#END_DEF read

def select(corpus, filename, add_file):
    """Select another CR function from a menu."""

    #TODO: write the selector for less common functions!
    print "Select a function:"
    print "    a. Correct the POS tags of words bearing certain lemmas in a corpus file."
    print "    b. Swap the POS tags in a corpus file with those from a map file."
    print "    c. Print a concordance of lemmas and POS tags in the corpus."
    print "    d. Print a concordance of lemmas per category as defined in an input category definition file."
    print "    e. Print all the unique lemmas (and their frequences) in a corpus file."
    print "    f. Print a concordance of the word forms (and their frequencies) for the given lemma."
    print "    g. Print the text (words, punctuation, milestones) of the corpus file."
    print "    h  Print just the words of the corpus file."
    print "    i. Transform case suffixes into dash tags."
    print "    j. Transform case dash tags back into suffixes."
    print

    # TODO: probably replace try/except blocks below
    selection = raw_input("Please enter the letter of the function you would like to run. ")
    print
    if selection == "a":
        try:
            lem_file = open(add_file, "rU")
            corpus.correct_by_lemma(filename, lem_file)
        except IOError:
            #print traceback.print_exc(file=sys.stdout)
            print "You need to enter the name of the category definition file on the command line to run this function!"
            print
    elif selection == "b":
        try:
            map_file = open(add_file, "rU")
            corpus.swap(filename, map_file)
        except IOError:
            #print traceback.print_exc(file=sys.stdout)
            print "You need to enter the name of the category definition file on the command line to run this function!"
            print
    elif selection == "c":
        corpus.pos_concordance()
    elif selection == "d":
        try:
            cat_file = open(add_file, "rU")
            corpus.category_concordance(cat_file)
        except IOError:
            #print traceback.print_exc(file=sys.stdout)
            print "You need to enter the name of the category definition file on the command line to run this function!"
            print
    elif selection == "e":
        print "Would you like to sort the lemmas by frequency or alphabetically?"
        print
        sort = raw_input("Please type 'freq' to sort by frequency or 'alpha' to sort alphabetically. ")
        print
        corpus.unique_lemmas(sort)
    elif selection == "f":
        if add_file != "":
            lemma = add_file
            corpus.lemma_concordance(lemma)
        else:
            print "You need to enter the lemma you are interested in on the command line to run this function!"
            print
    elif selection == "g":
        corpus.print_text(filename)
    elif selection == "h":
        corpus.print_words(filename)
    elif selection == "i":
        corpus.transform_case(filename)
    elif selection == "j":
        corpus.transform_back(filename)
    else:
        print "I'm sorry--I don't understand what you entered."
        print
        sys.exit()

#END_DEF select

if __name__ == "__main__":
    main()
