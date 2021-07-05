import pandas as pd
from sentiment_analysis_spanish import sentiment_analysis
from nltk import sent_tokenize
from dynaconf import Dynaconf

# Obtener archivo de texto a utilizar como fuente
settings = Dynaconf(load_dotenv=True, envvar_prefix="PFM")

abrir_archivo = settings.FILE

with open(abrir_archivo, 'r', encoding="UTF-8") as file:
    text = file.read()

# Aplicar modelo de análisis de sentimiento
sentiment = sentiment_analysis.SentimentAnalysisSpanish()

# Separa el texto en enunciados
sentencias = sent_tokenize(text)

# Variable para almacenar el análisis de sentimiento por frase
prob_sentimiento = []

for s in sentencias:
    prob_sentimiento.append([s, sentiment.sentiment(s)])

# Convertir a dataframe y ordenar análisis de sentimiento de positivo a negativo
df = pd.DataFrame(prob_sentimiento, columns=['frase', 'sentiment'])

sorted_df = df.sort_values(by='sentiment', ascending=False)

sorted_df['largo_frase'] = sorted_df['frase'].str.len()

# print(sorted_df.head(n=10).to_string(index=False))

# print(sorted_df.tail(n=10).to_string(index=False))

sorted_df.plot.kde(ind=sorted_df['sentiment'])