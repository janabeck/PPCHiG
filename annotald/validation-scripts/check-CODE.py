#!/usr/bin/env python

# make sure all CODE items (VS, COM, MAN, TODO) only have CODE as parent

import re

import os.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(SCRIPT_DIR + "/../../../../../Git/Academic/TreeTransformer")

from lovett.annotald import flagIf
from lovett.searchfns import *

code_stuff = re.compile("{VS:.*|{COM:.*|{MAN:.*|{TODO:.*")

flagIf(hasLeafLabel(code_stuff) & ~hasLabel("CODE"))

