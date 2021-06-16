import os
import random 
import stanzaCoNLLU
import nltk

def movie_reading(base_path, movie_name):
	'''Args: base_path is the path to the movie
	         movies_name is the name of the movie to read
	   Outputs: The sentences of the movie text file, using the sentence tokenizer from NLTK
	'''
	movie_name_manual = movie_name + '/manual'
	movie_dir_path = os.path.join(base_path, movie_name_manual) #input path with text file
	if os.path.exists(movie_dir_path):
		full_text = os.path.join(movie_dir_path, 'syntax-text.txt')
		f1 = open(full_text, "r")
		sents = nltk.sent_tokenize(f1.read())
		return sents
	else:
		return []

def sent_sample(movies, base_path = '/storage/vsub851/movie_scripts', k = 100):
	'''Randomly sample k sentences from a text file for the movie text'''
	sentences = []
	for m in movies:
		sentences = sentences + movie_reading(base_path, m) #Call movie_reading to obtain sentences
	#Use random.sample to sample k times from the sentences
	sampled_sentence = random.sample(sentences, k)
	f1 = open('SampledSentence.txt', 'w')
	f1.write(sampled_sentence)
	return sampled_sentence

def stanza_parse(sents, save_file = True):
	'''Obtain CoNLLUs from Stanza parses '''
	parses = stanzaCoNLLU.stanzatodicts(clean_sents) #Convert stanza parse to dictionary
	df_list = []
	for resp in parses:
		df_list.append(stanzaCoNLLU.dict_to_dataframe(resp))
	con_str = ''
	for df in df_list:
		out_string = stanzaCoNLLU.convert_dataframe_to_conllu(df)
		con_str = con_str + out_string
	if save_file:
		save_path = '/storage/vsub851'
		assert os.access(save_path, os.W_OK), 'Folder {} has no write permissions.'.format(save_path)
		save_name =  'stanza.conllu'
		conllu_path = os.path.join(save_path, save_name)
		with open(conllu_path, 'w') as f:
			f.write(con_str)
	return con_str

def coreNLP_parse(sents):
	'''Parse the sentences using CoreNLP and give the output as conllu format'''
	command = 'java -cp \"*\" -mx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,depparse'
	text_file = 'SampledSentence.txt'
	command = command + ' -file ' + text_file + ' -outputFormat conllu'
	os.system(command)
	return 'Finished'

movies = ['ant-man', 'aquaman', 'avengers-infinity-war', 'black-panther', 'cars-2', 'charlie-and-the-chocolate-factory', 'coraline', 'fantastic-mr-fox', 'guardians-of-the-galaxy', 'guardians-of-the-galaxy-2', 'home-alone-2', 'incredibles', 'in-the-shadow-of-the-moon', 'lotr-1', 'lotr-2', 'megamind', 'sesame-street-episode-3990', 'shrek-the-third', 'spider-man-3-homecoming', 'spider-man-far-from-home', 'tank-chase', 'the-martian', 'thor-ragnarok', 'toy-story', 'toy-story-3-spanish', 'venom', 'wreck-it-ralph-spanish']
sents = sent_sample(movies)


