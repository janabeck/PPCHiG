define: Accusative.def

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE


node: $ROOT

copy_corpus: t

query: ([1]{1}pronoun hasSister CONJ)
	AND ([1]pronoun hasSister [2]{2}pronoun)
	AND ([1]pronoun iPrecedes CONJ)
	AND (CONJ iPrecedes [2]pronoun)

add_internal_node{1, 2}: NP
