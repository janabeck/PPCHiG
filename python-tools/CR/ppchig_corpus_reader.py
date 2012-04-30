# This Python file uses the following encoding: utf-8

"""
ppchig_corpus_reader.py
Created 2012/3/22
@author: Jana E. Beck
@copyright: GNU General Public License http://www.gnu.org/licenses/
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
@contact: jana.eliz.beck@gmail.com
"""

import sys
import re

from corpus_reader import Corpus

class GreekCorpus(Corpus):
    """Greek-specific Corpus Reader functions."""

    def transform_case(self, filename):
        """Change case tags from non-hyphenated suffixes to hyphenated extensions."""

        participle = re.compile("VPR*|BPR*")

        adj = ["ADJ", "ADJ$", "ADJA", "ADJD"]

        be = ["BPR", "BPR$", "BPRA", "BPRD", "BPRP", "BPRP$", "BPRPA", "BPRPD"]

        clpro = ["CLPRO", "CLPRO$", "CLPROA", "CLPROD"]

        clq = ["CLQ", "CLQ$", "CLQA", "CLQD"]

        det = ["D", "D$", "DA", "DD", "DS", "DS$", "DSA", "DSD", "DEM", "DEM$", "DEMA", "DEMD", "DEMS", "DEMS$", "DEMSA", "DEMSD"]

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
                                    tag = "".join([coretag, remainder, "-" + dash])
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
                                tag = tag.replace("-RCP","")
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

#END_DEF GreekCorpus

def main():

    corpus = GreekCorpus()

    filename = sys.argv[1]

    try:
        add_file = sys.argv[2]
    except IndexError:
        add_file = ""

    corpus.read(filename)

    select(corpus, filename, add_file)

def select(corpus, filename, add_file):
    """Select a Greek-specific CR function."""

    print "Select a function:"
    print "    a. Change the POS tags of words in the corpus file having certain lemmas."
    print "    b. Replace the POS tags in the corpus file with those from a 'map' file."
    print "    c. Transform case suffixes into dash tags."
    print "    d. Transform case dash tags back into suffixes."
    print

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
            print "You need to enter the name of the POS map file on the command line to run this function!"
            print
    elif selection == "c":
        corpus.transform_case(filename)
    elif selection == "d":
        corpus.transform_back(filename)
    else:
        print "I'm sorry--I don't understand what you entered."
        print
        sys.exit()

#END_DEF select

if __name__ == "__main__":
    main()
