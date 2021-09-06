import pandas as pd
from dynaconf import Dynaconf
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

import pandas as pd

frases = pd.read_pickle("./palabras_emocion.pkl")

frases['sentimiento'] = frases['sentimiento'].str.replace('SentimentOutput', '')
frases['sentimiento'] = frases['sentimiento'].str.replace('probas=', '')
frases['sentimiento'] = frases['sentimiento'].str.replace('(', '').str.replace('{','').str.replace(')', '').str.replace('}','')

frases['emocion'] = frases['emocion'].str.replace('EmotionOutput', '')
frases['emocion'] = frases['emocion'].str.replace('probas=', '')
frases['emocion'] = frases['emocion'].str.replace('(', '').str.replace('{','').str.replace(')', '').str.replace('}','')

frases[['sent_winner', 'sent_prob1', 'sent_prob2', 'sent_prob3']] = frases['sentimiento'].str.split(', ', expand=True)
frases[['emo_winner', 'emo_prob1', 'emo_prob2', 'emo_prob3', 'emo_prob4', 'emo_prob5', 'emo_prob6', 'emo_prob7']] = frases['emocion'].str.split(', ', expand=True)

frases[['sent_winner', 'sent_winner_value']] = frases['sent_winner'].str.split('=', expand=True)
frases[['sent_prob1', 'sent_prob1_value']] = frases['sent_prob1'].str.split(': ', expand=True)
frases[['sent_prob2', 'sent_prob2_value']] = frases['sent_prob2'].str.split(': ', expand=True)
frases[['sent_prob3', 'sent_prob3_value']] = frases['sent_prob3'].str.split(': ', expand=True)

frases[['emo_winner', 'emo_winner_value']] = frases['emo_winner'].str.split('=', expand=True)
frases[['emo_prob1', 'emo_prob1_value']] = frases['emo_prob1'].str.split(': ', expand=True)
frases[['emo_prob2', 'emo_prob2_value']] = frases['emo_prob2'].str.split(': ', expand=True)
frases[['emo_prob3', 'emo_prob3_value']] = frases['emo_prob3'].str.split(': ', expand=True)
frases[['emo_prob4', 'emo_prob4_value']] = frases['emo_prob4'].str.split(': ', expand=True)
frases[['emo_prob5', 'emo_prob5_value']] = frases['emo_prob5'].str.split(': ', expand=True)
frases[['emo_prob6', 'emo_prob6_value']] = frases['emo_prob6'].str.split(': ', expand=True)
frases[['emo_prob7', 'emo_prob7_value']] = frases['emo_prob7'].str.split(': ', expand=True)

frases.to_pickle("SentEmo.pkl")

import pandas as pd

frases = pd.read_pickle("SentEmo.pkl")