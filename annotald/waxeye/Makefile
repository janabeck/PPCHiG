%.js: %.waxeye
	waxeye -g javascript . $<
	mv parser.js $@
	sed -i -e "s/var Parser =/var $(subst -,_,${<:%.waxeye=%_parser}) =/" $@
