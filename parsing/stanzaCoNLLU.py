import os
import sys
import sentsample
import pandas as pd
import stanza
#Contains all functions for translating a Stanza parse to CoNLLU

def stanzatodicts(sents, nlp, ln = 'en'):
	'''Takes in a list of sentences, parses them, and returns a dictionary that gives the fields for CoNLLU'''
	dicts = []
	for s in sents:
		doc = nlp(s) #Parse sentence
		out_dict = {}
		#Iterate through all words of a sentence.
		for word in doc.sentences[0].words:
			#Obtain all CoNLLU fields -- text, lemma, dependecies, heads, and POS.
			try:
				out_dict['words'].append(word.text)
			except KeyError:
				out_dict['words'] = [word.text]
			try:
				out_dict['predicted_dependencies'].append(word.deprel)
			except KeyError:
				out_dict['predicted_dependencies'] = [word.deprel]
			try:
				out_dict['predicted_heads'].append(str(word.head))
			except KeyError:
				out_dict['predicted_heads'] = [str(word.head)]
			try:
				out_dict['XPOS'].append(word.xpos)
			except KeyError:
				out_dict['XPOS'] = [word.xpos]
			try:
				out_dict['UPOS'].append(word.upos)
			except KeyError:
				out_dict['UPOS'] = [word.upos]
			try:
				out_dict['lemma'].append(word.lemma)
			except KeyError:
				out_dict['lemma'] = [word.lemma]
		#Append to list of dictionary that has a parse of all responses.
		dicts.append(out_dict)
	return dicts

def dict_to_dataframe(dict1):
	'''Takes in a dictionary with all CoNLLU fields and places them in dataframe. for conversion to CoNLLU'''
	extracted_dict = {}
	extracted_dict['FORM'] = dict1['words']
	extracted_dict['DEPREL'] = dict1['predicted_dependencies']
	extracted_dict['HEAD'] = dict1['predicted_heads']
	underscore = []
	#Put underscore for MISC and maybe LEMMA if necessary to indicate that they do not need to occur. 
	for i in range(0, len(dict1['words'])):
		underscore.append('_')
	extracted_dict['MISC'] = underscore
	# extracted_dict['LEMMA'] = underscore
	extracted_dict['UPOS'] = dict1['UPOS']
	extracted_dict['XPOS'] = dict1['XPOS']
	extracted_dict['LEMMA'] = dict1['lemma']
	#Create dataframe from dictionary with correct fields
	resp_df = pd.DataFrame.from_dict(extracted_dict)
	return resp_df

def convert_dataframe_to_conllu(df, conllu_str=''):
	'''Takes in dataframe with all CoNLLU fields and converts to CoNLLU string'''
	line_num = 1
	prev_end = 0 
	for i in df.index:
		row = df.loc[i]
		#Line number we are on
		conllu_str += str(line_num) + '\t'
		#Add FORM, LEMMA, UPOS, XPOS, HEAD, DEPREL, and MISC
		conllu_str += df.loc[i, 'FORM'] + '\t'
		conllu_str += df.loc[i, 'LEMMA'] + '\t'
		conllu_str += df.loc[i, 'UPOS'] + '\t'
		conllu_str += df.loc[i, 'XPOS'] + '\t'
		# Mark empty for FEATS
		conllu_str += '_\t'  
		conllu_str += df.loc[i, 'HEAD'] + '\t'
		conllu_str += df.loc[i, 'DEPREL'] + '\t'
		conllu_str += '_\t'  # Mark empty for DEPS
		conllu_str += df.loc[i, 'MISC']
		#Add new line for end of sentence
		conllu_str += '\n'
		line_num += 1
	conllu_str += '\n'           
	return conllu_str

def parse_list(list1):
	'''Given list of parse responses from stanzatodict, convert to CoNLLU string
	This was rewritten in the movieparses.py file to be more usable.
	'''
	df_list = []
	for resp in list1:
		df_list.append(dict_to_dataframe(resp)) #convert to dataframe
	con_str = ''
	for df in df_list:
		out_string = convert_dataframe_to_conllu(df) #Convert to CoNLLU
		con_str = con_str + out_string
	return con_str