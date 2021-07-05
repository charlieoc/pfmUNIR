import string
import matplotlib
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.collocations import *

# Archivo de texto a utilizar como fuente
abrir_archivo = "/home/robert/GitHub/pfmUNIR/archivos/texto_conferencias.txt"

with open(abrir_archivo, 'r') as file:
    text = file.read()

# Separar palabras
tokens = word_tokenize(text)

# Transformar a minúsculas
tokens = [w.lower() for w in tokens]

# Quitar puntuación
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]

# Quitar otros caracteres no alfanuméricos
words = [word for word in stripped if word.isalpha()]

personal_words = ['si','mas', 'buenos', 'buenas', 'días', 'gracias']

# Quitar palabras comunes (stop words)
stop_words = stopwords.words('spanish')
stop_words = stop_words + personal_words
words = [w for w in words if not w in stop_words]

# Obtener la frecuencia de las palabras
freq_dist = FreqDist(words)

# Graficar las 25 más utilizadas
freq_dist.plot(25, cumulative=False)

bigram_finder = nltk.collocations.BigramCollocationFinder.from_words(words)
bigram_finder.ngram_fd.most_common(5)
bigram_finder.ngram_fd.tabulate(5)

trigram_finder = nltk.collocations.TrigramCollocationFinder.from_words(words)
trigram_finder.ngram_fd.most_common(5)
trigram_finder.ngram_fd.tabulate(5)

quadgram_finder = nltk.collocations.QuadgramCollocationFinder.from_words(words)
quadgram_finder.ngram_fd.most_common(5)
quadgram_finder.ngram_fd.tabulate(5)

from sentiment_analysis_spanish import sentiment_analysis
import pandas as pd

sentiment = sentiment_analysis.SentimentAnalysisSpanish()

sentencias = sent_tokenize(text)

prob_sentimiento = []

for s in sentencias:
    prob_sentimiento.append([s, sentiment.sentiment(s)])

df = pd.DataFrame(prob_sentimiento, columns=['frase', 'sentiment'])
df.sort_values(by='sentiment', ascending=False)

from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("finiteautomata/beto-sentiment-analysis")

model = AutoModelForSequenceClassification.from_pretrained("finiteautomata/beto-sentiment-analysis")


from transformers import pipeline

classifier = pipeline("sentiment-analysis")

sentencias = sent_tokenize(text)

prob_sentimiento = []

for s in sentencias:
    prob_sentimiento.append([s, classifier(s)])