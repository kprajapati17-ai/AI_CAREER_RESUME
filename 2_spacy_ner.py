import spacy as sa

nlp = sa.load("en_core_web_sm")

paragraph = """
Yesterday, Rohan Patel traveled from Bhavnagar to Ahmedabad to attend a technology conference organized by The Easylearn Academy.
"""

doc = nlp(paragraph)


print("Named Entities")
print("-" * 30)

for tk in doc.ents:
    print(f"{tk.text}  {tk.label_}")