add_to_ignore: RPAREN|LPAREN

define: ../../definitions/verbs.def

node: IP*

/*
1 = #...X...X...V
2 = #X...X...V
3 = #...X...V...X
4 = #X...V...X
5 = #...V...X...X
*/

coding_query:

1: { t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB* iDoms [1].*) AND ([1].* iDoms \*ICH\**) AND (NP-OB* Precedes finite) AND ([2].* Precedes finite) AND ([2].* Precedes NP-OB*) AND ([2].* SameIndex \*ICH\**) AND (IP-MAT*|IP-SUB* iDomsFirst [3].*) AND ([3].* iDoms !\**)
     f: ELSE }

2: { t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB* iDoms [1].*) AND ([1].* iDoms \*ICH\**) AND (NP-OB* Precedes finite) AND ([2].* Precedes finite) AND ([2].* Precedes NP-OB*) AND ([2].* SameIndex \*ICH\**) AND (IP-MAT*|IP-SUB* iDomsFirst [2].*)
     f: ELSE }

3: { t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB* iDoms [1].*) AND ([1].* iDoms \*ICH\**) AND (finite Precedes NP-OB*) AND ([2].* Precedes finite) AND ([2].* SameIndex \*ICH\**) AND (IP-MAT*|IP-SUB* iDomsFirst [3].*) AND ([3].* iDoms !\**)
     f: ELSE }

4: { t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB* iDoms [1].*) AND ([1].* iDoms \*ICH\**) AND (finite Precedes NP-OB*) AND ([2].* Precedes finite) AND ([2].* SameIndex \*ICH\**) AND (IP-MAT*|IP-SUB* iDomsFirst [2].*) 
     f: ELSE }

5: { t: (IP-MAT*|IP-SUB* iDoms NP-OB*) AND (IP-MAT*|IP-SUB* iDoms finite) AND (NP-OB* iDoms [1].*) AND ([1].* iDoms \*ICH\**) AND (finite Precedes NP-OB*) AND (finite Precedes [2].*) AND ([2].* Precedes NP-OB*) AND ([2].* SameIndex \*ICH\**)
     f: ELSE }