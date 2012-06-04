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

    fin_re = vs['fin']
    nonfin_re = vs['nonfin']
    voice_re = re.compile(".*-INTRNS.*|.*-PASS.*|.*-TRNS1.*|.*-TRNS2.*")
    obj_re = re.compile("NP-OB1.*|NP-OBP.*|NP-OBQ.*")
    coms_re = re.compile("CP-COM.*|IP-INF-COM.*|CP-THT.*|IP-INF-THT.*|IP-SMC.*|IP-PPL-THT.*")

    tmp1 = []
    tmp2 = []

    for voice in vs['voices']:
        case_trans = tmp2.append("|".join(map(lambda x: ".*" + x + voice, vs['cases'])))

    case_trans_re = re.compile("|".join(tmp2))
    
    # adds -TRNS1 if sister to NP-OB1, NP-OBP, or NP-OBQ
    trans.findNodes((hasLabel(fin_re) | hasLabel(nonfin_re)) & ~hasLabel(voice_re)
        & hasSister(hasLabel(obj_re)))
    trans.changeLabel(lambda x: x + "-TRNS1")
    trans.addParentNode("TAGGED")

    # adds -TRNS2 if sister to something in coms_re
    trans.findNodes((hasLabel(fin_re) | hasLabel(nonfin_re)) & ~hasLabel(voice_re)
        & hasSister(hasLabel(coms_re)))
    trans.changeLabel(lambda x: x + "-TRNS2")
    trans.addParentNode("TAGGED")

    # adds -INTRNS if lemma in always intransitive lemmas list
    for lem in vs['intrans_lemmas']:
        trans.findNodes((hasLabel(fin_re) | hasLabel(nonfin_re)) & ~hasLabel(voice_re)
            & hasLemma(lem))
        trans.changeLabel(lambda x: x + "-INTRNS")
        trans.addParentNode("TAGGED")

    # reorders case and transitivity tags for participles
    for case in vs['cases']:
        for voice in vs['voices']:
            trans.findNodes(hasLabel(nonfin_re) & hasLabel(case_trans_re) & hasLabel(r(".*" + case + ".*")) & hasLabel(r(".*" + voice + ".*")))
            trans.changeLabel(lambda x: (x.replace(case,"").replace(voice,"") + voice + case))

    # finds traces of verbs that have been tagged
    trans.findNodes(hasLabel("TAGGED") & hasDaughter(isTrace()))
    trans.changeLabel(lambda x: x + "-TRACE")

    # finds remainder that need a transitivity tag
    trans.findNodes((hasLabel(fin_re) | hasLabel(nonfin_re)) & ~hasLabel(voice_re))
    trans.addParentNode("FLAG")

    print trans.pt() + "\n\n"
sys.stdout.close()