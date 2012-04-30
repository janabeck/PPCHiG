%.js: %.waxeye
	waxeye -g javascript . $<
	mv parser.js $@
	sed -i.bak "s/var Parser =/var $(subst -,_,${<:%.waxeye=%_parser}) =/" $@
	rm $@.bak
