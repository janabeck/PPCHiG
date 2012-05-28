# This Python file uses the following encoding: utf-8

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(current_dir + "/../../../../Git/Academic/TreeTransformer")

from lovett.annotald import flagIf, stdinValidator
from lovett.searchfns import *
from collections import OrderedDict

import runpy

vs = runpy.run_path(current_dir + "/../../../../Git/Academic/PPCHiG/annotald/validation-scripts/validation_settings.py")

import re
r = re.compile

# List of paths to javascript files which should be included in the
# Annotald UI
extraJavascripts=["/Users/janabeck/Downloads/waxeye-0.8.0/src/javascript/waxeye.js",
                  current_dir + "/waxeye/phrase-grammar.js",
                  current_dir + "/waxeye/leaf-grammar.js"]

# Set this to True if you are an Annotald developer or otherwise need to
# debug Annotald's jQuery code
debugJs = False

# Set this to True if you have defined a color.css file in the css directory
colorCSS = True

colorCSSPath = current_dir + "/color.css"

# flags CPs that don't have a C
CPwithoutC = flagIf(hasLabel("CP") & ~hasDaughter(hasLabel("C", True)) & ~isTrace() & ~hasDaughter(hasLabel("CONJP")))

# flags finite IPs without a subject
missingSBJ = flagIf(hasLabel(vs['subj_ips']) & ~hasDaughter(hasLabel(vs['subject'])) & ~hasDaughter(hasLabel("CONJP")) & ~hasParent(hasLabel("CP-CMP")))

# flags IP-MAT, IP-SUB, or IP-IMP with a non-coindexed infinitive on its spine
spineINF = flagIf(hasLabel(r("IP-MAT|IP-SUB|IP-IMP")) & hasDaughter(hasLabel(r("BEN.*|VBN.*"))) & ~hasDaughter(hasLabel(vs['finite'])))

# flags IPs with multiple subjects
multipleSBJ = flagIf(hasLabel("IP") & hasDaughter(hasLabel(vs['subject']) & hasSister(hasLabel(vs['subject']))))

validators = OrderedDict([
    ("v1", stdinValidator("/Users/janabeck/Git/Academic/PPCHiG/annotald/validation-scripts/v1.py")),
    ("v2", stdinValidator("/Users/janabeck/Git/Academic/PPCHiG/annotald/validation-scripts/v2.py")),
    ("sanity", stdinValidator("/Users/janabeck/Git/Academic/PPCHiG/annotald/validation-scripts/sanity.py")),
    ("CPs without C", CPwithoutC),
    ("Missing subject", missingSBJ),
    ("Infinitive on a finite spine", spineINF),
    ("Multiple subjects", multipleSBJ)
])
