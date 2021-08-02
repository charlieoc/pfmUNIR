import pandas as pd
from pysentimiento import SentimentAnalyzer
from dynaconf import Dynaconf
from nltk import sent_tokenize
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Obtener archivo de texto a utilizar como fuente
settings = Dynaconf(load_dotenv=True, envvar_prefix="PFM")

abrir_archivo = settings.FILE

with open(abrir_archivo, 'r', encoding="UTF-8") as file:
    text = file.read()

# Separa el texto en enunciados
sentencias = sent_tokenize(text)

sentencias.sort(key=len)

stop_words = ['Sí.','Buenos días.','¿Mande?','No.','No no.','Sí sí.', 'Ánimo.', 'A ver.', '.', 'Ya.']

sentencias = [s for s in sentencias if len(s) > 25]

analyzer = SentimentAnalyzer(lang="es")

with open(settings.OUTPUT, 'w', encoding="UTF-8") as file:
    for s in sentencias:
        file.write(str(analyzer.predict(s)) + s + "\n")