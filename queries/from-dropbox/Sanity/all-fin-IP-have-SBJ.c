node: IP*

coding_query:

1: { t: (IP-MAT*|IP-SUB*|IP-SMC* iDoms *-SBJ*)
     f: (IP-MAT*|IP-SUB*|IP-SMC* Exists) AND NOT (CP-CMP* iDoms IP-MAT*|IP-SUB*|IP-SMC*)
     o: ELSE }
