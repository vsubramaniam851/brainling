import sys
import os
import csv
import string

def conllu_to_text(input_path, filename, save_file = False, output_path = None):
	file_path = os.path.join(input_path, filename)
	out_str = ''
	with open(file_path) as csv_file:
		reader = csv.reader(csv_file, delimiter = '\t')
		for row in reader:
			if len(row) > 0:
				if str.lower(row[1]) != 'text':
					out_str = out_str + row[1] + ' '
	if save_file:
		save_name = filename.strip('.conllu') + '.txt'
		assert os.access(output_path, os.W_OK), 'Folder {} has no write permissions.'.format(output_path)
		save_path = os.path.join(output_path, save_name)
		with open(save_path, 'w') as f:
			f.write(out_str)
	return out_str

print(conllu_to_text('/storage/vsub851/parsing/testparses', 'sesame-street-episode-3990.conllu', save_file = True, output_path = '/storage/vsub851/parsing/test-text'))


