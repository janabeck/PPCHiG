node: $ROOT

copy_corpus: t

query: (*-SPE Doms {1}IP-MAT|IP-SUB|IP-MAT[-=][123456789]|IP-SUB[-=][123456789]|CP*)

append_label{1}: -SPE