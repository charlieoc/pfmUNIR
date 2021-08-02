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

