node: $ROOT

coding_query:

1: { f: (IP-MAT*|IP-SUB* iDoms VBN*|BEN*) AND NOT (VBN*|BEN* SameIndex .*)
     t: (IP-INF* iDoms VBN*|BEN*)
   }
