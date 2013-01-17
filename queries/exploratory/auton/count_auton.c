add_to_ignore: RPAREN|LPAREN

node: IP-MAT*|IP-SUB*

/*
1: form of αὐτός is preverbal or postverbal
2: form of αὐτός is only word in phrase
3: case of αὐτός
4: form of αὐτός precedes subject
*/

coding_query:

1: { b: (IP-MAT*|IP-SUB* iDoms NP-OB*-PRV)
     a: (IP-MAT*|IP-SUB* iDoms NP-OB*-PSTV)
}

2: { t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* iDomsOnly PRO*) AND (PRO* iDoms *-αὐτός)
     f: ELSE
}

3: { a: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* iDoms PRO-ACC*)
     d: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* iDoms PRO-DAT*)
     g: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* iDoms PRO-GEN*)
}

4: { t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (NP-OB* iDomsOnly PRO*) AND (PRO* iDoms *-αὐτός) AND (IP-MAT*|IP-SUB* iDoms NP-SBJ*) AND (NP-OB* Precedes NP-SBJ*) AND (NP-SBJ* iDoms !\*pro\**)
     f: ELSE
}
