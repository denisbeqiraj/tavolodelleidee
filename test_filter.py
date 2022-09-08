import yake
import spacy

# inizializzazione delle variabili necessarie per utilizzare le librerie per il filtro
nlp = spacy.load("it_core_news_lg")

kw_extractor = yake.KeywordExtractor()
audio_string = "Viviamo in un piccolo paese di campagna, in una bella casa con un cortile. I nostri tre figli si " \
               "chiamano Andrea, Martina e Giacomo. Andrea frequenta l'asilo, Martina e Giacomo frequentano le scuole " \
               "elementari. I miei tre figli amano giocare a tanti giochi diversi nel cortile. "
language = "it"
max_ngram_size = 2  # numero massimo di parole per una parola chiave
deduplication_threshold = 0.5  # una soglia di duplicazione delle parole nelle parole chiave trovate
numOfKeywords = 50  # numero massimo di parole chiave trovabili
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)
keywords_and_score = custom_kw_extractor.extract_keywords(audio_string)

# copia delle parole chiave trovate dalla libreria in una lista
keywords = []
for kw in keywords_and_score:
    keywords.append(kw[0])

# copia delle parole chiave trovate dalla libreria in un'altra lista
keywords2 = []
for kw in keywords_and_score:
    keywords2.append(kw[0])

doc = nlp(audio_string)

# analisi delle parole chiave trovate
for word in keywords:
    if " " not in word and "'" not in word:
        # ci si riferisce alle parole chiave composte da una parola
        for token in doc:
            if token.text == word and token.pos_ != "NOUN":
                if word in keywords2:
                    keywords2.remove(word)
    else:
        # ci si riferisce alle parole chiave composte da due parole
        single_word = nlp(word)
        for token in doc:
            # print(token.text + " " + token.pos_)
            if token.text == single_word[0].text and \
                    (token.pos_ == 'VERB' or token.pos_ == 'AUX' or token.pos_ == 'ADV' or token.pos_ == 'SCONJ'):
                keywords2.remove(word)
                break
            elif token.text == single_word[1].text and \
                    (token.pos_ == 'VERB' or token.pos_ == 'AUX' or token.pos_ == 'ADV' or token.pos_ == 'SCONJ'):
                keywords2.remove(word)
                break
            elif token.text == single_word[0].text and (token.pos_ == 'DET' or token.pos_ == 'ADP'):
                keywords.append(single_word[1].text)
                keywords2.append(single_word[1].text)
                keywords2.remove(word)
                break

if "stocazzo" in keywords2:
    keywords2.remove("stocazzo")
if "coglioni" in keywords2:
    keywords2.remove("coglioni")
if "ecc" in keywords2:
    keywords2.remove("ecc")
if "fallo" in keywords2:
    keywords2.remove("fallo")
if "falla" in keywords2:
    keywords2.remove("falla")
if "fammi" in keywords2:
    keywords2.remove("fammi")

for kw in keywords2:
    print(kw)
# print(spacy.explain("DET"))
