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

#END_DEF GreekCorpus

def main():

    print "Hello, world"

    corpus = GreekCorpus()

    filename = sys.argv[1]

    print filename

    corpus.read(filename)

    corpus.transform_case(filename)

if __name__ == "__main__":
    main()