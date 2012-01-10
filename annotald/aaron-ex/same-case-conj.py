#!/usr/bin/python

import nltk.tree as T
import re

import os.path
# = path of this python script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
# path from current directory (i.e., of this python script, to Git repo TreeTransformer)
sys.path.append(SCRIPT_DIR + "/../../../../myGit/TreeTransformer")

from lovett import transformer as TT
from lovett.searchfns import *

## def main():
data = sys.stdin.read()
data = data.replace("-FLAG", "") # TODO: do this in a smarter way
trees = data.split("\n\n")
nominals = ["ADJ","CLPRO","CLQ","D","DS","N","NPR","NPRS","NS","PRO","Q","WADJ","WD","WPRO"]
nominals_re = re.compile("|".join(nominals))
noun_phr = re.compile("NP.*|WNP.*")
for tree in trees:
    trans = TT.TreeTransformer(T.ParentedTree(tree))
    for case in ["", "A", "D", "\\$"]:
        case_nominals = re.compile("|".join(map(lambda x: x + case, nominals)))
        case_end_re = re.compile(".*" + case + "$|.*" + case + "-.*")
        trans.findNodes(hasLabel(case_nominals) & hasLabel(case_end_re))
        ## trans.findNodes(hasLabel(noun_phr) & hasDaughter(hasLabel(case_nominals) & hasLabel(case_end_re)) & hasSister(hasLabel("CONJP") & hasDaughter(hasLabel(noun_phr) & hasDaughter(hasLabel(case_nominals) & ~hasLabel(case_end_re)))))
        trans.changeLabel(lambda x: x + "-FLAG")
        print trans.pt() + "\n\n"
sys.stdout.close()

## if __name__ == "__main__":
##     main()

