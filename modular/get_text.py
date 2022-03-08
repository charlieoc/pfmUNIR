from os import path
from dynaconf import Dynaconf
import re

## Load environment variables
file_env = Dynaconf(load_dotenv=True, envvar_prefix='FILES')

## Path to the origin directory
file_path = file_env.DIR

## Date to get in format YYYYMMDD
fecha = '20210910'

## Create file name with date and the rest of the name
filename = f'{fecha}_ConferenciaMatutina.txt'

## File to read
open_file = path.join(file_path, filename)

with open(open_file, 'r', encoding='utf8') as f:
    lineas = f.readlines()    

new_file = f'archivos/arch_{fecha}.txt'

parentesis = ['Inaudible', 'inaudible']

with open(new_file, 'w') as file:
    for linea in lineas[1:]:
        if linea.find(':') > 0 and linea[: linea.find(':')].isupper():
            linea = linea.replace(linea[:linea.find(':')+1],'')
        if (
            linea.find("(") >= 0
            and linea.find(")") >= 0
            and (
                linea[linea.find("(") : linea.find(")")].isupper()
                or linea[linea.find("(") + 1 : linea.find(")")] in parentesis
            )
        ):
            linea = linea.replace(linea[linea.find("("):linea.find(")")+1], '')
        if not linea.isspace():
            file.write(linea)