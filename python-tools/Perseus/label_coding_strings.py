import sys
import re

def main():
	in_file = open(sys.argv[1], 'rU')

	out_file = open(sys.argv[2], 'w')

	num = re.compile('\d+')

	code_key = {'v:e:n:-:o:-:f:f:f': ['xOVx', 'OV'],
				'v:e:n:-:o:-:f:f:t': ['OV$', 'OV'],
				'v:e:n:-:v:-:f:f:f': ['xVOx', 'VO'],
				'v:e:n:-:v:-:f:t:f': ['^VOx', 'VO'],
				'v:n:n:s:o:o:f:f:f': ['OSVx', 'OV'],
				'v:n:n:s:o:o:f:f:t': ['OSV$', 'OV'],
				'v:n:n:s:o:s:f:f:f': ['SOVx', 'OV'],
				'v:n:n:s:o:s:f:f:t': ['SOV$', 'OV'],
				'v:n:n:s:v:s:f:f:f': ['SVO', 'VO'],
				'v:n:n:v:o:o:f:f:f': ['OVS', 'OV'],
				'v:n:n:v:v:o:f:f:f': ['xVOS', 'VO'],
				'v:n:n:v:v:o:f:t:f': ['^VOS', 'VO'],
				'v:n:n:v:v:s:f:f:f': ['xVSO', 'VO'],
				'v:n:n:v:v:s:f:t:f': ['^VSO', 'VO']}

	ov = 0

	ov_pairs = {}

	vo = 0

	vo_pairs = {}

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

	s1 = sorted(ov_pairs, key=ov_pairs.__getitem__, reverse=True)

	s2 = sorted(vo_pairs, key=vo_pairs.__getitem__, reverse=True)

	print >> out_file, "OV Sentences: " + str(ov)
	print >> out_file

	for i in s1:
		print >> out_file, "\t" + i + "\t" + str(ov_pairs[i])

	print >> out_file
	print >> out_file, "VO Sentences: " + str(vo)
	print >> out_file

	for i in s2:
		print >> out_file, "\t" + i + "\t" + str(vo_pairs[i])

if __name__ == '__main__':
	main()