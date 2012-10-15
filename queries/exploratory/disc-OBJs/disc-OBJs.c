add_to_ignore: RPAREN|LPAREN

node: IP*

/*
a = #X...X...V
b = #...X...V...X
c = #X...V...X
d = #...V...X...X
e = ELSE
*/

coding-query:

1: { a: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms VB*) AND (VB* iDoms !\**) AND (NP-OB1* Doms \*ICH\**)