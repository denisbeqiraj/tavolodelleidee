from keybert import KeyBERT

doc = "La giovane realtà ha creato un marketplace che unisce le farmacie italiane su un’unica piattaforma digitale, " \
      "ed è quindi attiva in un settore di mercato – l’e-pharmacy – che in Europa e ancor più in Italia ha " \
      "penetrazione prossima allo zero (il canale di vendita principale è offline e copre il 75% degli acquisti), " \
      "ma con enormi potenzialità di crescita e un valore di mercato stimato vicino ai 180 miliardi di euro. " \
      "1000Farmacie non è solo un ecommerce di prodotti parafarmaceutici da banco. Oggi è la piattaforma di farmacie " \
      "online leader in Italia interamente dedicata alla tua salute. Il nostro compito è quello di supportarti " \
      "durante tutto il processo di acquisto di prodotti farmaceutici, dalla consulenza dei nostri farmacisti in chat " \
      "fino al momento in cui ricevi a casa il prodotto ordinato nella farmacia più vicina a te. In questi anni " \
      "abbiamo consegnato più di 1 milione di ordini in oltre 1000 diverse città italiane da altrettante farmacie, " \
      "cercando di garantire un’esperienza impeccabile. "

kw_model = KeyBERT(model="paraphrase-multilingual-MiniLM-L12-v2")
keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), use_maxsum=True, nr_candidates=20)
for k in keywords:
    print(k[0])
