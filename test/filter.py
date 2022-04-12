import yake
import spacy

nlp = spacy.load("it_core_news_lg")

kw_extractor = yake.KeywordExtractor()
audio_string = "Cerchiamo sempre soluzioni innovative per ridurre il nostro impatto ambientale. I nostri negozi, " \
               "uffici, data center e centri logistici sono già a impatto zero. Ed entro il 2030 lo saranno anche i " \
               "nostri prodotti e il loro utilizzo. "
language = "it"
max_ngram_size = 2
deduplication_threshold = 0.3
numOfKeywords = 50
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)
keywords_and_score = custom_kw_extractor.extract_keywords(audio_string)

keywords = []
for kw in keywords_and_score:
    keywords.append(kw[0])

sentence = ""
for word in keywords:
    if " " not in word:
        sentence += word + " "

doc = nlp(sentence)
for word in doc:
    if word.pos_ != 'NOUN':
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
