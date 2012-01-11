/* checks to be sure that all finite IPs have some sort of subject */

node: IP-MAT*|IP-SUB*

query: ({1}IP-MAT*|IP-SUB* Exists) AND NOT(IP-MAT*|IP-SUB* iDoms *-SBJ*|CONJP)

append_label{1}: -XXX