node: $ROOT

define: pos_tags.def

coding_query:

// finds all movement traces
1: { t: (\*T\**|\*ICH\**|\*CL\**|\*-* Exists)
     f: ELSE
   }

// finds leftward movement
2: { W: (.* iDoms \**) AND (W* Precedes .*) AND (\** SameIndex W*)
     L: ([1].* iDoms \**) AND ([2].* Precedes [1].*) AND (\** SameIndex [2].*)
     f: ELSE
   }

// finds rightward movement
3: { R: ([1].* iDoms \**) AND ([1].* Precedes [2].*) AND (\** SameIndex [2].*) AND ([2].* iDoms [ABCDEFGHIJKLMNOPQRSTUVWXYZ]*)
     f: ELSE
   }
