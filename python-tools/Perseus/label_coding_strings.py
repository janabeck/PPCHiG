import sys
import re

def main():
	in_file = open(sys.argv[1], 'rU')

	out_file = open(sys.argv[2], 'w')

	num = re.compile('\d+')

	code_key = {'v:e:n:-:o:-:f:f:f': ['xOVx', 'OV', 'verb-medial'],
				'v:e:n:-:o:-:f:f:t': ['OV$', 'OV', 'verb-final'],
				'v:e:n:-:v:-:f:f:f': ['xVOx', 'VO', 'verb-medial'],
				'v:e:n:-:v:-:f:t:f': ['^VOx', 'VO', 'verb-initial'],
				'v:e:n:s:o:o:f:f:f': ['xOVx', 'OV', 'verb-medial'],
				'v:e:n:s:o:o:f:f:t': ['OV$', 'OV', 'verb-final'],
				'v:e:n:s:v:s:f:f:f': ['xVOx', 'VO', 'verb-medial'],
				'v:e:n:v:v:o:f:t:f': ['^VOx', 'VO', 'verb-initial'],
				'v:n:n:s:o:o:f:f:f': ['OSVx', 'OV', 'verb-medial'],
				'v:n:n:s:o:o:f:f:t': ['OSV$', 'OV', 'verb-final'],
				'v:n:n:s:o:s:f:f:f': ['SOVx', 'OV', 'verb-medial'],
				'v:n:n:s:o:s:f:f:t': ['SOV$', 'OV', 'verb-final'],
				'v:n:n:s:v:s:f:f:f': ['SVO', 'VO', 'verb-medial'],
				'v:n:n:v:o:o:f:f:f': ['OVS', 'OV', 'verb-medial'],
				'v:n:n:v:v:o:f:f:f': ['xVOS', 'VO', 'verb-medial'],
				'v:n:n:v:v:o:f:t:f': ['^VOS', 'VO', 'verb-initial'],
				'v:n:n:v:v:s:f:f:f': ['xVSO', 'VO', 'verb-medial'],
				'v:n:n:v:v:s:f:t:f': ['^VSO', 'VO', 'verb-initial']}

	ov = 0.0

	ov_pairs = {}

	vo = 0.0

	vo_pairs = {}

	verb_initial = {}

	vi = 0.0

	verb_medial = {}

	vm = 0.0

	verb_final = {}

	vf = 0.0

	for line in in_file:
		for key in code_key:
			if line.find(key) != -1:
				m = num.search(line)
				if m:
					n = int(m.group(0))
					if code_key[key][1] == 'OV':
						ov += n
						ov_pairs[key + " " + code_key[key][0]] = n
					elif code_key[key][1] == 'VO':
						vo += n
						vo_pairs[key + " " + code_key[key][0]] = n
					if code_key[key][2] == 'verb-initial':
						vi += n
						verb_initial[key + " " + code_key[key][0]] = n
					elif code_key[key][2] == 'verb-medial':
						vm += n
						verb_medial[key + " " + code_key[key][0]] = n
					elif code_key[key][2] == 'verb-final':
						vf += n
						verb_final[key + " " + code_key[key][0]] = n

	total1 = ov + vo

	total2 = vi + vm + vf

	s1 = sorted(ov_pairs, key=ov_pairs.__getitem__, reverse=True)

	s2 = sorted(vo_pairs, key=vo_pairs.__getitem__, reverse=True)

	v1 = sorted(verb_initial, key=verb_initial.__getitem__, reverse=True)

	v2 = sorted(verb_medial, key=verb_medial.__getitem__, reverse=True)

	v3 = sorted(verb_final, key=verb_final.__getitem__, reverse=True)

	print >> out_file, "OV Sentences: " + str(ov) + " (" + str(round(((ov/total1) * 100), 2)) + "%)"
	print >> out_file

	for i in s1:
		print >> out_file, "\t" + i + "\t" + str(ov_pairs[i]) + " (" + str(round(((ov_pairs[i]/total1)*100),2)) + "%)"

	print >> out_file
	print >> out_file, "VO Sentences: " + str(vo) + " (" + str(round(((vo/total1) * 100),2)) + "%)"
	print >> out_file

	for i in s2:
		print >> out_file, "\t" + i + "\t" + str(vo_pairs[i]) + " (" + str(round(((vo_pairs[i]/total1)*100),2)) + "%)"

	print >> out_file
	print >> out_file, "Verb-initial Sentences: " + str(vi) + " (" + str(round(((vi/total2) * 100),2)) + "%)"
	print >> out_file

	for i in v1:
		print >> out_file, "\t" + i + "\t" + str(verb_initial[i]) + " (" + str(round(((verb_initial[i]/total2)*100),2)) + "%)"

	print >> out_file
	print >> out_file, "Verb-medial Sentences: " + str(vm) + " (" + str(round(((vm/total2) * 100),2)) + "%)"
	print >> out_file

	for i in v2:
		print >> out_file, "\t" + i + "\t" + str(verb_medial[i]) + " (" + str(round(((verb_medial[i]/total2)*100),2)) + "%)"

	print >> out_file
	print >> out_file, "Verb-final Sentences: " + str(vf) + " (" + str(round(((vf/total2) * 100),2)) + "%)"
	print >> out_file

	for i in v3:
		print >> out_file, "\t" + i + "\t" + str(verb_final[i]) + " (" + str(round(((verb_final[i]/total2)*100),2)) + "%)"

	print >> out_file

if __name__ == '__main__':
	main()