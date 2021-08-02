from dynaconf import Dynaconf
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# Obtener archivo de texto a utilizar como fuente
settings = Dynaconf(load_dotenv=True, envvar_prefix="PFM")

abrir_archivo = settings.FILE

with open(abrir_archivo, 'r', encoding="UTF-8") as file:
    text = file.read()

model_name = "finiteautomata/beto-sentiment-analysis"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
#inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")

classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
results = classifier(text)


##########################

from transformers import BertForSequenceClassification, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

tokens = tokenizer.encode_plus(txt, add_special_tokens=False,
                               return_tensors='pt')

print(len(tokens['input_ids'][0]))

input_id_chunks = tokens['input_ids'][0].split(510)
mask_chunks = tokens['attention_mask'][0].split(510)

for tensor in input_id_chunks:
    print(len(tensor))

# get required padding length
pad_len = 512 - input_id_chunks[i].shape[0]
# check if tensor length satisfies required chunk size
if pad_len > 0:
    # if padding length is more than 0, we must add padding
    input_id_chunks[i] = torch.cat([
        input_id_chunks[i], torch.Tensor([0] * pad_len)
    ])
    mask_chunks[i] = torch.cat([
        mask_chunks[i], torch.Tensor([0] * pad_len)
    ])

input_ids = torch.stack(input_id_chunks)
attention_mask = torch.stack(mask_chunks)

input_dict = {
    'input_ids': input_ids.long(),
    'attention_mask': attention_mask.int()
}

outputs = model(**input_dict)

probs = torch.nn.functional.softmax(outputs[0], dim=-1)

probs = probs.mean(dim=0)



winner = torch.argmax(probs).item()

['positive', 'negative', 'neutral'][winner]

