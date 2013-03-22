add_to_ignore: RPAREN|LPAREN

define: ../../definitions/verbs.def

node: IP-MAT*|IP-SUB*

/*
1: type of verb (v = main verb, b = copula, o = other)
2: type of subject (n = nominal, p = pronominal, e = pro, t = trace or discontinuous)
3: type of object (n = nominal, p = pronominal, d = determiner, t = trace or discontinuous)
4: order of subject and verb (s = subject first, v = verb first)
5: order of object and verb (o = object first, v = verb first)
6: order of subject and object (s = subject first, o = object first)
7: more than one object (t = more than one, f = only one)
8: verb is first thing in clause (t = initial, f = not initial)
9: verb is last thing in clause (t = final, f = not final)
*/

coding_query:

1: { v: (IP-MAT*|IP-SUB* iDoms finite)
     b: (IP-MAT*|IP-SUB* iDoms finite_be)
     o: ELSE
}

2: { e: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* iDoms \*pro\**|\*con\**)
     p: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* iDoms PRO*|CLPRO*)
     t: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* Doms \*ICH\**|\*T\**)
     n: (IP-MAT*|IP-SUB* iDoms NP-SBJ*)
}

3: { p: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* iDoms PRO*|CLPRO*)
     d: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* iDomsOnly D*)
     t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* Doms \*ICH\**|\*T\**)
     n: (IP-MAT*|IP-SUB* iDoms NP-OB*)
}
   
4: { s: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-SBJ* Precedes finite)
     v: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes NP-SBJ*)
}

5: { o: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB* Precedes finite)
     v: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes NP-OB*)
}

6: { s: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-SBJ* Precedes NP-OB*)
     o: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* Precedes NP-SBJ*)
}

7: { t: (IP-MAT*|IP-SUB* iDoms [1]NP-OB*) AND (IP-MAT*|IP-SUB* iDoms [2]NP-OB*)
     f: ELSE
}

8: { t: (IP-MAT*|IP-SUB* iDomsFirst finite)
     f: ELSE
}

9: { t: (IP-MAT*|IP-SUB* iDomsLast finite)
     f: ELSE
}