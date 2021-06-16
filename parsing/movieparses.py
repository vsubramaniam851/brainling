import os
import sys
import csv
import stanza
import nltk
import stanzaCoNLLU
import argparse

sys.setrecursionlimit(100000)

def get_cmd_arguments():
	'''Obtain command line arguments to run the movie parsing. Need language, input path, and output path.'''
	ap = argparse.ArgumentParser()

	ap.add_argument('-m', '--movies', nargs = '*', action = 'store', type = str, dest = 'movies', 
		default = ['ant-man', 'aquaman', 'avengers-infinity-war', 'black-panther', 'cars-2', 'charlie-and-the-chocolate-factory', 'coraline', 'fantastic-mr-fox', 'guardians-of-the-galaxy', 'guardians-of-the-galaxy-2', 'home-alone-2', 'incredibles', 'in-the-shadow-of-the-moon', 'lotr-1', 'lotr-2', 'megamind', 'sesame-street-episode-3990', 'shrek-the-third', 'spider-man-3-homecoming', 'spider-man-far-from-home', 'tank-chase', 'the-martian', 'thor-ragnarok', 'toy-story', 'toy-story-3-spanish', 'venom', 'wreck-it-ralph-spanish'], help = 'The movie names that we want to parse.')
	ap.add_argument('-i', '--input_path', nargs = '?', action = 'store', type = str, dest = 'input_path', default = '/storage/datasets/neuroscience/ecog/transcripts',
		help = 'Location of datasets and movie scripts')
	ap.add_argument('-l', '--location', nargs = '?', action = 'store', type = str, dest = 'loc', default = '/manual', 
		help = 'The local directory of the movie script.')
	ap.add_argument('-c', '--csv', nargs = '?', action = 'store', type = bool, dest = 'is_csv', default = False,
		help = '.csv file or .txt file')
	ap.add_argument('-fn', '--filename', nargs = '?', action = 'store', type = str, dest = 'filename', default = 'syntax-text.txt',
		help = 'File name that has information')
	ap.add_argument('-ln', '--language', nargs = '?', action = 'store', type = str, dest = 'ln', default = 'en', 
		help = 'Language that we want to parse in.')
	ap.add_argument('-o', '--output_path', nargs = '?', action = 'store', type = str, dest = 'out_path', default = '/storage/vsub851/parsing/stanford-syntax',
		help = 'Folder where output should be stored.')
	return ap.parse_args()

def csv_to_text(input_path):
	'''Convert CSV to TXT.'''
	out_str = ''
	with open(input_path) as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			#Second entry has text but do not want to grab column name "text" so we skip this
			if row[1] != 'text':
				out_str += row[1]
	return out_str

def parse_list(base_path, nlp, movie_name, save_file = True, loc = '/manual', filename = 'syntax-text.txt', is_csv = False, output = 'storage/vsub851/stanford-syntax'):
	'''
	Takes movie script from text file as input and feeds it to the stanza dependency parser to get a parse response. 
	'''
	movie_name_manual = movie_name + loc
	movie_dir_path = os.path.join(base_path, movie_name_manual) #Input movie path
	if os.path.exists(movie_dir_path): #If input path exists
		print('Now parsing:', movie_name)
		full_text = os.path.join(movie_dir_path, filename)
		if is_csv:
			text = csv_to_text(full_text)
		else:
			f1 = open(full_text, 'r')
			text = f1.read()
		#Use NLTK sentence tokenizer to read in the sentences
		sents = nltk.sent_tokenize(text)
		clean_sents = []
		for s in sents:
			#Remove unwanted symbols such as @
			new_sent = s.replace('@', '')
			clean_sents.append(new_sent)
		parses = stanzaCoNLLU.stanzatodicts(clean_sents, nlp = nlp) #Convert sentences to parses in dictionary
		df_list = []
		for resp in parses:
			#Convert dictionary to pandas dataframe
			df_list.append(stanzaCoNLLU.dict_to_dataframe(resp))
		con_str = ''
		for df in df_list:
			#Convert dataframe to CoNLLU
			out_string = stanzaCoNLLU.convert_dataframe_to_conllu(df)
			con_str = con_str + out_string
		if save_file:
			save_path = output
			assert os.access(save_path, os.W_OK), 'Folder {} has no write permissions.'.format(save_path)
			save_name = movie_name + '.conllu'
			conllu_path = os.path.join(save_path, save_name)
			with open(conllu_path, 'w') as f:
				f.write(con_str)
		return con_str
	else:
		print('Movie path does not exist!')
		return None 

def main():
	'''Get command arguments from the command argument function and run the parse_list function'''
	args = get_cmd_arguments()
	input_path = args.input_path
	movies = args.movies
	loc = args.loc
	is_csv = args.is_csv
	file_name = args.filename
	language = args.ln
	output_path = args.out_path
	movies_not_covered = []
	#Initialize pipeline and pass it in as a function to be called so we don't need to initialize for every movie.
	nlp = stanza.Pipeline(language)
	for m in movies:
		out = parse_list(base_path = input_path, nlp = nlp, movie_name = m, loc = loc, filename = file_name, is_csv = is_csv, output = output_path)
		if out == None:
			movies_not_covered.append(m)
	print('Movies not parsed:', movies_not_covered)

if __name__ == '__main__':
	main()
