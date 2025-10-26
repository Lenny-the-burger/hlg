# Script to download and prepare the data you need

# Make sure dirs exist
mkdir -p ./data-train/
mkdir -p ./data-emb/
mkdir -p ./tmp/

# record what we have
touch data.txt

# clobber data.txt
echo "=data:" > data.txt
echo "_data-train:" >> data.txt

# Simple english Wikipedia dataset from Kaggle (171MB)
# Do we already have it?
if [ -f ./data-train/plain-wikitext/AllCombined.txt ]; then
	echo "Simple English Wikipedia dataset already exists, skipping download."
else
	echo "Downloading Simple English Wikipedia dataset..."
	echo""
	mkdir -p ./data-train/plain-wikitext/
	curl -L -o ./tmp/plain-text-wikipedia-simpleenglish.zip https://www.kaggle.com/api/v1/datasets/download/ffatty/plain-text-wikipedia-simpleenglish && \
	unzip ./tmp/plain-wikitext/plain-text-wikipedia-simpleenglish.zip -d ./data-train/plain-wikitext/
	echo "Done"
	echo ""
fi
echo "plain-wikitext" >> data.txt

echo "" >> data.txt
echo "_data-emb:" >> data.txt

# GloVe embedding (560MB) - (p sure they throttle downloads so might take a while)
# Do we already have it?
if [ -f ./data-emb/glove-50/wiki_giga_2024_100_MFT20_vectors_seed_2024_alpha_0.75_eta_0.05.050_combined.txt ]; then
	echo "GloVe embeddings already exist, skipping download."
else
	echo "Downloading GloVe embeddings..."
	echo ""
	mkdir -p ./data-emb/glove-50/
	curl -L -o ./tmp/glove.6B.zip "https://nlp.stanford.edu/data/wordvecs/glove.2024.wikigiga.100d.zip" && \
	unzip ./tmp/glove.6B.zip -d ./data-emb/glove-50/
	echo "Done"
	echo ""
fi
echo "glove-50" >> data.txt

echo "" >> data.txt

# Clean up tmp directory
rm -rf ./tmp/

echo "Got all the data"