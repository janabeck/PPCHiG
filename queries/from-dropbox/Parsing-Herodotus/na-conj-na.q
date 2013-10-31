define: Accusative.def

ignore_nodes: COMMENT|CODE|ID|LB|'|\"|E_S|\.|/|RMV:*|CLPRT|CLTE

node: $ROOT

copy_corpus: t

query: ([1]{1}nominal hasSister CONJ)
	AND ([1]nominal hasSister [2]{2}nominal)
	AND ([1]nominal iPrecedes CONJ)
	AND (CONJ iPrecedes [2]nominal)

add_internal_node{1, 2}: NP
