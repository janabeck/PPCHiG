//run on Mark

node: $ROOT

query: (CP-* iDoms W*) AND (CP-* iDoms IP-SUB*) AND (IP-SUB* iDoms NP-*) AND (NP-* iDoms NP-*|PP*) AND (NP-*|PP* SameIndex W*)