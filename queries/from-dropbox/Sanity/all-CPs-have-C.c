node: $ROOT

coding_query:

1: { r: (CP* iDoms \**)
     c: (CP* iDoms CP*)
     f: (CP* iDoms !C|C-*)
     t: (CP* iDoms C|C-*)
     o: ELSE
   }
