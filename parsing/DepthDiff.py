import DepDist
import ConstDist
import matplotlib.pyplot as plt  


sents = DepDist.extract_sentences('rag_script.txt')
dep_parses = DepDist.parse_dict(sents)
const_parses = ConstDist.const_parser(sents)

dependency_depths = {}
for key in dep_parses:
	Dep_Depth = DepDist.depth(dep_parses[key])
	dependency_depths[key] = Dep_Depth

constituency_depths = {}
for key in const_parses:
	Const_Depth = ConstDist.depth(const_parses[key])
	constituency_depths[key] = Const_Depth

def depth_diff(dict1, dict2):
	sent_diff = {}
	diff_freq = {}
	const_greater = {}
	dep_greater = {}
	for key in dict1:
		diff = abs(dict1[key] - dict2[key])
		sent_diff[key] = diff
		try:
			diff_freq[diff] += 1
		except KeyError:
			diff_freq[diff] = 1
		if dict1[key] > dict2[key]:
			const_greater[key] = (dict1[key], dict2[key], diff)
		elif dict1[key] < dict2[key]:
			dep_greater[key] = (dict1[key], dict2[key], diff)
	return (sent_diff, diff_freq, const_greater, dep_greater)


sent_diff, diff_freq, const_greater, dep_greater = depth_diff(constituency_depths, dependency_depths)

# x = list(constituency_depths.values())
# y = list(dependency_depths.values())
# plt.scatter(x, y, alpha=0.8, c="blue")
# plt.xlabel('Constituency Depths')
# plt.ylabel('Dependency Depths')
# plt.savefig("Depth_Diff_Scatter.png")
# plt.show()

print("NUMBER OF CONSTS GREATER", len(const_greater))
print("NUMBER OF DEPS GREATER", len(dep_greater))

# diffs = diff_freq.keys()
# counts = diff_freq.values()
# plt.bar(diffs,counts)
# plt.xlabel("DIFFERENCES")
# plt.ylabel("FREQUENCIES")
# plt.savefig("Diff_Freq_Distribution.png")
# plt.show()