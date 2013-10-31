node: $ROOT

define: case.def

coding_query:

1: { A: (NP-OB1* iDomsMod NP*|CONJP* acc)
     F: (NP-OB1* iDoms CP-FRL*)
     T: (NP-OB1* iDoms \**)
     X: ELSE }