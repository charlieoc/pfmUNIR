import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

frases = pd.read_pickle("./frases.pkl")

palabras = pd.read_pickle("./palabras.pkl")

frases['sentimiento'] = frases['sentimiento'].str.replace('SentimentOutput', '')

frases['sentimiento'] = frases['sentimiento'].str.replace('probas=', '')

frases['sentimiento'] = frases['sentimiento'].str.replace('(', '').str.replace('{','').str.replace(')', '').str.replace('}','')

frases[['winner', 'prob1', 'prob2', 'prob3']] = frases['sentimiento'].str.split(', ', expand=True)

frases[['prob1', 'prob1_value']] = frases['prob1'].str.split(': ', expand=True)

frases[['prob2', 'prob2_value']] = frases['prob2'].str.split(': ', expand=True)

frases[['prob3', 'prob3_value']] = frases['prob3'].str.split(': ', expand=True)

frases[['winner', 'winner_value']] = frases['winner'].str.split('=', expand=True)

#frases.head().to_csv('./test.csv')

#group = frases.groupby(['fechapub']).size().reset_index(name='counts')

#fig = px.line(group, x='fechapub', y='counts', title='# de frases por fecha en mañaneras')
#fig.show()

start_date = datetime.date(2019,8,1)
end_date = datetime.date(2019,8,31)
mask =  (frases['fechapub'] >= start_date) & (frases['fechapub'] <= end_date)

mes = frases.loc[mask]

group_sentiment = mes.groupby(['fechapub', 'winner_value']).size().reset_index(name='counts')

#print(group_sentiment.head())

fig = px.bar(group_sentiment, x='fechapub', color='winner_value', y='counts',
             title="Sentimiento por frases",
             barmode='group',
             height=800)
fig.show()