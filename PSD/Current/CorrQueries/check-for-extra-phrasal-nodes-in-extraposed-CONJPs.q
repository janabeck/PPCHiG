node: $ROOT

query: (CONJP-* domsWords 2) AND (CONJP-* iDoms {1}ADJP*|ADVP*|CONJP*|CP*|INTJP*|IP*|NP*|NUMP*|PP*|QP*|QTP*|RRC*)

add_internal_node{1}: FLAG
