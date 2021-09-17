import nltk 

es_tokenizer = nltk.data.load("tokenizers/punkt/spanish.pickle")

archivo='archivos/arch_20210910.txt'
destino = 'archivos/sents_20210910.txt'

with open(archivo, 'r', encoding='utf8') as f:
    lineas = f.readlines()

with open(destino, 'w', encoding='utf8') as dest:
    for line in lineas:
        line = line.lstrip()
        tokens = es_tokenizer.tokenize(line)
        for sent in tokens:
            dest.writelines(str(sent) + '\n')