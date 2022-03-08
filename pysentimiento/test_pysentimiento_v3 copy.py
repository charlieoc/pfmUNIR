import pandas as pd
import mysql.connector as msql
from dynaconf import Dynaconf
from nltk import sent_tokenize, word_tokenize
from collections import Counter
from pysentimiento import SentimentAnalyzer

# Obtener archivo de texto a utilizar como fuente
db_settings = Dynaconf(load_dotenv=True, envvar_prefix="DB")

# Crear el query
query = "SELECT id, fechapub, contenido FROM pfm_conferencias order by fechapub asc"

# Conectar con la BD
conn = msql.connect(user=db_settings.USER, password=db_settings.PWD, host=db_settings.HOST, port=db_settings.PORT, database=db_settings.NAME)

# Generar el cursor para almacenar los resultados
data_cur = conn.cursor()

data_cur.execute(query)

# Guardar los resultados para limpiarlos
registros = pd.DataFrame(data_cur.fetchall())

conn.close()

sentences = []
for row in registros.itertuples():
    sentences.extend(
        (row[1], row[2], sentence) for sentence in sent_tokenize(str(row[3]))
    )

frases = pd.DataFrame(sentences, columns=['ID', 'fechapub', 'frase'])

analyzer = SentimentAnalyzer(lang="es")

sentimiento = [str(analyzer.predict(row[3])) for row in frases.itertuples()]
frases["sentimiento"] = sentimiento

frases.to_pickle("./frases.pkl")

words = []
for row in frases.itertuples():
    words.extend((row[1],row[2], word) for word in word_tokenize(str(row[3])))
palabras = pd.DataFrame(words, columns=['ID', 'fechapub', 'palabra'])

palabras.to_pickle("./palabras.pkl")