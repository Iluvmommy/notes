import re
from simpletransformers.question_answering import QuestionAnsweringModel
from simpletransformers.seq2seq import Seq2SeqModel, Seq2SeqArgs
from simpletransformers.ner import NERModel


class Notes:

    def __init__(self, q="questions.txt", t="text.txt", a="answers.txt", n="notes.txt"):
        questions = open(q)
        self.questions = questions.read().split("\n")
        self.text = open(t, "r").read()
        self.answers = open(a, "w")
        self.notes = open(n, "w")
        self.distilbert = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad',
                                                 use_cuda=False)
        self.bart = Seq2SeqModel(encoder_decoder_type="bart", encoder_decoder_name="facebook/bart-large-cnn",
                                 args=Seq2SeqArgs(),
                                 use_cuda=False)
        self.bert = NERModel("bert", "dslim/bert-base-NER", use_cuda=False)

    def predict_answer(self, q):
        f_data = [{
            "context": self.text,
            "qas": [{
                "question": q,
                "id": "1",
            }],
        }]
        ans, probabilities = self.distilbert.predict(f_data)

        if ans:
            return max(ans[1]['answer'], key=len)
        print(q + ": No answer")
        return ''

    def write_answers(self):
        for i, question in enumerate(self.questions):
            try:
                p = self.predict_answer(question)
                ans = str(i + 1) + ". " + p + "\n\n"
                self.answers.write(ans)
                print(ans)
            except EOFError:
                print(EOFError)
                print("Error on #" + str(i + 1))

    def summarize(self, c):
        try:
            summary = self.bart.predict([c])
            return summary[0]
        except:
            print(c[0:10] + "... : Unable to summarize")
            return ""

    def get_entities(self, context):
        try:
            answers, prediction = self.bert.predict([context])
            final = []
            for obj in answers[0]:
                for key, value in obj.items():
                    if value == "B-ORG" or value == "I-PER":
                        final.append(key)
            return final
        except:
            print(context[0:8] + "... : Cannot get entities")
            return []

    def get_notes(self):

        splitParagraphs = re.compile(r"\n+")
        paragraphs = filter(lambda el: el != "", splitParagraphs.split(self.text))

        for p in paragraphs:
            self.notes.write(self.summarize(p) + "\n\n")
            for ent in self.get_entities(p):
                self.notes.write(ent + ": ")
                self.notes.write(self.predict_answer("What is " + ent + "?\n\n"))
