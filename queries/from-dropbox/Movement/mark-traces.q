node: $ROOT

query: ({1}[1].* iDoms \*T*|\*ICH*|\*CL*|\*-*) AND ({2}[2].* SameIndex \*T*|\*ICH*|\*CL*|\*-*) AND ([2].* iDoms !\**)

add_internal_node{1}: TRACE
add_internal_node{2}: ANT