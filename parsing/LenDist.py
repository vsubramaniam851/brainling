import nltk
import matplotlib.pyplot as plt  

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

out_dict = extract_sentences("rag_script.txt")
lengths = {}
for key in out_dict:
	for val in out_dict[key]:
		val = val.split()
		leng = len(val)
		try:
			lengths[leng] += 1
		except KeyError:
			lengths[leng] = 1
length = lengths.keys()
counts = lengths.values()
plt.bar(length,counts)
plt.xlabel("LENGTHS")
plt.ylabel("FREQUENCIES")
plt.savefig("LengthsDistribution.png")
plt.show()
