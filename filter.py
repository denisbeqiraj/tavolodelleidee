'''
import spacy

nlp = spacy.load("it_core_news_lg")
audio_string = "spaCy è una libreria software open-source per l'elaborazione avanzata del linguaggio naturale, scritta nei linguaggi di programmazione Python e Cython. La libreria è pubblicata sotto licenza MIT e i suoi principali sviluppatori sono Matthew Honnibal e Ines Montani, i fondatori della società di software Explosion."
doc = nlp(audio_string)
#print([(w.text, w.pos_) for w in doc]) sono i tipi di ogni parola in grammatica
print(doc.ents)
'''

import yake

kw_extractor = yake.KeywordExtractor()
audio_string = "Creare ed arredare un Open space può essere un’operazione costosa, snervante, e talvolta molto lunga, " \
               "però non è, almeno nella maggior parte dei casi, eccessivamente difficile a patto di impostarla in " \
               "maniera chiara e razionale e di attuarla in modo organico, secondo criteri coerenti. "
language = "it"
max_ngram_size = 3
deduplication_threshold = 0.9
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, features=None)
keywords = custom_kw_extractor.extract_keywords(audio_string)
for kw in keywords:
    print(kw)
