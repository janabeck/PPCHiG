# This Python file uses the following encoding: utf-8

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(current_dir + "/../../../../Git/Academic/TreeTransformer")

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

from lovett.annotald import stdinValidator, flagIf
from collections import OrderedDict
validators = OrderedDict([
    ("v1", stdinValidator("/Users/janabeck/Git/Academic/PPCHiG/annotald/validation-scripts/v1.py")),
    ("v2", stdinValidator("/Users/janabeck/Git/Academic/PPCHiG/annotald/validation-scripts/v2.py")),
    ("sanity", stdinValidator("/Users/janabeck/Git/Academic/PPCHiG/annotald/validation-scripts/sanity.py"))
])
