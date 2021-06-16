import stanfordnlp
import pandas as pd
import sentsample

def stanfordtodict(sents):
	'''Takes in a list of sentences, parses them, and returns a dictionary that gives the fields for CoNLLU'''
	nlp = stanfordnlp.Pipeline()
	#initialize stanfordnlp pipeline
	dicts = []
	for s in sents:
		doc = nlp(s)
		dep_list = []
		for sent in doc.sentences:
			for dep in sent.dependencies:
				#Append the dependency label, root, and head
				dep_list.append((dep[2].text, dep[0].index, dep[1]))
		out_dict = {}
		#Collect all the fields we need to store
		for d in dep_list:
			try:
				out_dict["words"].append(d[0])
			except KeyError:
				out_dict["words"] = [d[0]]				
			try:
				out_dict["predicted_dependencies"].append(d[2])
			except KeyError:
					out_dict["predicted_dependencies"] = [d[2]]
			try:
				out_dict["predicted_heads"].append(d[1])
			except KeyError:
				out_dict["predicted_heads"] = [d[1]]
		for sent in doc.sentences:
			#Need to go to the words level in StanfordNLP to extract POS information and lemma information
			for word in sent.words:
				try:
					out_dict["XPOS"].append(word.xpos)
				except KeyError:
					out_dict["XPOS"] = [word.xpos]
				try:
					out_dict["UPOS"].append(word.upos)
				except KeyError:
					out_dict["UPOS"] = [word.upos]
				try:
					out_dict["lemma"].append(word.lemma)
				except:
					out_dict["lemma"] = [word.lemma]
		dicts.append(out_dict)
	return dicts

def dict_to_dataframe(dict1):
	'''Takes in a dictionary with all CoNLLU fields and places them in dataframe. for conversion to CoNLLU'''
	extracted_dict = {}
	extracted_dict["FORM"] = dict1["words"]
	extracted_dict["DEPREL"] = dict1["predicted_dependencies"]
	extracted_dict["HEAD"] = dict1["predicted_heads"]
	underscore = []
	for i in range(0, len(dict1["words"])):
		underscore.append("_")
	extracted_dict["MISC"] = underscore
	extracted_dict["LEMMA"] = underscore
	extracted_dict["UPOS"] = dict1["UPOS"]
	extracted_dict["XPOS"] = dict1["XPOS"]
	extracted_dict["LEMMA"] = dict1["lemma"]
	resp_df = pd.DataFrame.from_dict(extracted_dict)
	return resp_df

def convert_dataframe_to_conllu(df, conllu_str=''):
	'''Takes in dataframe with all CoNLLU fields and converts to CoNLLU string'''
    line_num = 1
    prev_end = 0 
    for i in df.index:
        row = df.loc[i]
        conllu_str += str(line_num) + '\t'
        conllu_str += df.loc[i, 'FORM'] + '\t'
        conllu_str += df.loc[i, 'LEMMA'] + '\t'
        conllu_str += df.loc[i, 'UPOS'] + '\t'
        conllu_str += df.loc[i, 'XPOS'] + '\t'
        conllu_str += '_\t'  # Mark empty for FEATS
        conllu_str += df.loc[i, 'HEAD'] + '\t'
        conllu_str += df.loc[i, 'DEPREL'] + '\t'
        conllu_str += '_\t'  # Mark empty for DEPS
        conllu_str += df.loc[i, 'MISC']
        conllu_str += '\n'
        line_num += 1
    conllu_str += '\n'
            
    return conllu_str

def parse_list(list1):
	'''Given list of parse responses from stanzatodict, convert to CoNLLU string'''
	df_list = []
	for resp in list1:
		df_list.append(dict_to_dataframe(resp)) #Convert to dataframe
	con_str = ''
	for df in df_list:
		out_string = convert_dataframe_to_conllu(df)
		#Get CoNLLU string
		con_str = con_str + out_string
	return con_str