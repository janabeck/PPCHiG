add_to_ignore: RPAREN|LPAREN

define: ../../definitions/verbs.def

node: IP-MAT*|IP-SUB*

/*
1: type of verb (v = main verb, b = copula, o = other)
2: type of direct object (n = nominal, p = pronominal, t = trace or discontinuous)
3: type of indirect object (n = nominal, p = pronominal, d = determiner, t = trace or discontinuous)
4: order of direct object and verb (d = object first, v = verb first)
5: order of indirect object and verb (i = object first, v = verb first)
6: order of direct object and indirect object object (i = indirect first, d = direct first)
*/

coding_query:

1: { v: (IP-MAT*|IP-SUB* iDoms finite)
     b: (IP-MAT*|IP-SUB* iDoms finite_be)
     o: ELSE
}

2: { p: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (NP-OB1* iDoms PRO*|CLPRO*)
     d: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (NP-OB1* iDoms D*)
     t: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (NP-OB1* Doms \*ICH\**|\*T\**)
     n: (IP-MAT*|IP-SUB* iDoms NP-OB1*)
}

3: { p: (IP-MAT*|IP-SUB* iDoms NP-OB2*) AND (NP-OB2* iDoms PRO*|CLPRO*)
     d: (IP-MAT*|IP-SUB* iDoms NP-OB2*) AND (NP-OB2* iDoms D*)
     t: (IP-MAT*|IP-SUB* iDoms NP-OB2*) AND (NP-OB2* Doms \*ICH\**|\*T\**)
     n: (IP-MAT*|IP-SUB* iDoms NP-OB2*)
}
   
4: { d: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB1* Precedes finite)
     v: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes NP-OB1*)
}

5: { i: (IP-MAT*|IP-SUB* iDoms NP-OB2*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB2* Precedes finite)
     v: (IP-MAT*|IP-SUB* iDoms NP-OB2*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes NP-OB2*)
}

6: { d: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms NP-OB2*) AND (NP-OB1* Precedes NP-OB2*)
     i: (IP-MAT*|IP-SUB* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms NP-OB2*) AND (NP-OB2* Precedes NP-OB1*)
}