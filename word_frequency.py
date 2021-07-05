from dynaconf import Dynaconf
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib


# Obtener archivo de texto a utilizar como fuente
settings = Dynaconf(load_dotenv=True, envvar_prefix="PFM")

abrir_archivo = settings.FILE

with open(abrir_archivo, 'r', encoding="UTF-8") as file:
    text = file.read()

# Separar palabras
tokens = word_tokenize(text)

# Transformar a minúsculas
tokens = [w.lower() for w in tokens]

# Quitar puntuación
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]

# Quitar otros caracteres no alfanuméricos
words = [word for word in stripped if word.isalpha()]

# Quitar palabras comunes (stop words)
stop_words = stopwords.words('spanish')

# Agregar palabras que se pueden considerar superfluas
personal_words = ['si','mas', 'buenos', 'buenas', 'días', 'gracias', 'señor', 'presidente', 'así']

stop_words = stop_words + personal_words
words = [w for w in words if not w in stop_words]

# Obtener la frecuencia de las palabras
freq_dist = FreqDist(words)

# Mostrar las 30 más usadas con su número de apariciones
freq_dist.pprint(30)

# Graficar las 30 más utilizadas
freq_dist.plot(30, cumulative=False)