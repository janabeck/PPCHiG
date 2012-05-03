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

for tree in trees:
    trans = TT.TreeTransformer(T.ParentedTree(tree))

    for num in vs['numbers']:
        for case in vs['cases']:
        	pass

    print trans.pt() + "\n\n"
sys.stdout.close()