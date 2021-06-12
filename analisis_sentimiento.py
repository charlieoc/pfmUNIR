import mysql.connector as msql
import pandas as pd

# Crear el query
query = "SELECT fechapub, contenido FROM pfm_conferencias order by fechapub asc"

# Conectar con la BD
conn = msql.connect(user="conferencias", password="i^]D4vJ[$M$5r,6<Kh~F", host="127.0.0.1", port=3306, database="conferencias")

# Crear el DataFrame con el resultado del query
df = pd.read_sql(query, conn)



