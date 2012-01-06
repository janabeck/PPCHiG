#!/usr/bin/env python

import os.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(SCRIPT_DIR + "/TreeTransformer")

import re
import treetrans.transformer as TT
from treetrans.searchfns import *
import nltk.tree as T

if __name__ == "__main__":
    trees = sys.stdin.read().split("\n\n")
    transformed_trees = []
    for t in trees:
        if not t == "":
            tp = T.ParentedTree(t)
            tt = TT.TreeTransformer(tp)

            # Conjunctions
            conj_pairs = [("N", "NP"),
                          ("P", "PX"),
                          ("ADJ", "ADJP"),
                          # Too many false positives
                          # (re.compile("V.*"), "VX"),
                          ("PRO", "NP")]
            for label, repl in conj_pairs:
                tt.findNodes(hasLabel(label, exact=True) &
                             hasImmRightSister(hasLabel("CONJ") &
                                               hasImmRightSister(hasLabel(label,
                                                                          exact=True))))
                tt.addParentNodeSpanning(repl, hasLabel(label))

            # High-level structure
            # TODO: what is the right label for this?
            tt.findNodes(hasWord("<quote>")).addParentNodeSpanning("IP-MAT-SPE",
                                                                   hasWord("</quote>"))
            # TODO: we need a script for the multi-sentence case

            # Adjectives
            tt.findNodes(hasLabel("ADJ")).addParentNode("ADJP")
            qualifiers = ["muy", "tan"] # ...
            qualifiers_re = re.compile("|".join(qualifiers))
            tt.findNodes(hasLemma(qualifiers_re) & immRightSister(hasLabel("ADJP")))
            tt.extendUntil(hasLemma(qualifiers_re), right = False)

            # Nouns
            tt.findNodes(hasLabel(re.compile("N|NS|NPR|NPRS|ND|NDS")))
            tt.addParentNode("NBAR")
            tt.findNodes(hasLabel("NBAR") & hasDaughter(hasLabel("NPR") |
                                                        (hasLabel("N") &
                                                         hasLemma("santo"))) &
                         hasImmRightSister(hasLabel("NBAR") &
                                           hasDaughter(hasLabel("NPR"))))
            tt.addParentNodeSpanning("NBAR", hasLabel("NBAR"))
            tt.findNodes(hasLabel("NBAR") & hasParent(hasLabel("NBAR"))).prune()
            tt.findNodes(hasLabel("PRO", exact = True)).addParentNode("NBAR")
            tt.findNodes(hasLabel("PRO-NOM", exact = True)).addParentNode("NBAR-SBJ").\
                changeLabel("PRO")

            ## Prenominal modifiers
            for i in ["ADJP", "PRO$", "D", "NUM", "Q"]:
                tt.findNodes(hasLabel("NBAR")).extendUntil(hasLabel(i),
                                                           immediate = True,
                                                           right = False)

            ## Bare determiners/quantifiers
            for i in ["D", "Q"]:
                tt.findNodes(hasLabel(i) & ~hasParent(hasLabel("NBAR")))
                tt.addParentNode("NBAR")

            ## Postnominal modifiers
            oldtree = None
            while not oldtree == tt._tree:
                oldtree = tt._tree
                tt.findNodes(hasLabel("NBAR")).extendUntil(hasLabel("ADJP"),
                                                           immediate = True)
                
            tt.findNodes(hasLabel("NBAR")).extendUntil(hasLabel("PRO$"),
                                                       immediate = True)
            
            # Prepositions
            tt.findNodes(hasLabel("P") & hasImmRightSister(hasLabel("NBAR")))
            tt.addParentNodeSpanning("PP", hasLabel("NBAR"))

            # Nouns with PPs
            oldtree = None
            while not oldtree == tt._tree:
                oldtree = tt._tree
                tt.findNodes(hasLabel("NBAR") & hasImmRightSister(hasLabel("PP")))
                tt.extendUntil(hasLabel("PP"))

            # Finalize nouns
            tt.findNodes(hasLabel("NBAR")).changeLabel(lambda s: s.replace("NBAR", "NP"))

            # wh-words

            ## wh-projections
            tt.findNodes(hasLabel("WD")).addParentNode("WNP")
            tt.findNodes(hasLabel("WNP") & hasImmRightSister(hasLabel("PP")))
            tt.extendUntil(hasLabel("PP"), immediate = True)
            tt.findNodes(hasLabel("WPRO")).addParentNode("WNP")
            tt.findNodes(hasLabel("WPRO$")).addParentNodeSpanning("WNP", hasLabel("NP"),
                                                                  immediate = True)
            tt.findNodes(hasLabel("WADV")).addParentNode("WADVP")
            ## Null complementizer
            tt.findNodes(hasLabel(re.compile("WNP|WADVP")))
            tt.addSister("C", "0-0", before = False)
            ## CP and IP prejections
            sentence_end_rx = re.compile("\\.|,|\"")
            tt.addParentNodeSpanning("CP-REL", hasLabel(sentence_end_rx))
            tt.findNodes(hasLabel("C") & hasLemma("0") & immRightSister())
            tt.addParentNodeSpanning("IP-REL", hasLabel(sentence_end_rx))

            # TODO: make addParentNode move pointer, so we can say .addparent.addparent
            tt.findNodes(hasLabel("C") & hasLemma("que"))
            tt.addParentNodeSpanning("CP-THT", hasLabel(sentence_end_rx))
            tt.findNodes(hasLabel("CP-THT") & daughters(hasLemma("que")) &
                         immRightSister())
            tt.addParentNodeSpanning("IP-THT", hasLabel(sentence_end_rx))

            # Preposition + CP
            tt.findNodes(hasLabel("P") & hasImmRightSister(hasLabel("CP")))
            # TODO: is this right?
            tt.addParentNodeSpanning("PP", hasLabel("CP"))
            tt.findNodes(hasLabel("CP") & hasParent(hasLabel("PP")))
            # TODO: also, is this right?
            tt.changeLabel("CP-SUB")
            
            transformed_trees.append(tt.pt())
    print "\n\n".join(transformed_trees)
