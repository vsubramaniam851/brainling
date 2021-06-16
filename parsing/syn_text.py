import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 
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
# count = 0
# for key in out_dict:
# 	for value in out_dict[key]:
# 		value_list = value.split()
# 		if "?" in value and len(value_list) > 2:
# 			count = count + 1
# 			print(value)
# print("COUNT IS", count)
# count1 = 0
# for key in out_dict:
# 	for value in out_dict[key]:
# 		if "either" in value: #and "or" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		if "both" in value and "and" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		if "If" in value: #and "then" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		if "neither" in value and "nor" in value:
# 			count1 = count1 + 1
# 			print(value)
# print("NEW COUNT IS", count1)

# count1 = 0
# count2 = 0
# for key in out_dict:
# 	for value in out_dict[key]:
# 		if "I" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		elif "me" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		elif "They" in value or "they" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		elif "them" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		elif "He" in value or "he" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		elif "She" in value or "she" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		elif "him" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		elif "her" in value:
# 			count1 = count1 + 1
# 			print(value)
# 		if(len(value.split()) == 1):
# 			print("THIS IS LENGTH 1:", value)
# 		if len(value.split()) > 1:
# 			count2 = count2 + 1
# print("NEW COUNT IS", count1)
# print(count2)
overall_count = 0
for i in out_dict:
	for v in out_dict[i]:
		# print(v)
		overall_count = overall_count + 1
nominative_count = 0
accusative_count = 0
for key in out_dict:
	for value in out_dict[key]:
		value_list = value.split()
		if "I" in value_list or "they" in value_list or "They" in value_list or "He" in value_list or "he" in value_list or "We" in value_list or "we" in value_list or "She" in value_list or "she" in value_list:
			nominative_count = nominative_count + 1
		if "me" in value_list or "them" in value_list or "her" in value_list or "him" in value_list or "us" in value_list or "Me" in value_list or "Us" in value_list or "Her" in value_list or "Him" in value_list or "Them" in value_list:
			accusative_count = accusative_count + 1

cases = ["Nominative", "Accusative", "Overall"]
x_pos = [i for i, _ in enumerate(cases)]
counts = [nominative_count, accusative_count, overall_count]
plt.bar(x_pos,counts)
plt.xticks(x_pos, cases)
plt.savefig('cases.png')
plt.show()
statives = ["adore", "agree", "appear", "seem", "appreciate", "be", "exist", "believe", "belong", "concern", "consist of", "contain", "cost", "deny", "depend", "deserve", "detest", "disagree", "dislike", "doubt", "equal", "feel", "hate", "hear", "imagine", "include", "involve", "know", "lack", "like", "loathe", "look", "love", "matter", "mean", "measure", "mind", "need", "owe", "own", "possess", "promise", "realize", "recognize", "remember", "resemble", "satisfy", "see", "smell", "sound", "suppose","surprise", "taste", "think", "understand", "want", "weigh", "wish"]
stative_count = 0
non_stative = 0
overall = 0
lemmatizer = WordNetLemmatizer() 
for key in out_dict:
	for value in out_dict[key]:
		value_list = value.split()
		for v in value_list:
			v = lemmatizer.lemmatize(v)
			if v.lower() in statives:
				stative_count = stative_count + 1
			else:
				non_stative = non_stative + 1
			overall = overall + 1

types = ["Stative", "Dynamic", "Overall"]
x_pos = [i for i, _ in enumerate(types)]
counts = [stative_count, non_stative, overall]
print(counts)
plt.bar(x_pos,counts)
plt.xticks(x_pos, types)
plt.savefig('statives.png')
plt.show()
lengths = {}
for key in out_dict:
	for val in out_dict[key]:
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

