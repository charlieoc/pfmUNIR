import pandas as pd

frases = pd.read_pickle("SentEmo.pkl")

data = frases["sent_winner_value"].value_counts()

grafica = data.plot.line(x=data[0], y=data[1])


