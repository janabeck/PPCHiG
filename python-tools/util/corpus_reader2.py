# This Python file uses the following encoding: utf-8

"""
corpus_reader2.py
Created 2011/12/14
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import codecs
import sys
import re
from sets import Set
import nltk.tree as T

class Token():
    """A class for Penn-style parsed trees."""
    
    def __init__(self, str):
        """Initialize a token."""

        # _tree contains the token as an nltk Tree
        self._tree = T.ParentedTree(str)
        
        # id contains the token's ID as a string "Corpus,Book.x"
        self.id = ""

        # corpus contains the corpus part of the ID as a string
        self.corpus = ""

        # book contains the book (= filename) part of the ID as a string
        self.book = ""

        # id_num contains the numerical index of the ID as an integer
        self.id_num = 0

        # milestones contains all the milestones in a particular token
        self.milestones = []
        
        # words contains all the words in a sentence token, exclusive of punctuation, as a list
        self.words = []

        # text contains all the words in a sentence token, including punctuation, as a list
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

        # metadata contains the METADATA sub-tree if present
        self.metadata = ""

    def parse(self, tree):
        """Fill Token data structure."""
        
        # finds METADATA node, stores it, and then removes it so as not to interfere with word count, etc.
        for tr in tree.subtrees():
            if tr.node == "METADATA":
                self.metadata = tr
                main_tree = tr.right_sibling
                if main_tree.right_sibling:
                    id_tree = main_tree.right_sibling
                    tree = T.Tree("", [main_tree, id_tree])
                    tree = T.ParentedTree.convert(tree)
                else:
                    tree = T.Tree("", [main_tree])

        id_str = re.compile("^(.*),(.*):[0-9_;a-z]*\.([0-9]*)$")

        # finds $ROOT and stores in self.root

        subtrs = []

        for tr in tree.subtrees():
            subtrs.append(tr)

        root = subtrs[1]

        self.root = root.node
        
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
            elif tag.find("ID") != -1:
                self.id = leaf
                id_stuff = id_str.match(leaf)
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
            # catches everything else = just words
            else:
                self.text.append(leaf)
                self.pos.append((leaf, tag))
                self.words.append(leaf)

class Corpus():
    """A class for a database of Penn-style parsed trees."""

    def __init__(self):

        # trees contains keys = numerical indices corresponding to sequence of tokens in file and values = Token instances
        self.tokens = {}

    def load(self, trees):
        """Initializes Token objects and fills corpus instance."""

        count = 0

        for tree in trees:
            tok = Token(tree)
            tok.parse(tok._tree)
            self.tokens[count] = tok
            count += 1

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

    def word_count(self):
        """Count all and only the words in the .psd file."""

        word_count = 0

        keys = self.tokens.keys()

        for key in keys:
            tok = self.tokens[key]
            for word in tok.words:
                word_count += 1

        print "There are " + str(word_count) + " words in this file, excluding empty categories and punctuation."
        print

    def renumber_ids(self, filename):
        """Renumber/add IDs in the .psd file."""

        pass

    def add_milestones(self, filename):
        """Add continuity milestones in the .psd file."""

        lst_milestone = ""

    def print_trees(self, filename):
        """Just print the trees from an input file."""
        # (i.e., remove CS comment blocks from .out files)

        out_name = filename.replace(".out",".out.new")

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

def main():

    flag = ""

    # boolean for whether file is CorpusSearch output file format
    out = False
    
    try:
        if sys.argv[1].startswith("-"):
            flag = sys.argv.pop(1)
        # name of main .psd file interested in reading
        filename = sys.argv.pop(1)
        if filename.find(".out") != -1:
            out = True
        in_trees = read(filename, out)
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
        select(corpus)

def read(filename, out):
    """Read in a .psd file and return a list of trees as strings."""

    in_str = ""

    if not out:
        # method for getting trees out of regular .psd file
        in_str = open(filename, "rU").read()

    # boolean for whether currently in comment block in CorpusSearch output file
    comment = False
    
    if out:
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

def select(corpus):
    """Select another CR function from a menu."""

    #TODO
    pass

if __name__ == "__main__":
    main()


