from keras_preprocessing.text import text_to_word_sequence


def clean_text(text):
    text = text.replace("\n", " ").replace("\r", " ")
    punct_list = '\'!"#$%&()*+,-./:;<=>?@[\]^_{|}~' #+ '0123456789'
    #punct_list = '\'!"#$%&()*+,./:;<=>?@[\]^_{|}~' + '0123456789'
    t = str.maketrans(dict.fromkeys(punct_list, ""))
    text = text.translate(t)
    return text


def keras_tokenize(text):
    text = clean_text(text)
    tokens = text_to_word_sequence(text)
    return tokens


def getFullText( doc):
    l1 = []
    getFullTextRec(doc, l1)
    return " ".join(l1)


def getFullTextRec( doc, l):
    if isinstance(doc, dict):
        for (k, v) in doc.items():
            getFullTextRec(v, l)
    elif isinstance(doc, list):
        for i in doc:
            getFullTextRec(i, l)

    elif isinstance(doc, str):
        l.append(doc)
    return l


def search( doc, st):
    """
    :param st: string to search
    :return: List of path where st found
    """
    t = []
    q = []
    w = doc
    searchRec(st, w, t, q)
    return q


def searchRec( st, w, p, q):
    """
    search recursively a string into a Dict : Key or Value
    :param st: String to search
    :param w: Dict where search
    :param p: List of string of n-1 path into Dict (overTree)
    :param q: List of string which contains path where st has been found
    :return: List of path where st found
    """
    if isinstance(w, list):
        for a, i in enumerate(w, 0):
            if (isinstance(i, dict) or isinstance(i, list)):
                p.append(a)
            searchRec(st, i, p, q)
    elif isinstance(w, dict):
        for (k, v) in w.items():
            if k == st or v == st:
                # q.append(copy.deepcopy(p))
                q.append(v[0])
            p.append(k)
            searchRec(st, v, p, q)
            p.remove(k)  # rm sub trees when up
    return q
