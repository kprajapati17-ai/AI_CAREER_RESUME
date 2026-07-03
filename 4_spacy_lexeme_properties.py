import spacy as sa

nlp = sa.load("en_core_web_sm")

text = """
I am a student of Computer Engineering at The Easylearn Academy in Ahmedabad.
On 15 June 2026, I paid ₹1200 and scored 95 marks in Python.
"""

doc = nlp(text)

token = doc[5]

print("Token            :", token.text)
print("Lower            :", token.lower_)
print("Lemma            :", token.lemma_)
print("Shape            :", token.shape_)
print("Prefix           :", token.prefix_)
print("Suffix           :", token.suffix_)
print("Length           :", len(token))

print("\n------ Boolean Properties ------")

print("Alphabet         :", token.is_alpha)
print("ASCII            :", token.is_ascii)
print("Digit            :", token.is_digit)
print("Numeric          :", token.like_num)
print("Stop Word        :", token.is_stop)
print("Punctuation      :", token.is_punct)
print("Space            :", token.is_space)
print("Currency         :", token.is_currency)
print("Bracket          :", token.is_bracket)
print("Quote            :", token.is_quote)
print("Left Punct       :", token.is_left_punct)
print("Right Punct      :", token.is_right_punct)

print("\n------ NLP Properties ------")

print("POS              :", token.pos_)
print("Detailed POS     :", token.tag_)
print("Dependency       :", token.dep_)
print("Language         :", token.lang_)
print("Entity Type      :", token.ent_type_)
print("Entity IOB       :", token.ent_iob_)