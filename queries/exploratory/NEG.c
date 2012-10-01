add_to_ignore: RPAREN|LPAREN|\**

node: IP*

/*
l = alone in IP* (ellipsis)
a = ambiguous because both first position and pre-verbal
f = unambiguously first position
c = ambiguous because both second position and pre-verbal
v = unambiguously pre-verbal
s = unambiguously second position
o = other
e = no negation
*/

coding_query:

1: { l: (IP-MAT*|IP-SUB* iDomsFirst NEG) AND (IP-MAT*|IP-SUB* domsWords 1) AND (NEG iDoms !*@*)
     a: (IP-MAT*|IP-SUB* iDomsFirst NEG) AND (NEG iPrecedes VB*|BE*) AND (NEG iDoms !*@*)
     f: (IP-MAT*|IP-SUB* iDomsFirst NEG) AND (NEG iDoms !*@*)
     c: (IP-MAT*|IP-SUB* iDoms VB*|BE*) AND (VB*|BE* iDoms !\*ICH\**) AND (NEG iPrecedes VB*|BE*) AND (NEG iDoms !*@*) AND (IP-MAT*|IP-SUB* iDomsNumber 2 NEG)
     v: (IP-MAT*|IP-SUB* iDoms VB*|BE*) AND (VB*|BE* iDoms !\*ICH\**) AND (NEG iPrecedes VB*|BE*) AND (NEG iDoms !*@*)
     s: (IP-MAT*|IP-SUB* iDomsNumber 2 NEG) AND (NEG iDoms !*@*)
     o: (IP-MAT*|IP-SUB* iDoms NEG) AND (NEG iDoms !*@*)
     e: ELSE }