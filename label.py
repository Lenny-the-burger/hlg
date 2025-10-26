import spacy
import json
import cupy

# shutup torch/cupy warnings
import warnings
import numpy as np
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


# label words with spaCy
spacy.require_gpu()
print("GPU enabled:", spacy.prefer_gpu())

nlp = spacy.load("en_core_web_trf")

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


text = "The Foundation contains many anomalies."
doc = nlp(text)

for token in doc:
    word = dep_to_readable.get(token.dep_, "idk")
    print(f"[{token.text} | {word}]", end=' ')

print()
