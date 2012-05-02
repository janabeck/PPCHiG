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

# TODO: fix this to run in Annotald!
vs = runpy.run_path("validation_settings.py")

data = sys.stdin.read()
trees = data.split("\n\n")

for tree in trees:
    trans = TT.TreeTransformer(T.ParentedTree(tree))

    for num in vs['numbers']:
        for case in vs['cases']:
            nom_re = re.compile("|".join(map(lambda x: x + case, num[0])))
            det_re = re.compile("|".join(map(lambda x: x + case, num[1])))
            dem_re = re.compile("|".join(map(lambda x: x + case, num[2])))

            # does DEM + D + any nominal combinations
            trans.findNodes(hasLabel(dem_re) & hasParent(hasLabel("IP-MAT")) & hasImmRightSister(hasLabel(det_re)))
            trans.addParentNodeSpanning("NP"+case, hasLabel(det_re))
            trans.findNodes(hasLabel("NP"+case))
            trans.extendUntil(hasLabel(nom_re), immediate=True)

            # does D + any nominal + DEM combinations
            trans.findNodes(hasLabel(det_re) & hasParent(hasLabel("IP-MAT")) & hasImmRightSister(hasLabel(nom_re)))
            trans.addParentNodeSpanning("NP"+case, hasLabel(nom_re))
            trans.findNodes(hasLabel("NP"+case))
            trans.extendUntil(hasLabel(dem_re), immediate=True)

            # does D/DEM + clitic + any nominal
            trans.findNodes((hasLabel(dem_re) | hasLabel(det_re)) & hasParent(hasLabel("IP-MAT")) 
                & hasImmRightSister(hasLabel(vs['ignore']) & hasImmRightSister(hasLabel(nom_re))))
            trans.addParentNodeSpanning("NP"+case, hasLabel(nom_re))

            # does D/DEM + any nominal
            trans.findNodes((hasLabel(dem_re) | hasLabel(det_re)) & hasParent(hasLabel("IP-MAT"))
                & hasImmRightSister(hasLabel(nom_re)))
            trans.addParentNodeSpanning("NP"+case, hasLabel(nom_re))

            trans.findNodes(hasLabel("NP"+case))
            trans.extendUntil(hasLabel(nom_re), immediate=True)

            trans.findNodes(hasLabel(vs['np_re']))
            trans.changeLabel("NP-FLAG")

        trans.findNodes(hasLabel("P", True) & hasParent(hasLabel("IP-MAT")))
        trans.addParentNode("PP")
        trans.findNodes(hasLabel("PP") & ~hasDaughter(hasLabel("NP-FLAG")))
        trans.extendUntil(hasLabel("NP-FLAG"), immediate=True)

    print trans.pt() + "\n\n"
sys.stdout.close()
