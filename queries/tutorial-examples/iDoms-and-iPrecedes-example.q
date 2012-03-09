node: $ROOT

//print_indices: t

query: (NP-* iDoms D*) AND 
       (NP-* iDoms N*) AND 
       (NP-* iDoms PP|NP-*) AND 
       (D* iPrecedes PP|NP-*) AND 
       (PP|NP-* iPrecedes N*)