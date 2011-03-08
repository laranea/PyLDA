from glob import glob;
from collections import defaultdict;
from topmod.facility.output_function import output_defaultdict_dict, output_dict

# this method is used for mapping documents correspondence between two corpora, usually for multilingual study
# corpus_a, corpus_b: dict or defaultdict(dict) data type, indexed by document id
# output the corresponding corpus with exact one-to-one mapping on the document id's
def map_corpus(corpus_a, corpus_b):
    common_docs = (set(corpus_a.keys()) & set(corpus_b.keys()));
   
    for doc in corpus_a.keys():
        if doc not in common_docs:
            del corpus_a[doc]
            
    for doc in corpus_b.keys():
        if doc not in common_docs:
            del corpus_b[doc]
            
    return corpus_a, corpus_b

def output_param(alpha, beta, gamma, dir, index=-1):
    if index!=-1:
        postfix = str(index)
    else:
        postfix = ""

    alpha_path = dir + "alpha" + postfix
    f = open(alpha_path, "w");
    for k in alpha.keys():
        f.write(str(k) + "\t" + str(alpha[k]) + "\n")
        
    beta_path = dir + "beta" + postfix
    f = open(beta_path, "w");
    for term in beta.keys():
        for k in beta[term].keys():
            f.write(str(term) + "\t" + str(k) + "\t" + str(beta[term][k]) + "\n")
        
    gamma_path = dir + "gamma" + postfix
    f = open(gamma_path, "w");
    for doc in gamma.keys():
        for k in gamma[doc].keys():
            f.write(str(doc) + "\t" + str(k) + "\t" + str(gamma[doc][k]) + "\n")
            
def output(d):
    f = open("/windows/d/Workspace/data/test_data", "w");
    
    terms = [];
    for value in d.values():
        terms = terms+value;
    terms = set(terms);
    
    termID = {}
    i = 0;
    for t in terms:
        termID[t] = i;
        i+=1;
    
    i = 1;
    for doc in d.keys():
        if len(d[doc])==0:
            continue;
        f.write(str(i) + "\t");
        temp = set(d[doc]);
        for t in temp:
            f.write(str(termID[t])+ "\t"+str(d[doc].count(t))+"\t");
        f.write("\n");
        i+=1;