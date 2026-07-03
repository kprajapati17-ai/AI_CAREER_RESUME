import spacy as sa

nlp = sa.load("en_core_web_sm")

text = """
I am a student. I am learning Python.
NLP is very interesting.
Today I attended a workshop.
"""

doc = nlp(text)

c=0

for tk in doc.sents:
    c+=1
    print(f"Sentence {tk} : {tk.text}")

print("\nTotal Sentences =", c)