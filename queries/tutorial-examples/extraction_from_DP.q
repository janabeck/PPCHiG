//run on Histories1a.00.psd

node: $ROOT

query: (CP-* iDoms W*) AND (CP-* iDoms IP-SUB*) AND (IP-SUB* iDoms NP-*) AND (NP-* iDoms NP-*|PP*) AND (NP-*|PP* iDoms \**) AND (\** SameIndex W*)