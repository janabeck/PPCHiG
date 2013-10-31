node: $ROOT

query: (D* iPrecedes {1}Q*) AND (Q* iPrecedes N*|ADJ*) AND (D* hasSister Q*) AND (Q* hasSister N*|ADJ*)

add_internal_node{1}: FLAG
