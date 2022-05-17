import yake
import spacy

# inizializzazione delle variabili necessarie per utilizzare le librerie per il filtro
nlp = spacy.load("it_core_news_lg")

kw_extractor = yake.KeywordExtractor()
audio_string = "Buongiorno! Oggi vi presento la mia famiglia. Io sono il padre, mi chiamo Gennaro Pirlo, " \
               "ho trentasette anni, e lavoro come scrittore e giornalista da quando ne avevo venti. "
language = "it"
max_ngram_size = 2 #numero massimo di parole per una parola chiave
deduplication_threshold = 0.3 #una soglia di duplicazione delle parole nelle parole chiave trovate
numOfKeywords = 50 #numero massimo di parole chiave trovabili
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)
keywords_and_score = custom_kw_extractor.extract_keywords(audio_string)

# copia delle parole chiave trovate dalla libreria in una lista
keywords = []
for kw in keywords_and_score:
    keywords.append(kw[0])

#unisce le parole chiave singole in una stringa
#e le parole chiave doppie vengono salvate in una lista
sentence = ""
sentence2 = []
for word in keywords:
    if " " not in word:
        sentence += word + " "
    else:
        sentence2.append(word)

#le parole chiave doppie se contengono verbi vengono eliminate
for w in sentence2:
    doc1 = nlp(w)
    for w1 in doc1:
        if w1.pos_ == 'VERB':
            if w in keywords:
                keywords.remove(w)

#le parole chiave singole se non sono nomi vengono eliminate
doc = nlp(sentence)
for word in doc:
    if word.pos_ != 'NOUN':
        if word.text in keywords:
            keywords.remove(word.text)

for kw in keywords:
    print(kw)
'''
import spacy
import pke

nlp = spacy.load("it_core_news_lg")

pos = {'NOUN'}
extractor = pke.unsupervised.TopicRank()
audio_string = 'Cerchiamo sempre soluzioni innovative per ridurre il nostro impatto ambientale. I nostri negozi, ' \
               'uffici, data center e centri logistici sono già a impatto zero. Ed entro il 2030 lo saranno anche i ' \
               'nostri prodotti e il loro utilizzo. '
extractor.load_document(audio_string, language='it')
extractor.candidate_selection(pos=pos)
extractor.candidate_weighting()
keyphrases = extractor.get_n_best(n=15)
results = []
for scored_keywords in keyphrases:
    for keyword in scored_keywords:
        if isinstance(keyword, str):
            results.append(keyword)
print(results)

'''
