add_to_ignore: RPAREN|LPAREN

define: ../../definitions/verbs.def

node: IP-MAT*|IP-SUB*

/*
1: type of verb (v = finite, b = finite 'be', o = ELSE)
2: type of subject (n = nominal, p = pronominal, e = pro, t = trace or discontinuous)
3: infinitive sister of matrix verb? (t/f)
4: type of acc. object (n = nominal, p = pronominal, d = determiner, t = trace or discontinuous)
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

3: { t: (IP-MAT*|IP-SUB* iDoms IP-INF-COM*) AND (IP-INF-COM* iDom \*ICH\**) AND (IP-INF-COM* iDoms infinitive) AND (infinitive iDoms !\*ICH\**)
     f: ELSE
}

4: { p: (infinitive iDoms NP-OB1*) AND (NP-OB1* iDoms PRO*|CLPRO*)
     d: (infinitive iDoms NP-OB1*) AND (NP-OB1* iDomsOnly D*)
     t: (infinitive iDoms NP-OB1*) AND (NP-OB1* Doms \*ICH\**|\*T\**)
     n: (infinitive iDoms NP-OB1*)
}

5: { p: (infinitive iDoms NP-OB2*) AND (NP-OB2* iDoms PRO*|CLPRO*)
     d: (infinitive iDoms NP-OB2*) AND (NP-OB2* iDomsOnly D*)
     t: (infinitive iDoms NP-OB2*) AND (NP-OB2* Doms \*ICH\**|\*T\**)
     n: (infinitive iDoms NP-OB2*)
}