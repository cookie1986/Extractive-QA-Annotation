import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

# load irrelevant phrases to be filtered
with open('irrelevant_phrases.txt', 'r') as f:
    irrelevant_phrases = f.readlines()
irrelevant_phrases = [phrase.rstrip() for phrase in irrelevant_phrases]

matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
patterns = [nlp.make_doc(phrase) for phrase in irrelevant_phrases]
matcher.add("IrrelevantPhrases", patterns)

def filter_irrelevant_text(input_text):
    doc = nlp(input_text)

    # filter out irrelevant phrases
    filtered_text = []
    for line in doc.splitlines():
        # remove punctuation symbols
        filtered_line = re.sub(r'[^a-zA-Z]', ' ', line)
        line_doc = nlp(filtered_line)
        matches = matcher(line_doc)
        if not matches:
            filtered_text.append(line)
    
    # join filtered text
    cleaned_text = "\n".join(filtered_text)

    return cleaned_text