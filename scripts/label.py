import spacy
import json
import cupy
from tqdm import tqdm
from pathlib import Path
import glob

# shutup torch/cupy warnings
import warnings
import numpy as np
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


# label words with spaCy
spacy.require_gpu()
print("GPU enabled:", spacy.prefer_gpu())

# Load model with only necessary components for speed
nlp = spacy.load("en_core_web_trf", disable=["lemmatizer", "ner", "attribute_ruler"])
print(f"Active pipeline components: {nlp.pipe_names}")

dep_to_readable = {
    # Core sentence roles
    "nsubj": "nominal subject",
    "nsubjpass": "passive nominal subject",
    "csubj": "clausal subject",
    "csubjpass": "passive clausal subject",
    "dobj": "direct object",
    "iobj": "indirect object",
    "pobj": "object of preposition",
    "attr": "attribute or predicate complement",
    "ROOT": "root of the sentence (main verb)",

    # Clauses & complements
    "ccomp": "clausal complement (with its own subject)",
    "xcomp": "open clausal complement (no subject, shares one)",
    "advcl": "adverbial clause modifier",
    "acl": "adjectival clause modifier",
    "relcl": "relative clause modifier",

    # Modifiers
    "amod": "adjectival modifier",
    "advmod": "adverbial modifier",
    "npmod": "noun phrase as adverbial modifier",
    "nmod": "nominal modifier",
    "appos": "appositional modifier",
    "det": "determiner",
    "prep": "prepositional modifier",
    "pcomp": "complement of preposition",
    "poss": "possessive modifier",
    "compound": "compound noun or modifier",
    "nummod": "numeric modifier",
    "quantmod": "quantifier modifier",

    # Function words & structure
    "aux": "auxiliary verb",
    "auxpass": "passive auxiliary verb",
    "cop": "copula (linking verb, like 'be')",
    "mark": "marker (like 'that', 'if', 'because')",
    "case": "case marker (preposition, etc.)",
    "cc": "coordinating conjunction",
    "conj": "conjunct in coordination",
    "preconj": "pre-correlative conjunction (like 'both' in 'both A and B')",

    # Sentence/discourse relations
    "advmod": "adverbial modifier",
    "discourse": "discourse element (like 'well', 'oh')",
    "parataxis": "loosely connected clause (e.g., 'he said', 'she left')",
    "dep": "unspecified dependency",
    "expl": "expletive (dummy subject like 'it' in 'it rains')",

    # Punctuation and misc
    "punct": "punctuation",
    "intj": "interjection",
    "meta": "meta modifier (editorial marks, e.g., '(sic)')",

    # Coordinating and comparative structures
    "cc": "coordinating conjunction",
    "conj": "conjunct in a coordinated phrase",
    "prep": "prepositional modifier",
    "advmod": "adverbial modifier",
    "acomp": "adjectival complement",
    "neg": "negation modifier (e.g., 'not')",
}

def process_file(input_path, output_path, pbar=None):
    """Process a single file and write labeled output"""
    # Read all lines, preserving empty ones
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    # Find non-empty lines for processing
    texts_to_process = [(i, line) for i, line in enumerate(lines) if line.strip()]

    # Process all texts
    processed = {}
    for i, doc in enumerate(nlp.pipe([t[1] for t in texts_to_process], batch_size=256)):
        line_idx = texts_to_process[i][0]
        labeled_line = " ".join([f"{token.text}|{token.dep_}" for token in doc])
        processed[line_idx] = labeled_line

        # Update progress bar if provided
        if pbar:
            pbar.update(1)

    # Write output with preserved structure
    with open(output_path, 'w', encoding='utf-8') as out:
        consecutive_newlines = 0
        for i, line in enumerate(lines):
            if line.strip():
                # Non-empty line - write the labeled version
                out.write(processed[i] + "\n")
                consecutive_newlines = 0
            else:
                # Empty line
                consecutive_newlines += 1
                if consecutive_newlines == 4:
                    out.write("\nEND\nSTART\n")
                    consecutive_newlines = 0
                elif consecutive_newlines < 4:
                    out.write("\n")

    return len(texts_to_process)

# Configuration
NUM_FILES_TO_PROCESS = 3  # Change this to process more/fewer files

# Get all wiki files
print("\nFinding all wiki files...")
input_dirs = [
    "data/data-train/plain-wikitext/1of2",
    "data/data-train/plain-wikitext/2of2"
]

all_files = []
for input_dir in input_dirs:
    wiki_files = sorted(glob.glob(f"{input_dir}/wiki_*"))
    all_files.extend(wiki_files)

# Limit to N files
all_files = all_files[:NUM_FILES_TO_PROCESS]

print(f"Found {len(all_files)} files to process")

# Create output directory
output_dir = Path("data/data-out")
output_dir.mkdir(exist_ok=True, parents=True)

# Count total lines across all files first
print(f"\nCounting total lines...")
total_lines_to_process = 0
for input_file in all_files:
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]
        total_lines_to_process += len(lines)

print(f"Total lines to process: {total_lines_to_process}")

# Process all files with unified progress bar
print(f"\nProcessing {len(all_files)} files...")
total_lines = 0
with tqdm(total=total_lines_to_process, desc="Labeling lines", unit="lines") as pbar:
    for input_file in all_files:
        input_path = Path(input_file)
        # Create output filename preserving directory structure
        if "1of2" in str(input_path):
            output_file = output_dir / f"1of2_{input_path.name}.txt"
        else:
            output_file = output_dir / f"2of2_{input_path.name}.txt"

        lines_processed = process_file(input_path, output_file, pbar)
        total_lines += lines_processed

print(f"\nDone! Processed {len(all_files)} files with {total_lines} total lines.")
print(f"Output saved to: {output_dir}")