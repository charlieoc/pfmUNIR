import mysql.connector as msql
import os.path

# Crear el query
query = "SELECT contenido FROM pfm_conferencias"

# Definir la ruta del archivo de texto
nombre_archivo = "/home/robert/GitHub/pfmUNIR/archivos/texto_conferencias.txt"

# Conectar con la BD
conn = msql.connect(user="conferencias", password="i^]D4vJ[$M$5r,6<Kh~F", host="127.0.0.1", port=3306, database="conferencias")

# Generar el cursor para almacenar los resultados
data_cur = conn.cursor()

# Ejecutar el query para obtener el contenido de la conferencia de la fecha indicada
data_cur.execute(query)

# Guardar los resultados para limpiarlos
registros = data_cur.fetchall()

# Cerrar la conexión a BD
conn.close()

# Preparar el archivo a utilizar
archivo_final = open(nombre_archivo, "w", encoding='utf-8')

# Convertir el dato de la BD a texto, reemplazar \n por salto de línea 
# y poner todo en minúsculas para facilitar el reemplazo de palabras
for linea in registros:
    archivo_final.write(str(linea[0]).replace("\\n", ""))

# Cerrar el archivo    
archivo_final.close()