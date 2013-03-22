add_to_ignore: RPAREN|LPAREN

define: ../../definitions/verbs.def

node: IP-MAT*|IP-SUB*

/*
1: type of verb (v = finite, b = finite 'be', o = ELSE)
2: type of subject (n = nominal, p = pronominal, e = pro, t = trace or discontinuous)
3: infinitive sister of matrix verb? (t/f)
4: type of acc. object (n = nominal, p = pronominal, d = determiner, t = trace or discontinuous, f = none)
5: type of dat. object (n = nominal, p = pronominal, d = determiner, t = trace or discontinuous, f = none)
6: order of subject and matrix verb (s = subject first, v = verb first)
7: order of matrix verb and inf (v = verb first, i = inf. first)
8: order of matrix verb and acc. object (v = verb first, a = acc. first)
9: order of matrix verb and dat. object (v = verb first, d = dat. first)
10: order of inf. and acc. object (i = inf. first, a = acc. first)
11: order of inf. and dat. object (i = inf. first, d = dat. first)
12: order of subject and acc. object (s = subject first, a = acc. first)
13: order of subject and dat. object (s = subject first, d = dat. first)
*/

coding_query:

1: { v: (IP-MAT*|IP-SUB* iDoms finite)
     b: (IP-MAT*|IP-SUB* iDoms finite_be)
     o: ELSE
}

2: { e: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* iDoms \*pro\**|\*con\**|\*exp\**)
     p: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* iDoms PRO*|CLPRO*)
     t: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* Doms \*ICH\**|\*T\**)
     n: (IP-MAT*|IP-SUB* iDoms NP-SBJ*)
}

3: { t: (IP-MAT*|IP-SUB* iDoms IP-INF-COM*) AND NOT (IP-INF-COM* iDoms \*ICH\**) AND (IP-INF-COM* iDoms infinitive) AND NOT (infinitive iDoms \*ICH\**)
     f: ELSE
}

4: { p: (IP-INF-COM* iDoms NP-OB1*) AND (NP-OB1* iDoms PRO*|CLPRO*)
     d: (IP-INF-COM* iDoms NP-OB1*) AND (NP-OB1* iDomsOnly D*)
     t: (IP-INF-COM* iDoms NP-OB1*) AND (NP-OB1* Doms \*ICH\**|\*T\**)
     n: (IP-INF-COM* iDoms NP-OB1*)
     f: ELSE
}

5: { p: (IP-INF-COM* iDoms NP-OB2*) AND (NP-OB2* iDoms PRO*|CLPRO*)
     d: (IP-INF-COM* iDoms NP-OB2*) AND (NP-OB2* iDomsOnly D*)
     t: (IP-INF-COM* iDoms NP-OB2*) AND (NP-OB2* Doms \*ICH\**|\*T\**)
     n: (IP-INF-COM* iDoms NP-OB2*)
     f: ELSE
}

6: { s: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-SBJ* Precedes finite)
     v: (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes NP-SBJ*)
}

7: { i: (IP-INF-COM* iDoms infinitive) AND (IP-MAT*|IP-SUB* iDoms finite) AND (infinitive Precedes finite)
     v: (IP-INF-COM* iDoms infinitive) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes infinitive)
}

8: { a: (IP-INF-COM* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB1* Precedes finite)
     v: (IP-INF-COM* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes NP-OB1*)
}

9: { d: (IP-INF-COM* iDoms NP-OB2*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB2* Precedes finite)
     v: (IP-INF-COM* iDoms NP-OB2*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (finite Precedes NP-OB2*)
}

10: { i: (IP-INF-COM* iDoms infinitive) AND (IP-INF-COM* iDoms NP-OB1*) AND (infinitive Precedes NP-OB1*)
      a: (IP-INF-COM* iDoms infinitive) AND (IP-INF-COM* iDoms NP-OB1*) AND (NP-OB1* Precedes infinitive)
}

11: { i: (IP-INF-COM* iDoms infinitive) AND (IP-INF-COM* iDoms NP-OB2*) AND (infinitive Precedes NP-OB2*)
      d: (IP-INF-COM* iDoms infinitive) AND (IP-INF-COM* iDoms NP-OB2*) AND (NP-OB2* Precedes infinitive)
}

12: { a: (IP-INF-COM* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-OB1* Precedes NP-SBJ*)
      s: (IP-INF-COM* iDoms NP-OB1*) AND (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* Precedes NP-OB1*)
}

13: { d: (IP-INF-COM* iDoms NP-OB2*) AND (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-OB2* Precedes NP-SBJ*)
      s: (IP-INF-COM* iDoms NP-OB2*) AND (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-SBJ* Precedes NP-OB2*)
}