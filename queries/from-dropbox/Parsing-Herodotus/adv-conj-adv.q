node: $ROOT

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

copy_corpus: t

query: ([1]{1}ADV|ADVR|ADVS hasSister CONJ)
	AND ([1]ADV|ADVR|ADVS hasSister [2]{2}ADV|ADVR|ADVS)
	AND ([1]ADV|ADVR|ADVS iPrecedes CONJ)
	AND (CONJ iPrecedes [2]ADV|ADVR|ADVS)

add_internal_node{1, 2}: ADVP
