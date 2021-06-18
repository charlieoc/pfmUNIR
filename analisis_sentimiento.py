import mysql.connector as msql
import pandas as pd
#import string as str
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Archivo de texto a utilizar como fuente
abrir_archivo = "/home/robert/GitHub/pfmUNIR/archivos/ConferenciasMatutinas.txt"

with open(abrir_archivo, 'r') as file:
    text = file.read()

# Conectar con la BD
conn = msql.connect(user="conferencias", password="i^]D4vJ[$M$5r,6<Kh~F", host="127.0.0.1", port=3306, database="conferencias")

df = pd.read_sql("select contenido from pfm_conferencias;", con=conn)

# Separar palabras
tokens = df['contenido'].apply(word_tokenize)#(text)

print(tokens)


# Transformar a minúsculas
#tokens = tokens['contenido'].str.lower()#[w.lower() for w in tokens]

# Quitar puntuación
#table = str.maketrans('', '', string.punctuation)
#stripped = [w.translate(table) for w in tokens]

# Quitar otros caracteres no alfanuméricos
#words = [word for word in stripped if word.isalpha()]

# Quitar palabras comunes (stop words)
#stop_words = set(stopwords.words('spanish'))
#words = [w for w in words if not w in stop_words]

#freq_dist = FreqDist(words)

#freq_dist.plot(25, cumulative=False)