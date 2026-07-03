import spacy as sa

nlp = sa.load("en_core_web_sm")

paragraph = """
Yesterday, Rohan Patel traveled from Bhavnagar to Ahmedabad.
"""

doc = nlp(paragraph)

print("Named Entities")
print("-" * 30)

for entity in doc.ents:
    print(entity.text, "->", entity.label_)

print("\nFirst 6 Tokens")
print("-" * 30)

span = doc[0:6]

print(span.text)