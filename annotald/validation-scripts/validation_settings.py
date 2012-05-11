import re

cases = ["-NOM","-GEN","-ACC","-DAT"]

sing = ["N","NPR","ADJ","Q","CLQ","OTHER"]

pl = ["NS","NPRS","ADJ","Q","CLQ","OTHER"]

numbers = [(sing, ["D"], ["DEM"]), (pl, ["DS"],["DEMS"])]

ignore = re.compile("CLPRT*|CLTE*|CLGE*|CLPRO*")

nom = ["N","NPR","NS","NPRS","ADJ","Q","CLQ","OTHER"]

np_re = re.compile("|".join(map(lambda x: "NP" + x, cases)))

pro_re = re.compile("|".join(map(lambda x: "PRO" + x, cases) + map(lambda x: "CLPRO" + x, cases)))

det = ["D","DS"]

dem = ["DEM","DEMS"]

quant = ["Q","CLQ"]

all_together = ["N","NPR","NS","NPRS","D","DEM","DS","DEMS","ADJ","Q","CLQ","OTHER"]

all_cases = []

for item in all_together:
    for case in cases:
        all_cases.append(item+case)
