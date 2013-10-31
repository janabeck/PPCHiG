node: $ROOT

query: ([1]BE*|BP*|VB*|VP* Precedes [1]BE*|BP*|VB*|VP*) AND 
([1]BE*|BP*|VB*|VP* hasSister [2]BE*|BP*|VB*|VP*) AND 
({1}[3]BE*|BP*|VB*|VP* iDoms [1]BE*|BP*|VB*|VP*)

add_leaf_before{1}: (FLAG 0)