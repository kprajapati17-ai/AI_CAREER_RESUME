import spacy as sa

nlp = sa.load("en_core_web_sm")

text = "I am learning NLP. Learning NLP is fun. I am a student of Machine Learning."

doc = nlp(text)

print("Tokens\n")

for tk in doc:
    print(tk.text)

print("\nTotal Tokens =", len(doc))