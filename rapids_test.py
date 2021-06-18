import os
import pandas as pd
import cupy as cp
import cudf
import mysql.connector as msql
import nltk

# Conectar con la BD
conn = msql.connect(user="conferencias", password="i^]D4vJ[$M$5r,6<Kh~F", host="127.0.0.1", port=3306, database="conferencias")

df = pd.read_sql("select contenido from pfm_conferencias;", con=conn)

cuda_df = cudf.DataFrame.from_pandas(df)

cuda_df = cuda_df['Contenido'].apply(word_tokenize)