from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Archivo de texto a utilizar como fuente
abrir_archivo = "/home/robert/GitHub/pfmUNIR/archivos/ConferenciasMatutinas.txt"

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

# Quitar palabras comunes (stop words)
stop_words = set(stopwords.words('spanish'))
words = [w for w in words if not w in stop_words]

freq_dist = FreqDist(words)

freq_dist.plot(25, cumulative=False)