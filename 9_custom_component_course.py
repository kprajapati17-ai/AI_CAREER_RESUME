import spacy
from spacy.tokens import Doc
from spacy.language import Language

nlp = spacy.load("en_core_web_sm")

Doc.set_extension("course",default=[])

courses = [
    "python",
    "data science",
    "c",
    "c++",
    "java",
    "cyber security",
    "digital marketing",
    "machine learning",
    "artificial intelligence",
    "web development",
    "cloud computing"
]

@Language.component("FetchCourses")

def FetchCourses(doc):
    
    found_courses = []

    text = doc.text.lower()

    for c in courses:
        if c in text:
            found_courses.append(c)

    doc._.course = found_courses

    return doc

nlp.add_pipe("FetchCourses",last=True)

text = """
I am a Computer Engineering student.
Currently I am learning Python, Data Science and Machine Learning.
After completing these courses I want to study Artificial Intelligence,
Cyber Security and Cloud Computing.
My friend is learning Java and Web Development.
"""


doc = nlp(text)

print("Courses Found")
print("-" * 40)

for c in doc._.course:
    print(c)

print("-" * 40)
print("Total Courses Found =", len(doc._.course))




