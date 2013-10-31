node: $ROOT

define: case.def

coding_query:

1: { D: (NP-OB2* iDomsMod NP*|CONJP* dat)
     F: (NP-OB2* iDoms CP-FRL*)
     T: (NP-OB2* iDoms \**)
     X: ELSE }
