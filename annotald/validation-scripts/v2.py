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
            nom_re = re.compile("|".join(map(lambda x: x + case, vs['nom'])))
            det_re = re.compile("|".join(map(lambda x: x + case, vs['det'])))
            dem_re = re.compile("|".join(map(lambda x: x + case, vs['dem'])))
            gen_re = re.compile("|".join(map(lambda x: x + "-GEN", vs['all_together'])))

            # does D + center-embedded genitive noun + nom
            trans.findNodes(hasLabel(det_re) & hasParent(hasLabel("IP-MAT")) & hasImmRightSister(
                hasLabel(gen_re) & hasImmRightSister(hasLabel(nom_re))))
            trans.addParentNodeSpanning("NP-FLAG", hasLabel(nom_re))

            # does D + center-embedded genitive NP + nom
            trans.findNodes(hasLabel(det_re) & hasParent(hasLabel("IP-MAT")) & hasImmRightSister(
                hasLabel("NP") & hasDaughter(hasLabel(gen_re)) & hasImmRightSister(hasLabel(nom_re))))
            trans.addParentNodeSpanning("NP-FLAG", hasLabel(nom_re))

            # does nom + nom
            trans.findNodes(hasLabel(nom_re) & hasParent(hasLabel("IP-MAT")) & hasImmRightSister(hasLabel(nom_re)))
            trans.addParentNodeSpanning("NP-FLAG", hasLabel(nom_re))

        trans.findNodes(hasLabel("P", True) & hasParent(hasLabel("IP-MAT")))
        trans.addParentNode("PP")
        trans.findNodes(hasLabel("PP") & ~hasDaughter(hasLabel("NP-FLAG") | hasLabel("NP")))
        trans.extendUntil(hasLabel("NP-FLAG"), immediate=True)

    for case in vs['cases']:
        nom_re = re.compile("|".join(map(lambda x: x + case, vs['nom'])))
        det_re = re.compile("|".join(map(lambda x: x + case, vs['det'])))
        dem_re = re.compile("|".join(map(lambda x: x + case, vs['dem'])))
        all_re = re.compile("|".join(map(lambda x: x + case, vs['nom'])+ map(lambda x: x + case, vs['det'])+ map(lambda x: x + case, vs['dem'])))

        # does lone nominals that aren't neighbors with anything else nominal-like or with CONJ or CLPRT
        trans.findNodes((hasLabel(nom_re) | hasLabel(det_re) | hasLabel(dem_re)) & hasParent(hasLabel("IP-MAT"))
            & (hasImmLeftSister(~(hasLabel(all_re) | hasLabel("CONJ"))) & hasImmRightSister(~(hasLabel(all_re) | hasLabel("CONJ") | hasLabel("CLPRT")))))
        trans.addParentNode("NP-FLAG")

        # does lone pronouns
        trans.findNodes(hasLabel(vs['pro_re']) & hasParent(hasLabel("IP-MAT")))
        trans.addParentNode("NP-FLAG")

        trans.findNodes(hasLabel("P", True) & hasParent(hasLabel("IP-MAT")))
        trans.addParentNode("PP")
        trans.findNodes(hasLabel("PP") & ~hasDaughter(hasLabel("NP-FLAG") | hasLabel("NP")))
        trans.extendUntil(hasLabel("NP-FLAG"), immediate=True)

        if case == "-NOM":
            trans.findNodes(hasLabel("NP") & hasParent(hasLabel("IP-MAT")))
            trans.changeLabel("NP-SBJ")

    print trans.pt() + "\n\n"
sys.stdout.close()