#!/usr/bin/env python

import os.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(SCRIPT_DIR + "/../../../../../Git/Academic/TreeTransformer")

import re
import lovett.transformer as TT
from lovett.searchfns import *
import nltk.tree as T

import runpy

vs = runpy.run_path(SCRIPT_DIR + "/../../../../../Git/Academic/PPCHiG/annotald/validation-scripts/validation_settings.py")

data = sys.stdin.read()
trees = data.split("\n\n")

r = re.compile

for tree in trees:
    trans = TT.TreeTransformer(T.ParentedTree(tree))

    # adds null C if none present in a CP
    trans.findNodes(hasLabel("IP") & hasParent(hasLabel("CP") & ~hasDaughter(hasLabel("C", True))))
    trans.addSister("C-FLAG", "0")

    # adds (NP-SBJ *pro*) where needed
    trans.findNodes(hasLabel(vs['finite']) & hasParent(hasLabel(vs['subj_ips']) & ~hasDaughter(hasLabel(r(".*\-SBJ.*")))))
    trans.addSister("NP-SBJ-FLAG", "*pro*")

    # flags optatives for review
    trans.findNodes(hasLabel(r("VBO.*|BEO.*")))
    trans.addParentNode("FLAG")

    print trans.pt() + "\n\n"
sys.stdout.close()