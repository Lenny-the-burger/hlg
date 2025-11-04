# Clean the embedding file by removing not needed parts

# read line by line and write to new file based on if the word (first sep by ' ') complies
# only keep words that only contain characters a-z or the "-" character

import re
def clean_embedding_file(input_file, output_file):
	# make output file

	# match letters and -
	pattern = re.compile(r'^[0-9a-zA-Z-]+$')
	
	linecount = 0
	with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
		for line in infile:
			word = line.split(' ')[0]
			if pattern.match(word):
				outfile.write(line)

			# if the word is only one chartacter add it
			elif len(word) == 1:
				outfile.write(line)

			linecount += 1
			if linecount % 100000 == 0:
				print(f"Processed {linecount} lines")


if __name__ == "__main__":
	inflile = "C:\\Users\\tednb\\source\\repos\\hlg\\data\\data-emb\\glove-50\\wiki_giga_2024_100_MFT20_vectors_seed_2024_alpha_0.75_eta_0.05.050_combined.txt"
	outfile = "C:\\Users\\tednb\\source\\repos\\hlg\\data\\data-emb\\glove-50\\cleaned.txt"
	clean_embedding_file(inflile, outfile)