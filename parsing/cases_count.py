import stanfordnlp
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

def case_count(in_dict):
	nlp = stanfordnlp.Pipeline()
	nouns = ["NNP", "NN", "NNS", "NNPS"]
	verbs = ["VB", "VBZ", "VBN", "VBP", "VBG", "VBD"]
	abl = ["by", "from", "in" ,"with", "below", "above", "before"]
	dat = ["to", "for"]
	gen = ["of"]
	cases = {"Datives": 0, "Nominative/Accusative": 0, "Ablative": 0, "Genitive": 0}
	for key in in_dict:
		for val in in_dict[key]:
			doc = nlp(val)
			for sent in doc.sentences:
				for i in range(0, len(sent.words)):
					if sent.words[i].xpos in nouns:
						new_val = val.split()
						try:
							prev_word = new_val[i-1]
							if prev_word in gen:
								cases["Genitive"] += 1
							elif prev_word in dat:
								cases["Datives"] += 1
							elif prev_word in abl:
								cases["Ablative"] += 1
							else:
								cases["Nominative/Accusative"] +=1 
						except IndexError:
							continue
	return cases

sentences = extract_sentences("rag_script.txt")
cases_dict = case_count(sentences)
print(cases_dict)
cases = cases_dict.keys()
counts = cases_dict.values()
plt.bar(cases,counts)
plt.xlabel("CASES")
plt.ylabel("FREQUENCIES")
plt.savefig("Case_Distribution.png")
plt.show()








