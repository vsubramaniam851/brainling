from pycorenlp import StanfordCoreNLP
import nltk
import matplotlib.pyplot as plt
nlp = StanfordCoreNLP('http://localhost:9000')

def const_parser(dict1):
	parses = {}
	for key in dict1:
		for val in dict1[key]:
			output = nlp.annotate(val, properties = {'annotators':'parse', 'outputFormat': 'json'})
			parse = output['sentences'][0]['parse']
			parses[val] = parse
	return parses

def depth(parse):
	count = 0
	reverse_parse = parse[::-1]
	index = 0
	for i in range(0, len(reverse_parse)):
		if reverse_parse[i] == '\n':
			index = i
			break
	leftover = reverse_parse[index+1:]
	for char in leftover:
		if char == ")":
			count = count + 1
		else:
			break
	count = count + 1
	return count

def depth_dist(parses):
	depth_dist = {}
	for key in parses:
		val = parses[key]
		out_depth = depth(val)
		try:
			depth_dist[out_depth] += 1
		except KeyError:
			depth_dist[out_depth] = 1
	return depth_dist

def extract_sentences(filename):
	script = open(filename, "r")
	script_lines = script.readlines()
	speaker_dict = {}
	for line in script_lines:
		lines_list = line.split()
		if lines_list:
			range1 = 0
			for i in range(len(lines_list)):
				if ":" in lines_list[i]: #Find word with ":" 
					speaker = lines_list[:i+1]
					range1 = i+1
			speaker = ' '.join(speaker)
			speaker1 = speaker[:len(speaker) - 1]
			sents = ' '.join(lines_list[range1:])
			sent_list = nltk.sent_tokenize(sents)
			try:
				for s in sent_list:
					speaker_dict[speaker1].append(s)
			except KeyError:
				speaker_dict[speaker1] = sent_list
	return speaker_dict
# sentences = extract_sentences("rag_script.txt")
# parses = const_parser(sentences)
# depth_dict = depth_dist(parses)
# depths = depth_dict.keys()
# counts = depth_dict.values()
# plt.bar(depths,counts)
# plt.xlabel("DEPTHS")
# plt.ylabel("FREQUENCIES")
# plt.savefig("Const_Depth_Distribution.png")
# plt.show()
