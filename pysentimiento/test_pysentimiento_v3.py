import pandas as pd
import mysql.connector as msql
import regex
from dynaconf import Dynaconf
from nltk import sent_tokenize, word_tokenize
from collections import Counter
from pysentimiento import SentimentAnalyzer, EmotionAnalyzer

# Obtener archivo de texto a utilizar como fuente
db_settings = Dynaconf(load_dotenv=True, envvar_prefix="DB")

# Crear el query
query = "SELECT id, fechapub, contenido FROM pfm_conferencias order by fechapub asc"

# Conectar con la BD
conn = msql.connect(user=db_settings.USER, password=db_settings.PWD, host=db_settings.HOST, port=db_settings.PORT, database=db_settings.NAME)
    
# Generar el cursor para almacenar los resultados
data_cur = conn.cursor()

    # Ejecutar el query para obtener el contenido de la conferencia de la fecha indicada
data_cur.execute(query)

# Guardar los resultados para limpiarlos
registros = pd.DataFrame(data_cur.fetchall())

conn.close()

print("Finalizada extracción BD")

sentences = []
for row in registros.itertuples():
    for sentence in sent_tokenize(str(row[3])):
        sentences.append((row[1],row[2], sentence))

frases_completo = pd.DataFrame(sentences, columns=['ID', 'fechapub', 'frase'])

print ("Fin tokenización")

sentanalyzer = SentimentAnalyzer(lang="es")
emoanalyzer = EmotionAnalyzer(lang="es")

print("Finalizada carga de modelos")

sentimiento = []
emotion = []
i = 0

print("Iniciar iteración de análisis, Número de fila")

for row in frases_completo.itertuples():
    sentimiento.append(str(sentanalyzer.predict(row[3])))
    emotion.append(str(emoanalyzer.predict(row[3])))
    i+=1
    print(i)

frases_completo["sentimiento"] = sentimiento
frases_completo["emocion"] = emotion

print("Grabar pickle")

frases_completo.to_pickle("./palabras_emocion.pkl")