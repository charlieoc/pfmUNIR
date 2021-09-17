from os import path, remove
from dynaconf import Dynaconf
from pysentimiento import SentimentAnalyzer, EmotionAnalyzer
import pandas as pd
import nltk 

## Load environment variables
file_env = Dynaconf(load_dotenv=True, envvar_prefix='FILES')

## Path to the origin directory
file_path = file_env.DIR

def fecha_proceso():
    while True:
        ## Date to get in format YYYYMMDD
        fecha = input("Fecha en formato YYYYMMDD: ")
        ## Create file name with date and the rest of the name
        filename = fecha + '_ConferenciaMatutina.txt'
        ## File to read
        open_file = path.join(file_path, filename)
        try:
            path.isfile(open_file)
            print("Fecha válida. Continúa ejecución")
        except OSError:
            print('No existe archivo para la fecha indicada. Intente nuevamente')
        else:
            return open_file, fecha

def elimina_nombres(open_file, fecha):
    with open(open_file, 'r', encoding='utf8') as f:
        lineas = f.readlines()    
    new_file = 'archivos/arch_temp_' + fecha + '.txt'
    parentesis = ['Inaudible', 'inaudible']
    with open(new_file, 'w') as file:
        for linea in lineas[1:]:
            if linea.find(':') > 0:
                if linea[:linea.find(':')].isupper():
                    linea = linea.replace(linea[:linea.find(':')+1],'')
            if linea.find("(") >= 0 and linea.find(")") >= 0:
                if linea[linea.find("("):linea.find(")")].isupper() or linea[linea.find("(")+1:linea.find(")")] in parentesis:
                    linea = linea.replace(linea[linea.find("("):linea.find(")")+1], '')
            if not linea.isspace():
                file.write(linea)
    return new_file

def genera_frases(new_file):
    es_tokenizer = nltk.data.load("tokenizers/punkt/spanish.pickle")
    destino = new_file.replace('arch_temp', 'sent_temp')

    with open(new_file, 'r', encoding='utf8') as f:
        lineas = f.readlines()

    with open(destino, 'w', encoding='utf8') as dest:
        for line in lineas:
            line = line.lstrip()
            tokens = es_tokenizer.tokenize(line)
            for sent in tokens:
                dest.writelines(str(sent) + '\n')
    return destino

def genera_analisis(sent_file):
    sentiment = SentimentAnalyzer(lang="es")
    emotion = EmotionAnalyzer(lang="es")
    frases = []
    emocion = []
    sentimiento = []
    with open(sent_file, 'r', encoding='utf8') as f:
        lineas = f.readlines()

    for linea in lineas:
        frases.append(linea)
        res_emocion = str(emotion.predict(linea))
        res_sentimiento = str(sentiment.predict(linea))
        enc_emocion = res_emocion.find('=')
        enc_emo_fin = res_emocion.find(',')
        emocion.append(res_emocion[enc_emocion+1:enc_emo_fin])
        enc_sentimiento = res_sentimiento.find('=')
        enc_sen_fin = res_sentimiento.find(',')
        sentimiento.append(res_sentimiento[enc_sentimiento+1:enc_sen_fin])
    analisis = pd.DataFrame(frases, columns=['frases'])
    analisis['sentimiento'] = sentimiento
    analisis['emocion'] = emocion
    return analisis

def analisis_to_file(analisis, fecha):
    filename = 'archivos/analisis_' + fecha + '.csv'
    analisis.to_csv(filename)
    print("Archivo generado: " + filename)

def cleanup(arch_temp, sent_temp):
    remove(arch_temp)
    remove(sent_temp)

def main():
    arch_origen, fecha = fecha_proceso()
    print("Iniciar generación de archivos temporales")
    noname_tmp = elimina_nombres(arch_origen, fecha)
    frases_tmp = genera_frases(noname_tmp)
    print("Iniciar análisis con pysentimiento")
    analisis = genera_analisis(frases_tmp)
    print("Escribir CSV con resultados de análisis")
    analisis_to_file(analisis, fecha)
    cleanup(noname_tmp, frases_tmp)

if __name__== "__main__":
    main()

