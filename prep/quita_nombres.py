import os.path
import regex

# Definir la ruta del archivo de texto
abrir_archivo = "/home/robert/GitHub/pfmUNIR/archivos/texto_conferencias.txt"
crear_archivo = "/home/robert/GitHub/pfmUNIR/archivos/texto_conferencias_snombre.txt"

work_file = open(abrir_archivo, 'r')

lineas = work_file.readlines()

with open(crear_archivo, 'w') as file:
    for linea in lineas:
        if regex.match('^[^:]+:\s+', linea):
            linea = regex.sub('^[^:]+:\s+', '', linea)
        if not linea.isspace():
            file.write(linea)