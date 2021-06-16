import os
import conllu
from conllu import parse


def conllu_to_sentences(base_path, movie, save_path = '/storage/vsub851/parsed_text', save_file = True):
	movie_file = movie + '.conllu'
	conllu_file = os.path.join(base_path, movie_file)
	if os.path.exists(conllu_file):
		f1 = open(conllu_file, 'r')
		conllu_text = f1.read()
		sentences = parse(conllu_text)
		if save_file:
			save_name = movie + '-parse.txt'
			conllu_save=  os.path.join(save_path, save_name)
			f2 = open(conllu_save, 'w')
			text = ''
			for sent in sentences:
				for token in sent:
					if token['form'] != '.' and token['form'] != ',' and token['form'] != '\'':
						text = text + ' ' + token['form']
					else:
						text = text + token['form']
			f2.write(text)
		return text
	else:
		return 'Path not found'

movies = ['shrek-the-third', 'megamind']
for m in movies:
	output = conllu_to_sentences(base_path = '/storage/vsub851/stanford-syntax', movie = m)
	print(output)



