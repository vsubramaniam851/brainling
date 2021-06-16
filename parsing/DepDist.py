import stanfordnlp
import matplotlib.pyplot as plt 
import nltk

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
# ret_dict = extract_sentences("rag_script.txt")

def parse_list(dict1):
	out_list = []
	nlp = stanfordnlp.Pipeline()
	for key in dict1:
		for value in dict1[key]:
			doc = nlp(value)
			dep_list = []
			for dep in doc.sentences[0].dependencies:
				dep_list.append((dep[2].text, dep[0].index, dep[1]))
			out_list.append(dep_list)
	return out_list

def parse_dict(dict1):
	out_dict = {}
	nlp = stanfordnlp.Pipeline()
	for key in dict1:
		for value in dict1[key]:
			doc = nlp(value)
			dep_list = []
			for dep in doc.sentences[0].dependencies:
				dep_list.append((dep[2].text, dep[0].index, dep[1]))
			out_dict[value] = dep_list
	return out_dict

def depth(parse):
	heads = [0]
	total_depth = 0
	for p in parse:
		if int(p[1]) not in heads:
			total_depth = total_depth + 1
			heads.append(int(p[1]))
	return total_depth
	
# parse_list = parse_list(ret_dict)
def count_dict(parse_list):
	out_dict = {}
	for parse in parse_list:
		out_depth = depth(parse)
		try:
			out_dict[out_depth] += 1
		except KeyError:
			out_dict[out_depth] = 1
	return out_dict

# depth_dict = count_dict(parse_list)
# depths = depth_dict.keys()
# counts = depth_dict.values()
# plt.bar(depths,counts)
# plt.xlabel("DEPTHS")
# plt.ylabel("FREQUENCIES")
# plt.savefig("Depth_Distribution.png")
# plt.show()