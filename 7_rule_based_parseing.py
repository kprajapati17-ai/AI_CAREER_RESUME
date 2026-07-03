import spacy

from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

match = Matcher(nlp.vocab)


text = """
Apple is buying Indian startup for $1 billion.
Elon Musk is the CEO of Tesla.
"""

doc = nlp(text)

pattern = [
    {"LOWER": "apple"},
    {"LOWER": "is"},
    {"LEMMA": "buy"},
    {"LOWER": "indian"},
    {"LOWER": "startup"},
]

match.add("Apple_Buying",[pattern])

matchs = match(doc)

for match_id, start, end in matchs:
    span = doc[start:end]
    print("Pattern :", nlp.vocab.strings[match_id])
    print("Text    :", span.text)
    print("Start   :", start)
    print("End     :", end)