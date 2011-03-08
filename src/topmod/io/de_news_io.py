from glob import glob;
from collections import defaultdict;

from topmod.facility.output_function import output_defaultdict_dict, output_dict
from topmod.io.io_adapter import map_corpus

def parse_de_news_gs(glob_expression, lang="english", doc_limit= -1, title = True, path = False):
    docs = parse_de_news(glob_expression, lang, doc_limit, title, path);
    return docs

def parse_de_news_vi(glob_expression, lang="english", doc_limit= -1, title = True, path = False):
    docs = parse_de_news(glob_expression, lang, doc_limit, title, path);
    return parse_data(docs)

# this method reads in the data from de-news dataset/corpus
# output a dict data type, indexed by the document id, value is a list of the words in that document, not necessarily unique
# this format is generally used for gibbs sampling
def parse_de_news(glob_expression, lang="english", doc_limit= -1, title = True, path = False):
    from nltk.tokenize.treebank import TreebankWordTokenizer
    tokenizer = TreebankWordTokenizer()

    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    if lang.lower() == "english":
        stop = stopwords.words('english')
    elif lang.lower() == "german":
        stop = stopwords.words('german')
    else:
        print "language option unspecified, default to english..."
          
    from string import ascii_lowercase
  
    docs = {}
    files = glob(glob_expression)
    print("Found %i files" % len(files))
    for ii in files:
        text = open(ii).read().lower()
        
        sections = text.split("<doc")
        
        for section in sections:
            if section != None and len(section) != 0:
                index_content = section.split(">\n<h1>\n")
                title_content = index_content[1].split("</h1>")
                # not x in stop: to remove the stopwords
                # min(y in ascii_lowercase for y in x) : to remove punctuation or any expression with punctuation and special symbols
                words = [x for x in tokenizer.tokenize(title_content[1]) if (not x in stop) and (min(y in ascii_lowercase for y in x))]
                if path:
                    if title:
                        docs["%s\t%s\t%s" % (ii, index_content[0].strip(), title_content[0].strip())] = words
                    else:
                        docs["%s\t%s" % (ii, index_content[0].strip())] = words
                else:
                    if title:
                        docs["%s\t%s" % (index_content[0].strip(), title_content[0].strip())] = words
                    else:
                        docs["%s" % (index_content[0].strip())] = words
                                        
        if doc_limit > 0 and len(docs) > doc_limit:
            print("Passed doc limit %i" % len(docs))
            break
    
    return docs

# this method convert a corpus into proper format for training lda model for variational inference
# output a defaultdict(dict) data type, first indexed by the document id, then indexed by the unique tokens
# corpus: a dict data type, indexed by document id, corresponding value is a list of words (not necessarily unique from each other)
def parse_data(corpus):
    docs = defaultdict(dict)
    
    for doc in corpus.keys():
        content = {}
        for term in corpus[doc]:
            if term in content.keys():
                content[term] = content[term] + 1
            else:
                content[term] = 1
        docs[doc] = content
    
    return docs

if __name__ == "__main__":
    data_en = parse_de_news("/windows/d/Data/de-news/txt/*.en.txt", "english",
                  1, False)
    print data_en
    
    data_en = parse_data(data_en)
    data_de = parse_de_news("/windows/d/Data/de-news/txt/*.de.txt", "german",
                  1, False)
    data_de = parse_data(data_de)
    print len(data_en), "\t", len(data_de)
    
    [data_en, data_de] = map_corpus(data_en, data_de)
    print len(data_en), "\t", len(data_de)
    
#lda.initialize(d)

#lda.sample(100)
#lda.print_topics()