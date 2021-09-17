import pandas as pd
from pysentimiento import SentimentAnalyzer, EmotionAnalyzer

sentiment = SentimentAnalyzer(lang="es")
emotion = EmotionAnalyzer(lang="es")

archivo = 'archivos/sents_20210910.txt'

frases = []
emocion = []
sentimiento = []

with open(archivo, 'r', encoding='utf8') as f:
    lineas = f.readlines()

for linea in lineas:
    frases.append(linea)
    res_emocion = str(emotion.predict(linea))
    res_sentimiento = str(sentiment.predict(linea))
    enc_emocion = res_emocion.find('=')
    enc_emo_fin = res_emocion.find(',')
    emocion.append(res_emocion[enc_emocion+1:enc_emo_fin])
    enc_sentimiento = res_sentimiento.find('=')
    enc_sen_fin = res_sentimiento.find(',')
    sentimiento.append(res_sentimiento[enc_sentimiento+1:enc_sen_fin])

analisis = pd.DataFrame(frases, columns=['frases'])

analisis['sentimiento'] = sentimiento
analisis['emocion'] = emocion

analisis.to_csv('archivos/analisis.csv')