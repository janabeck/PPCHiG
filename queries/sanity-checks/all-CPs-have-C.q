/* check to be sure that all CPs have some sort of C */

node: $ROOT

query: (CP* Exists) AND NOT(CP* iDoms C|C-*)