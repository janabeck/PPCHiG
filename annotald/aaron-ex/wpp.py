#!/usr/bin/env python

import os.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(SCRIPT_DIR + "/../../scripts/TreeTransformer")

from lovett.annotald import flagIf
from lovett.searchfns import *

flagIf(hasLabel("PP") & hasImmRightSister(hasLabel("CP-REL")))
